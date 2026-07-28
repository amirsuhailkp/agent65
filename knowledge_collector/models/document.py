"""Canonical model for a downloaded HTML document."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import NamedTuple


class RedirectHop(NamedTuple):
    """One HTTP or client-side redirect observed during retrieval."""

    source_url: str
    destination_url: str
    status_code: int
    mechanism: str


@dataclass(frozen=True, slots=True)
class DownloadedDocument:
    """A downloaded HTML document and its retrieval metadata."""

    requested_url: str
    final_url: str
    html: str
    status_code: int
    headers: dict[str, str] | None = None
    redirect_history: tuple[RedirectHop, ...] = ()
    content_type: str | None = None
    encoding: str | None = None
    downloaded_at: datetime = field(default_factory=lambda: datetime.now(UTC))
