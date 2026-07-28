"""Terminal and file-log progress reporting for crawl operations."""

from __future__ import annotations

import logging
import sys
import time
from collections.abc import Callable
from typing import TextIO


logger = logging.getLogger("knowledge_collector.crawl_progress")


class CrawlProgressTracker:
    """Render crawl state cleanly in an interactive terminal and log snapshots."""

    def __init__(
        self,
        *,
        total_pages: int | None = None,
        stream: TextIO | None = None,
        clock: Callable[[], float] | None = None,
        enabled: bool | None = None,
    ) -> None:
        self._total_pages = total_pages
        self._stream = stream or sys.stdout
        self._clock = clock or time.monotonic
        self._enabled = self._stream.isatty() if enabled is None else enabled
        self._started_at = self._clock()
        self._has_rendered = False

    def update(
        self,
        *,
        current_page: int,
        pages_completed: int,
        pages_remaining: int,
        queue_size: int,
        visited_pages: int,
        current_depth: int,
        current_url: str,
    ) -> None:
        """Display and log the current crawl state."""

        elapsed_seconds = max(0.0, self._clock() - self._started_at)
        estimated_remaining_seconds = _estimate_remaining(
            elapsed_seconds,
            pages_completed,
            pages_remaining,
        )
        lines = (
            f"Current page: {current_page}",
            f"Pages completed: {pages_completed}",
            f"Pages remaining: {pages_remaining}",
            f"Queue size: {queue_size}",
            f"Visited pages: {visited_pages}",
            f"Current depth: {current_depth}",
            f"Elapsed time: {_format_duration(elapsed_seconds)}",
            f"Estimated remaining time: {_format_duration(estimated_remaining_seconds)}",
            f"Current URL: {current_url}",
        )
        logger.info(" | ".join(lines))

        if self._enabled:
            prefix = "\r\033[2J\033[H" if self._has_rendered else ""
            self._stream.write(prefix + "Crawl progress\n" + "\n".join(lines) + "\n")
            self._stream.flush()
            self._has_rendered = True

    def finish(self) -> None:
        """End an interactive progress display on a fresh terminal line."""

        if self._enabled and self._has_rendered:
            self._stream.write("\n")
            self._stream.flush()


def _estimate_remaining(elapsed_seconds: float, completed: int, remaining: int) -> float:
    if completed <= 0:
        return 0.0
    return elapsed_seconds / completed * max(0, remaining)


def _format_duration(seconds: float) -> str:
    total_seconds = int(round(seconds))
    minutes, seconds_part = divmod(total_seconds, 60)
    hours, minutes_part = divmod(minutes, 60)
    if hours:
        return f"{hours:d}:{minutes_part:02d}:{seconds_part:02d}"
    return f"{minutes_part:02d}:{seconds_part:02d}"
