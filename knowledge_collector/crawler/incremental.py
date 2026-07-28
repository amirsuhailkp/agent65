"""Per-URL crawl metadata for incremental (changed-only) recrawls.

Future crawls of the same source should download only new or changed pages.
This module records, per URL, the content hash, ``Last-Modified``, ``ETag``,
crawl timestamp, and HTTP status observed on the most recent successful
fetch. Callers (see ``collectors/generic.py``) use ``has_changed`` to decide
whether a page needs to be re-downloaded and re-processed at all.
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

from config.settings import settings


logger = logging.getLogger("knowledge_collector.crawler.incremental")

_STORE_VERSION = 1


@dataclass(frozen=True, slots=True)
class PageRecord:
    """Fetch metadata recorded for one URL after a successful collection."""

    url: str
    sha256: str
    last_modified: str | None
    etag: str | None
    crawl_timestamp: str
    http_status: int


class PageMetadataStore:
    """Track per-URL fetch metadata to support incremental, changed-only crawls."""

    def __init__(self, path: Path | None = None) -> None:
        self._path = path or settings.logs_directory / "page_metadata.json"
        self._records: dict[str, dict[str, object]] = {}
        self._load()

    def get(self, url: str) -> PageRecord | None:
        """Return the stored record for ``url``, or ``None`` if never seen."""

        raw = self._records.get(url)
        return PageRecord(**raw) if raw else None  # type: ignore[arg-type]

    def has_changed(
        self,
        url: str,
        *,
        sha256: str | None = None,
        etag: str | None = None,
        last_modified: str | None = None,
    ) -> bool:
        """Return whether ``url`` should be (re)collected.

        A page is considered unchanged, and therefore skippable, only when at
        least one strong identity signal (ETag, Last-Modified, or content
        hash) matches the previous crawl. Unknown pages always need collection.
        """

        existing = self.get(url)
        if existing is None:
            return True
        if etag and existing.etag and etag == existing.etag:
            return False
        if last_modified and existing.last_modified and last_modified == existing.last_modified:
            return False
        if sha256 and existing.sha256 and sha256 == existing.sha256:
            return False
        return True

    def record(self, record: PageRecord) -> None:
        """Persist ``record`` as the latest known state for its URL."""

        self._records[record.url] = asdict(record)
        self._save()

    def _load(self) -> None:
        if not self._path.is_file():
            return
        try:
            payload = json.loads(self._path.read_text(encoding="utf-8"))
            if payload.get("version") == _STORE_VERSION:
                self._records = dict(payload.get("records", {}))
        except (json.JSONDecodeError, OSError, TypeError) as exc:
            logger.warning("Could not read page metadata store at %s (%s); starting fresh", self._path, exc)

    def _save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"version": _STORE_VERSION, "records": self._records}
        temporary_path = self._path.with_suffix(f"{self._path.suffix}.tmp")
        with temporary_path.open("w", encoding="utf-8", newline="\n") as file:
            json.dump(payload, file, ensure_ascii=False, indent=2)
            file.flush()
            os.fsync(file.fileno())
        temporary_path.replace(self._path)


def utc_now_iso() -> str:
    """Return the current UTC time as an ISO-8601 string with a ``Z`` suffix."""

    return datetime.now(UTC).isoformat().replace("+00:00", "Z")
