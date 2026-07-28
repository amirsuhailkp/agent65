"""Stable naming helpers for stored knowledge artifacts."""

from __future__ import annotations

import hashlib
import re
from urllib.parse import urlsplit


def build_artifact_filenames(source_name: str, url: str) -> tuple[str, str]:
    """Derive portable, collision-resistant artifact names for a source URL."""

    parsed = urlsplit(url)
    slug_source = f"{parsed.hostname or ''}-{parsed.path.strip('/') or 'index'}"
    slug = re.sub(r"[^a-z0-9]+", "-", slug_source.casefold()).strip("-")
    slug = slug[:120] or "page"
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:12]
    stem = f"{source_name}-{slug}-{digest}"
    return f"{stem}.html", f"{stem}.md"
