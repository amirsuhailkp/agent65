"""Breadth-first crawler for same-site HTML page discovery."""

from __future__ import annotations

import logging
import time
from collections import deque
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol
from urllib.parse import urlsplit

from config.settings import settings

from .domain_filter import DomainFilter
from .checkpoint import CheckpointQueueItem, CrawlCheckpoint, CrawlCheckpointState
from .progress import CrawlProgressTracker
from .page_processor import CrawlPageProcessor, ProcessedCrawlPage
from .rate_limiter import RateLimiter
from .robots import RobotsPolicy
from .url_discovery import URLDiscoveryEngine
from .visited import VisitedURLDatabase


logger = logging.getLogger("knowledge_collector.crawler.bfs")


class HtmlFetcher(Protocol):
    """Minimal fetch boundary required for crawling."""

    def download(self, url: str) -> str:
        """Return HTML for one URL."""


class _FetchOnlyPageProcessor:
    """Compatibility adapter for discovery-only callers of ``BFSCrawler``."""

    def __init__(self, fetcher: HtmlFetcher, download: Callable[[str], str]) -> None:
        self._fetcher = fetcher
        self._download = download

    def process(self, url: str) -> ProcessedCrawlPage:
        html = self._download(url)
        return ProcessedCrawlPage(
            discovery_html=html,
            final_url=url,
            download_size_bytes=len(html.encode("utf-8")),
            extraction_size_bytes=0,
            extraction_collected=False,
        )


@dataclass(frozen=True, slots=True)
class CrawlStatistics:
    """Outcome metrics for one BFS crawl run."""

    pages_visited: int
    pages_failed: int
    skipped_visited_urls: int
    links_discovered: int
    links_enqueued: int
    max_depth_reached: int
    queue_size_remaining: int
    duration_seconds: float
    stop_reason: str
    duplicate_urls: int = 0
    external_urls: int = 0
    download_size_bytes: int = 0
    extraction_size_bytes: int = 0
    extraction_collected: bool = False
    errors: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class _QueueItem:
    url: str
    depth: int


class BFSCrawler:
    """Traverse same-site pages with breadth-first ordering and hard limits."""

    def __init__(
        self,
        fetcher: HtmlFetcher,
        *,
        page_processor: CrawlPageProcessor | None = None,
        url_discovery: URLDiscoveryEngine | None = None,
        domain_filter: DomainFilter | None = None,
        visited: VisitedURLDatabase | None = None,
        max_pages: int = 100,
        max_depth: int = 2,
        max_runtime_seconds: float = 300.0,
        # `max_pages=0` is a documented sentinel meaning "unlimited pages";
        # the crawl then stops only when the queue is empty or robots.txt
        # disallows further URLs. `max_depth`'s existing meaning (0 = only
        # the start URL) is unchanged; callers who want effectively unlimited
        # depth alongside unlimited pages pass a very large max_depth (the
        # CLI does this automatically -- see main.py).
        delay_between_requests_seconds: float | None = None,
        ignore_robots: bool | None = None,
        robots: RobotsPolicy | None = None,
        rate_limiter: RateLimiter | None = None,
        progress: CrawlProgressTracker | None = None,
        checkpoint_path: Path | None = None,
        time_provider: Callable[[], float] | None = None,
        sleep: Callable[[float], None] | None = None,
    ) -> None:
        if max_pages < 0:
            raise ValueError("max_pages cannot be negative (use 0 for unlimited)")
        if max_depth < 0:
            raise ValueError("max_depth cannot be negative")
        if max_runtime_seconds <= 0:
            raise ValueError("max_runtime_seconds must be greater than zero")
        if delay_between_requests_seconds is not None and delay_between_requests_seconds < 0:
            raise ValueError("delay_between_requests_seconds cannot be negative")

        self._fetcher = fetcher
        self._url_discovery = url_discovery or URLDiscoveryEngine()
        self._domain_filter = domain_filter or DomainFilter()
        self._visited = visited or VisitedURLDatabase()
        self._max_pages = max_pages
        self._max_depth = max_depth
        self._max_runtime_seconds = max_runtime_seconds
        self._time = time_provider or time.monotonic
        self._sleep = sleep or time.sleep
        self._rate_limiter = rate_limiter or RateLimiter(
            settings.crawl_delay_seconds
            if delay_between_requests_seconds is None
            else delay_between_requests_seconds,
            sleep=self._sleep,
        )
        if ignore_robots is None:
            ignore_robots = settings.ignore_robots
        self._robots = robots or RobotsPolicy(
            self._download,
            ignore_robots=ignore_robots,
        )
        self._progress = progress or CrawlProgressTracker(
            total_pages=None if max_pages == 0 else max_pages
        )
        self._checkpoint = CrawlCheckpoint(
            checkpoint_path or settings.logs_directory / "crawl_checkpoint.json"
        )
        self._download_size_bytes = 0
        self._extraction_size_bytes = 0
        self._extraction_collected = False
        self._page_processor = page_processor or _FetchOnlyPageProcessor(fetcher, self._download)

    def crawl(self, start_url: str, *, resume: bool = False) -> CrawlStatistics:
        """Run BFS from one start URL and return crawl statistics."""

        normalized_start = _normalize_start_url(start_url)
        start_host = _hostname(normalized_start)
        if start_host is None:
            raise ValueError("start_url must be an absolute HTTP(S) URL")

        started_at = self._time()
        checkpoint_started_at = time.monotonic()
        pages_visited = 0
        pages_failed = 0
        skipped_visited_urls = 0
        links_discovered = 0
        links_enqueued = 0
        max_depth_reached = 0
        previous_duration_seconds = 0.0
        duplicate_urls = 0
        external_urls = 0
        errors: list[str] = []
        warnings: list[str] = []
        stop_reason = "completed"
        self._download_size_bytes = 0
        self._extraction_size_bytes = 0
        self._extraction_collected = False

        if resume:
            state = self._checkpoint.load(normalized_start)
            self._visited.restore(state.visited_urls)
            queue = deque(_QueueItem(item.url, item.depth) for item in state.queue)
            queued_urls = {item.url for item in queue}
            pages_visited = _stat_int(state.statistics, "pages_visited")
            pages_failed = _stat_int(state.statistics, "pages_failed")
            skipped_visited_urls = _stat_int(state.statistics, "skipped_visited_urls")
            links_discovered = _stat_int(state.statistics, "links_discovered")
            links_enqueued = _stat_int(state.statistics, "links_enqueued")
            max_depth_reached = _stat_int(state.statistics, "max_depth_reached")
            previous_duration_seconds = _stat_float(state.statistics, "duration_seconds")
            duplicate_urls = _stat_int(state.statistics, "duplicate_urls")
            external_urls = _stat_int(state.statistics, "external_urls")
            download_size_bytes = _stat_int(state.statistics, "download_size_bytes")
            self._download_size_bytes = download_size_bytes
            self._extraction_size_bytes = _stat_int(state.statistics, "extraction_size_bytes")
            self._extraction_collected = _stat_bool(state.statistics, "extraction_collected")
            errors = _stat_strings(state.statistics, "errors")
            warnings = _stat_strings(state.statistics, "warnings")
            logger.info("Resuming crawl at %s with %s queued URLs", state.current_url, len(queue))
        else:
            queue = deque([_QueueItem(normalized_start, 0)])
            queued_urls = {normalized_start}

        def checkpoint(current: _QueueItem | None = None) -> None:
            self._checkpoint.save(
                CrawlCheckpointState(
                    start_url=normalized_start,
                    queue=tuple(CheckpointQueueItem(item.url, item.depth) for item in queue),
                    visited_urls=self._visited.urls,
                    statistics={
                        "pages_visited": pages_visited,
                        "pages_failed": pages_failed,
                        "skipped_visited_urls": skipped_visited_urls,
                        "links_discovered": links_discovered,
                        "links_enqueued": links_enqueued,
                        "max_depth_reached": max_depth_reached,
                        "queue_size_remaining": len(queue),
                        "duration_seconds": previous_duration_seconds
                        + max(0.0, time.monotonic() - checkpoint_started_at),
                        "stop_reason": stop_reason,
                        "duplicate_urls": duplicate_urls,
                        "external_urls": external_urls,
                        "download_size_bytes": self._download_size_bytes,
                        "extraction_size_bytes": self._extraction_size_bytes,
                        "extraction_collected": self._extraction_collected,
                        "errors": errors,
                        "warnings": warnings,
                    },
                    current_depth=current.depth if current else None,
                    current_url=current.url if current else None,
                )
            )

        checkpoint()

        try:
            while queue:
                elapsed = self._time() - started_at
                if elapsed >= self._max_runtime_seconds:
                    stop_reason = "max_runtime"
                    break
                if self._max_pages and pages_visited >= self._max_pages:
                    stop_reason = "max_pages"
                    break

                # Keep the active item queued until its fetch has completed.
                # A process interruption can therefore only repeat unfinished work.
                current = queue[0]
                checkpoint(current)
                self._progress.update(
                    current_page=pages_visited + pages_failed + 1,
                    pages_completed=pages_visited,
                    pages_remaining=len(queue),
                    queue_size=len(queue),
                    visited_pages=pages_visited,
                    current_depth=current.depth,
                    current_url=current.url,
                )

                if self._visited.is_visited(current.url):
                    queue.popleft()
                    queued_urls.discard(current.url)
                    skipped_visited_urls += 1
                    checkpoint()
                    continue

                if not self._robots.can_fetch(current.url):
                    queue.popleft()
                    queued_urls.discard(current.url)
                    checkpoint()
                    continue

                try:
                    processed_page = self._page_processor.process(current.url)
                except Exception as exc:
                    queue.popleft()
                    queued_urls.discard(current.url)
                    pages_failed += 1
                    errors.append(f"{current.url}: {exc}")
                    logger.warning("Failed to download %s: %s", current.url, exc)
                    checkpoint()
                    continue

                if not self._visited.mark_visited(current.url):
                    queue.popleft()
                    queued_urls.discard(current.url)
                    skipped_visited_urls += 1
                    checkpoint()
                    continue

                queue.popleft()
                queued_urls.discard(current.url)
                pages_visited += 1
                self._download_size_bytes += processed_page.download_size_bytes
                self._extraction_size_bytes += processed_page.extraction_size_bytes
                self._extraction_collected = (
                    self._extraction_collected or processed_page.extraction_collected
                )
                max_depth_reached = max(max_depth_reached, current.depth)
                logger.info("Visited page: %s (depth=%s)", current.url, current.depth)

                if current.depth < self._max_depth:
                    discovered = self._url_discovery.discover_urls(
                        processed_page.discovery_html,
                        base_url=processed_page.final_url,
                    )
                    links_discovered += len(discovered)
                    external_urls += sum(not _is_same_website(url, start_host) for url in discovered)

                    filtered = self._domain_filter.filter_same_website_urls(
                        current_domain=start_host,
                        candidate_urls=discovered,
                    )
                    for candidate in filtered:
                        if candidate in queued_urls:
                            duplicate_urls += 1
                            continue
                        if self._visited.is_visited(candidate):
                            skipped_visited_urls += 1
                            duplicate_urls += 1
                            continue
                        queue.append(_QueueItem(candidate, current.depth + 1))
                        queued_urls.add(candidate)
                        links_enqueued += 1
                checkpoint()
        except BaseException:
            checkpoint(queue[0] if queue else None)
            self._progress.finish()
            raise

        duration = previous_duration_seconds + self._time() - started_at
        statistics = CrawlStatistics(
            pages_visited=pages_visited,
            pages_failed=pages_failed,
            skipped_visited_urls=skipped_visited_urls,
            links_discovered=links_discovered,
            links_enqueued=links_enqueued,
            max_depth_reached=max_depth_reached,
            queue_size_remaining=len(queue),
            duration_seconds=duration,
            stop_reason=stop_reason,
            duplicate_urls=duplicate_urls,
            external_urls=external_urls,
            download_size_bytes=self._download_size_bytes,
            extraction_size_bytes=self._extraction_size_bytes,
            extraction_collected=self._extraction_collected,
            errors=tuple(errors),
            warnings=tuple(warnings),
        )
        self._progress.finish()
        if queue:
            checkpoint(queue[0])
        else:
            self._checkpoint.clear()
        return statistics

    def _download(self, url: str) -> str:
        """Pace a fetch operation, including robots.txt downloads."""

        self._rate_limiter.wait(url)
        return self._fetcher.download(url)


def _normalize_start_url(url: str) -> str:
    if not isinstance(url, str) or not url.strip():
        raise ValueError("start_url cannot be empty")
    return url.strip()


def _hostname(url: str) -> str | None:
    parsed = urlsplit(url)
    if parsed.scheme.casefold() not in {"http", "https"}:
        return None
    if not parsed.hostname:
        return None
    return parsed.hostname.casefold().removeprefix("www.")


def _is_same_website(url: str, domain: str) -> bool:
    host = _hostname(url)
    return host is not None and (host == domain or host.endswith(f".{domain}"))


def _stat_int(statistics: dict[str, object], name: str) -> int:
    value = statistics.get(name, 0)
    if not isinstance(value, int) or value < 0:
        raise ValueError(f"invalid checkpoint statistic: {name}")
    return value


def _stat_float(statistics: dict[str, object], name: str) -> float:
    value = statistics.get(name, 0.0)
    if not isinstance(value, (int, float)) or value < 0:
        raise ValueError(f"invalid checkpoint statistic: {name}")
    return float(value)


def _stat_bool(statistics: dict[str, object], name: str) -> bool:
    value = statistics.get(name, False)
    if not isinstance(value, bool):
        raise ValueError(f"invalid checkpoint statistic: {name}")
    return value


def _stat_strings(statistics: dict[str, object], name: str) -> list[str]:
    value = statistics.get(name, [])
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"invalid checkpoint statistic: {name}")
    return list(value)
