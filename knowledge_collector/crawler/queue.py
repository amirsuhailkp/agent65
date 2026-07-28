"""Persistent FIFO queue for resumable crawl workflows."""

import json
import logging
import os
from collections import deque
from pathlib import Path


logger = logging.getLogger("knowledge_collector.crawler.queue")

_QUEUE_FILE_VERSION = 1


class CrawlQueue:
    """FIFO URL queue with duplicate prevention and JSON persistence."""

    def __init__(self, items: list[str] | None = None) -> None:
        self._queue: deque[str] = deque()
        self._seen: set[str] = set()
        for item in items or []:
            self.enqueue(item)
        self._log_size("initialize")

    def enqueue(self, item: str) -> bool:
        """Enqueue one URL unless it is already present.

        Returns ``True`` when added, ``False`` when skipped as duplicate.
        """

        normalized = self._validate_item(item)
        if normalized in self._seen:
            self._log_size("enqueue(skip-duplicate)")
            return False
        self._queue.append(normalized)
        self._seen.add(normalized)
        self._log_size("enqueue")
        return True

    def dequeue(self) -> str:
        """Remove and return the next URL in FIFO order."""

        item = self._queue.popleft()
        self._seen.remove(item)
        self._log_size("dequeue")
        return item

    def peek(self) -> str | None:
        """Return the next URL without removing it."""

        next_item = self._queue[0] if self._queue else None
        self._log_size("peek")
        return next_item

    def is_empty(self) -> bool:
        """Return whether the queue has no pending URLs."""

        empty = not self._queue
        self._log_size("is_empty")
        return empty

    def size(self) -> int:
        """Return the number of pending URLs."""

        queue_size = len(self._queue)
        self._log_size("size")
        return queue_size

    def to_list(self) -> list[str]:
        """Return queue contents in dequeue order."""

        return list(self._queue)

    def save_to_json(self, file_path: Path) -> None:
        """Persist queue state atomically for interruption-safe resume."""

        target = Path(file_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "version": _QUEUE_FILE_VERSION,
            "items": self.to_list(),
        }
        temporary = target.with_suffix(f"{target.suffix}.tmp")
        with temporary.open("w", encoding="utf-8", newline="\n") as queue_file:
            json.dump(payload, queue_file, ensure_ascii=False, indent=2)
            queue_file.flush()
            os.fsync(queue_file.fileno())
        temporary.replace(target)
        self._log_size("save_to_json")

    @classmethod
    def load_from_json(cls, file_path: Path) -> "CrawlQueue":
        """Load queue state from JSON for crawl resumption."""

        target = Path(file_path)
        state = json.loads(target.read_text(encoding="utf-8"))
        if state.get("version") != _QUEUE_FILE_VERSION:
            raise ValueError(f"unsupported queue file version: {state.get('version')}")
        items = state.get("items")
        if not isinstance(items, list) or not all(isinstance(item, str) for item in items):
            raise ValueError("queue file items must be a list of strings")

        queue = cls(items)
        queue._log_size("load_from_json")
        return queue

    @staticmethod
    def _validate_item(item: str) -> str:
        if not isinstance(item, str):
            raise TypeError("queue item must be a string")
        normalized = item.strip()
        if not normalized:
            raise ValueError("queue item cannot be empty")
        return normalized

    def _log_size(self, operation: str) -> None:
        logger.info("Queue operation=%s size=%s", operation, len(self._queue))
