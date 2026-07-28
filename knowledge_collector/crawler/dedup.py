"""URL canonicalization and content-hash duplicate detection.

Two independent layers of duplicate protection are provided:

1. ``canonicalize_url`` normalizes URL variants (tracking parameters,
   default ports, trailing slashes, ``www.`` prefixes) so equivalent URLs
   collapse to one canonical form before they ever reach the visited-URL
   database.
2. ``ContentHashStore`` fingerprints downloaded HTML with SHA-256 so pages
   reachable via different URLs (mirrors, redirected paths, session-id
   query strings that survive canonicalization) are still only saved once.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
from pathlib import Path
from urllib.parse import SplitResult, parse_qsl, urlencode, urlsplit, urlunsplit

from config.settings import settings


logger = logging.getLogger("knowledge_collector.crawler.dedup")

_TRACKING_PARAMETERS = frozenset(
    {"fbclid", "gclid", "mc_cid", "mc_eid", "ref", "source", "igshid"}
)
_STORE_VERSION = 1


def canonicalize_url(url: str) -> str | None:
    """Return a stable canonical form of ``url``, or ``None`` if invalid.

    Strips tracking query parameters, default ports, ``www.`` prefixes, and
    trailing slashes so equivalent URLs normalize to the same string.
    """

    if not isinstance(url, str) or not url.strip():
        return None
    parsed = urlsplit(url.strip())
    scheme = parsed.scheme.casefold()
    if scheme not in {"http", "https"} or not parsed.hostname:
        return None

    try:
        port = parsed.port
    except ValueError:
        return None

    hostname = parsed.hostname.casefold().removeprefix("www.")
    default_port = (scheme == "http" and port == 80) or (scheme == "https" and port == 443)
    netloc = hostname if port is None or default_port else f"{hostname}:{port}"

    path = parsed.path or "/"
    if len(path) > 1 and path.endswith("/"):
        path = path.rstrip("/")

    filtered_query = [
        (key, value)
        for key, value in parse_qsl(parsed.query, keep_blank_values=True)
        if not key.casefold().startswith("utm_") and key.casefold() not in _TRACKING_PARAMETERS
    ]
    normalized = SplitResult(
        scheme=scheme,
        netloc=netloc,
        path=path,
        query=urlencode(filtered_query, doseq=True),
        fragment="",
    )
    return urlunsplit(normalized)


def content_hash(content: str | bytes) -> str:
    """Return the SHA-256 hex digest of ``content``."""

    data = content.encode("utf-8") if isinstance(content, str) else content
    return hashlib.sha256(data).hexdigest()


class ContentHashStore:
    """Persist known content hashes so identical content is never saved twice."""

    def __init__(self, path: Path | None = None) -> None:
        self._path = path or settings.logs_directory / "content_hashes.json"
        self._hashes: dict[str, str] = {}
        self._load()

    def seen(self, digest: str) -> bool:
        """Return whether ``digest`` has already been recorded."""

        return digest in self._hashes

    def record(self, digest: str, url: str) -> bool:
        """Record ``digest`` as seen for ``url``.

        Returns ``True`` when the hash is newly recorded, ``False`` when it
        is already known (i.e. this content is a duplicate).
        """

        if digest in self._hashes:
            logger.info("Duplicate content detected: %s matches earlier %s", url, self._hashes[digest])
            return False
        self._hashes[digest] = url
        self._save()
        return True

    def _load(self) -> None:
        if not self._path.is_file():
            return
        try:
            payload = json.loads(self._path.read_text(encoding="utf-8"))
            if payload.get("version") == _STORE_VERSION:
                self._hashes = dict(payload.get("hashes", {}))
        except (json.JSONDecodeError, OSError, TypeError) as exc:
            logger.warning("Could not read content hash store at %s (%s); starting fresh", self._path, exc)

    def _save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"version": _STORE_VERSION, "hashes": self._hashes}
        temporary_path = self._path.with_suffix(f"{self._path.suffix}.tmp")
        with temporary_path.open("w", encoding="utf-8", newline="\n") as file:
            json.dump(payload, file, ensure_ascii=False, indent=2)
            file.flush()
            os.fsync(file.fileno())
        temporary_path.replace(self._path)
