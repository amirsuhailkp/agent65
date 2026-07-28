"""Domain-scoped filtering for crawler candidate URLs."""

import logging
from collections.abc import Iterable
from urllib.parse import SplitResult, urlsplit, urlunsplit


logger = logging.getLogger("knowledge_collector.crawler.domain_filter")

_NON_HTML_EXTENSIONS = frozenset(
    {
        ".pdf",
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".svg",
        ".zip",
        ".rar",
        ".7z",
        ".doc",
        ".docx",
        ".ppt",
        ".pptx",
        ".exe",
        ".iso",
    }
)


class DomainFilter:
    """Filter candidate URLs to same-website, likely-HTML pages."""

    def filter_same_website_urls(
        self,
        *,
        current_domain: str,
        candidate_urls: Iterable[str],
    ) -> list[str]:
        """Return only same-website candidate URLs that look like HTML pages."""

        base_domain = _normalize_domain(current_domain)
        if base_domain is None:
            raise ValueError("current_domain must be a valid domain or HTTP(S) URL")

        candidates = list(candidate_urls)
        accepted: list[str] = []
        seen: set[str] = set()

        for candidate in candidates:
            normalized_url = _normalize_candidate_url(candidate)
            if normalized_url is None:
                continue
            if normalized_url in seen:
                continue

            host = urlsplit(normalized_url).hostname
            if host is None:
                continue
            normalized_host = _strip_www(host.casefold())
            if normalized_host != base_domain and not normalized_host.endswith(f".{base_domain}"):
                continue
            if _has_non_html_extension(normalized_url):
                continue

            seen.add(normalized_url)
            accepted.append(normalized_url)

        logger.info(
            "Domain filter accepted %s of %s candidates for domain %s",
            len(accepted),
            len(candidates),
            base_domain,
        )
        return accepted


def _normalize_domain(value: str) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    parsed = urlsplit(text if "://" in text else f"https://{text}")
    host = parsed.hostname
    if not host:
        return None
    return _strip_www(host.casefold())


def _normalize_candidate_url(url: str) -> str | None:
    if not isinstance(url, str) or not url.strip():
        return None
    parsed = urlsplit(url.strip())
    scheme = parsed.scheme.casefold()
    if scheme not in {"http", "https"}:
        return None
    host = parsed.hostname
    if not host:
        return None

    try:
        port = parsed.port
    except ValueError:
        return None

    hostname = _strip_www(host.casefold())
    default_port = (scheme == "http" and port == 80) or (scheme == "https" and port == 443)
    netloc = hostname if port is None or default_port else f"{hostname}:{port}"
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


def _has_non_html_extension(url: str) -> bool:
    path = urlsplit(url).path.casefold()
    for extension in _NON_HTML_EXTENSIONS:
        if path.endswith(extension):
            return True
    return False


def _strip_www(hostname: str) -> str:
    return hostname.removeprefix("www.")
