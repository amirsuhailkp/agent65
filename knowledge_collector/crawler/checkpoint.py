"""Atomic checkpoint storage for resumable crawler state."""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


_CHECKPOINT_VERSION = 1


@dataclass(frozen=True, slots=True)
class CheckpointQueueItem:
    """One pending crawl target persisted in FIFO order."""

    url: str
    depth: int


@dataclass(frozen=True, slots=True)
class CrawlCheckpointState:
    """All state required to resume a crawl without repeating completed work."""

    start_url: str
    queue: tuple[CheckpointQueueItem, ...]
    visited_urls: tuple[str, ...]
    statistics: dict[str, Any]
    current_depth: int | None
    current_url: str | None


class CrawlCheckpoint:
    """Persist and restore crawler state using atomic replace semantics."""

    def __init__(self, path: Path) -> None:
        self.path = Path(path)

    def exists(self) -> bool:
        """Return whether a saved checkpoint is available."""

        return self.path.is_file()

    def save(self, state: CrawlCheckpointState) -> None:
        """Atomically save a complete crawl snapshot."""

        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "version": _CHECKPOINT_VERSION,
            "start_url": state.start_url,
            "queue": [asdict(item) for item in state.queue],
            "visited_urls": sorted(state.visited_urls),
            "statistics": state.statistics,
            "current_depth": state.current_depth,
            "current_url": state.current_url,
        }
        temporary_path = self.path.with_suffix(f"{self.path.suffix}.tmp")
        with temporary_path.open("w", encoding="utf-8", newline="\n") as checkpoint_file:
            json.dump(payload, checkpoint_file, ensure_ascii=False, indent=2)
            checkpoint_file.flush()
            os.fsync(checkpoint_file.fileno())
        temporary_path.replace(self.path)

    def load(self, start_url: str) -> CrawlCheckpointState:
        """Load and validate the checkpoint for ``start_url``."""

        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
            if payload.get("version") != _CHECKPOINT_VERSION:
                raise ValueError("unsupported checkpoint version")
            if payload.get("start_url") != start_url:
                raise ValueError("checkpoint does not match this start URL")
            queue = tuple(CheckpointQueueItem(**item) for item in payload["queue"])
            if any(not item.url or item.depth < 0 for item in queue):
                raise ValueError("checkpoint queue contains invalid items")
            visited_urls = tuple(payload["visited_urls"])
            if not all(isinstance(url, str) and url for url in visited_urls):
                raise ValueError("checkpoint visited URLs are invalid")
            statistics = payload["statistics"]
            if not isinstance(statistics, dict):
                raise ValueError("checkpoint statistics are invalid")
            current_depth = payload.get("current_depth")
            current_url = payload.get("current_url")
            if current_depth is not None and (not isinstance(current_depth, int) or current_depth < 0):
                raise ValueError("checkpoint current depth is invalid")
            if current_url is not None and (not isinstance(current_url, str) or not current_url):
                raise ValueError("checkpoint current URL is invalid")
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"invalid crawl checkpoint: {self.path}") from exc

        return CrawlCheckpointState(
            start_url=start_url,
            queue=queue,
            visited_urls=visited_urls,
            statistics=statistics,
            current_depth=current_depth,
            current_url=current_url,
        )

    def clear(self) -> None:
        """Remove a checkpoint after a crawl completes successfully."""

        if self.path.is_file():
            self.path.unlink()
