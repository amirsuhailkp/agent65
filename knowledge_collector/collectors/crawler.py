"""Checkpointed same-domain URL discovery for documentation sites.

The crawler fetches HTML solely to discover links. It neither stores page bodies
nor invokes extraction, conversion, cleaning, or metadata workflows.
"""

import json
import logging
import os
from collections import deque
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Protocol
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

from bs4 import BeautifulSoup

from config.settings import settings
from crawler.visited import VisitedURLDatabase
from crawler.robots import RobotsPolicy
from crawler.rate_limiter import RateLimiter
from crawler.progress import CrawlProgressTracker
from downloader.downloader import DEFAULT_USER_AGENT, DownloaderError


logger = logging.getLogger("knowledge_collector.crawler")

_IGNORED_SUFFIXES = frozenset(
    {
        ".7z", ".avi", ".bmp", ".bz2", ".csv", ".doc", ".docx", ".epub",
        ".gif", ".gz", ".ico", ".iso", ".jpeg", ".jpg", ".mkv", ".mov",
        ".mp3", ".mp4", ".pdf", ".png", ".ppt", ".pptx", ".rar", ".svg",
        ".tar", ".tgz", ".tif", ".tiff", ".webm", ".webp", ".xls", ".xlsx",
        ".zip",
    }
)
_TRACKING_PARAMETERS = frozenset({"fbclid", "gclid", "mc_cid", "mc_eid"})
_QUEUE_VERSION = 1


class HtmlFetcher(Protocol):
    """Minimal network boundary required for HTML discovery."""

    def download(self, url: str) -> str:
        """Return the HTML response body for a URL."""


@dataclass(frozen=True, slots=True)
class QueueItem:
    """A pending crawl target and its distance from the starting URL."""

    url: str
    depth: int


class WebsiteCrawler:
    """Discover internal HTML URLs using breadth-first, resumable traversal.

    Args:
        fetcher: HTTP boundary used to retrieve HTML in memory.
        max_depth: Maximum link distance from the start URL; zero visits only it.
        max_pages: Safety limit for pages fetched per invocation. Queue state is
            persisted at the limit, allowing the next run to resume.
        queue_path: JSON checkpoint location. Defaults to ``logs/crawl_queue.json``.
        respect_robots: Whether to honor parsed ``robots.txt`` directives.
        ignore_robots: Explicitly bypass robots policy. Takes precedence over
            ``respect_robots`` and the global setting.
        user_agent: Identifier supplied to ``robots.txt`` policy evaluation.
    """

    def __init__(
        self,
        fetcher: HtmlFetcher,
        *,
        max_depth: int = 2,
        max_pages: int = 1_000,
        queue_path: Path | None = None,
        visited_path: Path | None = None,
        respect_robots: bool | None = None,
        ignore_robots: bool | None = None,
        user_agent: str = DEFAULT_USER_AGENT,
        rate_limiter: RateLimiter | None = None,
        progress: CrawlProgressTracker | None = None,
    ) -> None:
        if max_depth < 0:
            raise ValueError("max_depth cannot be negative")
        if max_pages < 1:
            raise ValueError("max_pages must be at least one")
        if not user_agent.strip():
            raise ValueError("user_agent cannot be empty")

        self._fetcher = fetcher
        self._max_depth = max_depth
        self._max_pages = max_pages
        self._queue_path = queue_path or settings.logs_directory / "crawl_queue.json"
        self._visited = VisitedURLDatabase(visited_path or settings.logs_directory / "visited_urls.json")
        self._rate_limiter = rate_limiter or RateLimiter(settings.crawl_delay_seconds)
        self._progress = progress or CrawlProgressTracker(total_pages=max_pages)
        if ignore_robots is None:
            ignore_robots = settings.ignore_robots if respect_robots is None else not respect_robots
        self._robots = RobotsPolicy(
            self._download,
            user_agent=user_agent,
            ignore_robots=ignore_robots,
        )

    def crawl(self, start_url: str, *, resume: bool = False) -> list[str]:
        """Return discovered URLs, starting from one same-domain URL.

        Each successful HTML fetch is checkpointed. With ``resume=True``, the
        existing queue is restored only if it belongs to the same start URL.
        """

        canonical_start = _canonicalize_url(start_url)
        if canonical_start is None:
            raise ValueError("start_url must be an absolute HTTP(S) URL")

        if resume:
            pending, visited, skipped = self._load_state(canonical_start)
            logger.info("Resuming crawl with %s pending URLs", len(pending))
        else:
            pending, visited, skipped = deque([QueueItem(canonical_start, 0)]), [], set()
            self._save_state(canonical_start, pending, visited, skipped)

        visited_set = set(visited)
        pending_urls = {item.url for item in pending}
        processed_this_run = 0

        while pending and processed_this_run < self._max_pages:
            item = pending.popleft()
            pending_urls.discard(item.url)
            self._progress.update(
                current_page=processed_this_run + 1,
                pages_completed=processed_this_run,
                pages_remaining=len(pending),
                queue_size=len(pending),
                visited_pages=len(visited),
                current_depth=item.depth,
                current_url=item.url,
            )
            if item.url in skipped:
                continue
            if item.url in visited_set:
                continue
            if self._visited.is_visited(item.url):
                continue
            if not self._robots.can_fetch(item.url):
                logger.info("Skipping robots-disallowed URL: %s", item.url)
                skipped.add(item.url)
                self._save_state(canonical_start, pending, visited, skipped)
                continue

            try:
                html = self._download(item.url)
            except DownloaderError as exc:
                logger.warning("Skipping unavailable URL %s: %s", item.url, exc)
                skipped.add(item.url)
                self._save_state(canonical_start, pending, visited, skipped)
                continue

            is_new_page = self._visited.mark_visited(item.url)
            if not is_new_page:
                skipped.add(item.url)
                self._save_state(canonical_start, pending, visited, skipped)
                continue

            visited.append(item.url)
            visited_set.add(item.url)
            processed_this_run += 1
            logger.info("Crawled URL %s (depth=%s)", item.url, item.depth)

            if item.depth < self._max_depth:
                for target_url in self._discover_links(html, item.url, canonical_start):
                    if target_url not in visited_set and target_url not in skipped and target_url not in pending_urls:
                        pending.append(QueueItem(target_url, item.depth + 1))
                        pending_urls.add(target_url)

            self._save_state(canonical_start, pending, visited, skipped)

        if pending:
            logger.info("Crawl paused at max_pages=%s; %s URLs remain queued", self._max_pages, len(pending))
        else:
            logger.info("Crawl completed with %s URLs", len(visited))
        self._progress.finish()
        return visited

    def _download(self, url: str) -> str:
        """Pace every network operation, including robots.txt downloads."""

        self._rate_limiter.wait(url)
        return self._fetcher.download(url)

    def _discover_links(self, html: str, current_url: str, start_url: str) -> Iterable[str]:
        start_host = urlsplit(start_url).hostname
        soup = BeautifulSoup(html, "html.parser")
        for anchor in soup.select("a[href]"):
            target_url = _canonicalize_url(urljoin(current_url, anchor["href"]))
            if target_url is None or urlsplit(target_url).hostname != start_host:
                continue
            if _is_ignored_resource(target_url):
                continue
            yield target_url

    def _load_state(self, start_url: str) -> tuple[deque[QueueItem], list[str], set[str]]:
        if not self._queue_path.is_file():
            raise FileNotFoundError(f"crawl queue does not exist: {self._queue_path}")
        try:
            state = json.loads(self._queue_path.read_text(encoding="utf-8"))
            if state.get("version") != _QUEUE_VERSION or state.get("start_url") != start_url:
                raise ValueError("crawl queue does not match this start URL")
            pending = deque(QueueItem(**item) for item in state["pending"])
            visited = list(state["visited"])
            skipped = set(state.get("skipped", []))
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            raise ValueError(f"invalid crawl queue: {self._queue_path}") from exc
        return pending, visited, skipped

    def _save_state(
        self,
        start_url: str,
        pending: deque[QueueItem],
        visited: list[str],
        skipped: set[str],
    ) -> None:
        state = {
            "version": _QUEUE_VERSION,
            "start_url": start_url,
            "max_depth": self._max_depth,
            "pending": [asdict(item) for item in pending],
            "visited": visited,
            "skipped": sorted(skipped),
        }
        self._queue_path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = self._queue_path.with_suffix(f"{self._queue_path.suffix}.tmp")
        with temporary_path.open("w", encoding="utf-8", newline="\n") as queue_file:
            json.dump(state, queue_file, ensure_ascii=False, indent=2)
            queue_file.flush()
            os.fsync(queue_file.fileno())
        temporary_path.replace(self._queue_path)


def _canonicalize_url(url: str) -> str | None:
    parsed = urlsplit(url)
    if parsed.scheme.casefold() not in {"http", "https"} or not parsed.hostname:
        return None
    filtered_query = [
        (key, value)
        for key, value in parse_qsl(parsed.query, keep_blank_values=True)
        if not key.casefold().startswith("utm_") and key.casefold() not in _TRACKING_PARAMETERS
    ]
    hostname = parsed.hostname.casefold()
    netloc = hostname if parsed.port is None else f"{hostname}:{parsed.port}"
    path = parsed.path or "/"
    return urlunsplit((parsed.scheme.casefold(), netloc, path, urlencode(filtered_query, doseq=True), ""))


def _is_ignored_resource(url: str) -> bool:
    return Path(urlsplit(url).path).suffix.casefold() in _IGNORED_SUFFIXES
