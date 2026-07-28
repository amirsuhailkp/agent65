"""Persistent visited-URL registry for resumable crawling."""

import json
import logging
import os
from pathlib import Path

from config.settings import settings


logger = logging.getLogger("knowledge_collector.crawler.visited")

_VISITED_FILE_VERSION = 1


class VisitedURLDatabase:
    """Maintain visited URLs with fast lookup and JSON persistence."""

    def __init__(self, file_path: Path | None = None) -> None:
        self._file_path = file_path or settings.logs_directory / "visited_urls.json"
        self._visited_urls: set[str] = set()
        self._skipped_duplicates = 0
        self._new_pages = 0
        self.load()

    def mark_visited(self, url: str) -> bool:
        """Mark a URL as visited and persist state when newly added.

        Returns ``True`` when the URL is newly added; ``False`` when already
        present and therefore skipped as a duplicate.
        """

        normalized = self._validate_url(url)
        if normalized in self._visited_urls:
            self._skipped_duplicates += 1
            self._log_stats("mark_visited(duplicate)")
            return False

        self._visited_urls.add(normalized)
        self._new_pages += 1
        self.save()
        self._log_stats("mark_visited(new)")
        return True

    def is_visited(self, url: str) -> bool:
        """Return whether a URL has already been visited."""

        normalized = self._validate_url(url)
        visited = normalized in self._visited_urls
        self._log_stats("is_visited")
        return visited

    def save(self) -> None:
        """Persist visited URLs using atomic JSON write semantics."""

        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "version": _VISITED_FILE_VERSION,
            "urls": sorted(self._visited_urls),
        }
        temporary_path = self._file_path.with_suffix(f"{self._file_path.suffix}.tmp")
        with temporary_path.open("w", encoding="utf-8", newline="\n") as file:
            json.dump(payload, file, ensure_ascii=False, indent=2)
            file.flush()
            os.fsync(file.fileno())
        temporary_path.replace(self._file_path)
        self._log_stats("save")

    def load(self) -> None:
        """Load visited URLs from JSON at startup when available."""

        if not self._file_path.is_file():
            self._visited_urls.clear()
            self._log_stats("load(empty)")
            return

        state = json.loads(self._file_path.read_text(encoding="utf-8"))
        if state.get("version") != _VISITED_FILE_VERSION:
            raise ValueError(f"unsupported visited file version: {state.get('version')}")
        urls = state.get("urls")
        if not isinstance(urls, list) or not all(isinstance(value, str) for value in urls):
            raise ValueError("visited URL database must contain a list of strings")

        self._visited_urls = {self._validate_url(url) for url in urls}
        self._log_stats("load")

    @property
    def visited_count(self) -> int:
        """Expose current number of unique visited URLs."""

        return len(self._visited_urls)

    @property
    def urls(self) -> tuple[str, ...]:
        """Return a stable snapshot of all completed URLs."""

        return tuple(sorted(self._visited_urls))

    def restore(self, urls: tuple[str, ...]) -> None:
        """Restore URLs saved in a crawl checkpoint and persist the union."""

        restored = {self._validate_url(url) for url in urls}
        if restored.difference(self._visited_urls):
            self._visited_urls.update(restored)
            self.save()
        self._log_stats("restore")

    @staticmethod
    def _validate_url(url: str) -> str:
        if not isinstance(url, str):
            raise TypeError("url must be a string")
        normalized = url.strip()
        if not normalized:
            raise ValueError("url cannot be empty")
        return normalized

    def _log_stats(self, operation: str) -> None:
        logger.info(
            "Visited DB operation=%s visited_count=%s skipped_duplicates=%s new_pages=%s",
            operation,
            len(self._visited_urls),
            self._skipped_duplicates,
            self._new_pages,
        )
