"""HTML URL discovery and normalization utilities."""

import logging
from urllib.parse import SplitResult, urldefrag, urljoin, urlsplit, urlunsplit

from bs4 import BeautifulSoup


logger = logging.getLogger("knowledge_collector.crawler.url_discovery")

_IGNORED_SCHEMES = ("javascript:", "mailto:", "tel:", "data:")


class URLDiscoveryEngine:
    """Discover unique, normalized links from one HTML document."""

    def discover_urls(self, html: str, *, base_url: str) -> list[str]:
        """Return normalized, unique URLs discovered from ``<a href>`` tags.

        Args:
            html: Source HTML that contains hyperlink elements.
            base_url: Absolute reference URL used to resolve relative links.
        """

        if not isinstance(html, str):
            raise TypeError("html must be a string")
        if not isinstance(base_url, str) or not base_url.strip():
            raise ValueError("base_url must be a non-empty string")

        soup = BeautifulSoup(html, "html.parser")
        anchors = soup.select("a[href]")
        total_links_found = len(anchors)

        discovered: list[str] = []
        seen: set[str] = set()
        invalid_links = 0
        duplicate_links_removed = 0

        for anchor in anchors:
            raw_href = anchor.get("href")
            href = raw_href.strip() if isinstance(raw_href, str) else ""
            if not href:
                invalid_links += 1
                continue

            lowered = href.casefold()
            if lowered.startswith("#"):
                invalid_links += 1
                continue
            if lowered.startswith(_IGNORED_SCHEMES):
                invalid_links += 1
                continue

            resolved_url = urljoin(base_url, href)
            resolved_without_fragment, _ = urldefrag(resolved_url)
            normalized_url = _normalize_url(resolved_without_fragment)
            if normalized_url is None:
                invalid_links += 1
                continue

            if normalized_url in seen:
                duplicate_links_removed += 1
                continue

            seen.add(normalized_url)
            discovered.append(normalized_url)

        logger.info(
            "URL discovery stats (total_links=%s, valid_links=%s, invalid_links=%s, duplicates_removed=%s)",
            total_links_found,
            len(discovered),
            invalid_links,
            duplicate_links_removed,
        )
        return discovered


def _normalize_url(url: str) -> str | None:
    """Normalize absolute HTTP(S) URLs for stable deduplication."""

    parsed = urlsplit(url)
    scheme = parsed.scheme.casefold()
    if scheme not in {"http", "https"}:
        return None
    if not parsed.hostname:
        return None

    hostname = parsed.hostname.casefold()
    try:
        port = parsed.port
    except ValueError:
        return None

    is_default_port = (scheme == "http" and port == 80) or (scheme == "https" and port == 443)
    netloc = hostname if port is None or is_default_port else f"{hostname}:{port}"

    path = parsed.path or "/"
    if len(path) > 1 and path.endswith("/"):
        path = path.rstrip("/")

    normalized = SplitResult(
        scheme=scheme,
        netloc=netloc,
        path=path,
        query=parsed.query,
        fragment="",
    )
    return urlunsplit(normalized)
