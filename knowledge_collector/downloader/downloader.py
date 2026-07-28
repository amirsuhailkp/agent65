"""Reliable HTML downloading for knowledge sources.

This module deliberately stops at HTTP retrieval. Content parsing and cleaning
belong to downstream layers.
"""

import logging
import re
from typing import Final, NamedTuple
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from models.document import DownloadedDocument, RedirectHop


DEFAULT_TIMEOUT_SECONDS: Final[float] = 20.0
DEFAULT_USER_AGENT: Final[str] = "Agent-Cyber-Knowledge-Collector/0.1"
RETRYABLE_STATUS_CODES: Final[frozenset[int]] = frozenset({429, 500, 502, 503, 504})
DEFAULT_MAX_CLIENT_REDIRECTS: Final[int] = 5

logger = logging.getLogger("knowledge_collector.downloader")


class DownloaderError(RuntimeError):
    """Raised when an HTML resource cannot be downloaded."""


class RedirectResolutionError(DownloaderError):
    """Raised when a client-side redirect cannot be resolved safely."""


class NotModifiedError(DownloaderError):
    """Raised when a conditional request confirms content is unchanged (HTTP 304).

    Supports incremental crawling: callers that already hold a cached
    ``ETag``/``Last-Modified`` value can pass it to
    :meth:`Downloader.download_document` and skip re-processing entirely
    when the server confirms nothing changed.
    """


class _ClientRedirect(NamedTuple):
    destination: str | None
    mechanism: str


class Downloader:
    """Download HTML documents using a resilient, reusable HTTP session.

    Args:
        timeout: Per-request timeout in seconds.
        user_agent: Value sent in the ``User-Agent`` request header.
        max_retries: Number of retries for temporary failures.
        backoff_factor: Exponential retry backoff multiplier.
        session: Optional preconfigured session, primarily for dependency
            injection and testing. The caller retains ownership of it.
    """

    def __init__(
        self,
        *,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
        user_agent: str = DEFAULT_USER_AGENT,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
        max_client_redirects: int = DEFAULT_MAX_CLIENT_REDIRECTS,
        session: requests.Session | None = None,
    ) -> None:
        if timeout <= 0:
            raise ValueError("timeout must be greater than zero")
        if max_retries < 0:
            raise ValueError("max_retries cannot be negative")
        if backoff_factor < 0:
            raise ValueError("backoff_factor cannot be negative")
        if max_client_redirects < 0:
            raise ValueError("max_client_redirects cannot be negative")
        if not user_agent.strip():
            raise ValueError("user_agent cannot be empty")

        self._timeout = timeout
        self._max_client_redirects = max_client_redirects
        self._owns_session = session is None
        self._session = session or requests.Session()
        self._session.headers.update({"User-Agent": user_agent})

        if self._owns_session:
            self._configure_retries(max_retries, backoff_factor)

    def _configure_retries(self, max_retries: int, backoff_factor: float) -> None:
        retry_policy = Retry(
            total=max_retries,
            connect=max_retries,
            read=max_retries,
            status=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=RETRYABLE_STATUS_CODES,
            allowed_methods=frozenset({"GET"}),
            respect_retry_after_header=True,
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry_policy)
        self._session.mount("https://", adapter)
        self._session.mount("http://", adapter)

    def download(self, url: str) -> str:
        """Retrieve and return HTML only, for compatibility with existing callers."""

        return self.download_document(url).html

    def download_document(
        self,
        url: str,
        *,
        conditional_headers: dict[str, str] | None = None,
    ) -> DownloadedDocument:
        """Retrieve HTML and its final URL after HTTP/client-side redirects.

        HTTP redirects are followed by ``requests``. Meta refresh, JavaScript
        location, and redirect-only HTML pages are followed explicitly.

        Args:
            conditional_headers: Optional ``If-None-Match``/``If-Modified-Since``
                headers for incremental crawling. When the server responds
                ``304 Not Modified``, :class:`NotModifiedError` is raised
                instead of an empty document.
        """

        if not url.strip():
            raise ValueError("url cannot be empty")

        requested_url = url
        current_url = url
        seen_urls = {url}
        redirect_history: list[RedirectHop] = []

        for client_redirect_count in range(self._max_client_redirects + 1):
            logger.info("Requested URL: %s", current_url)
            request_headers = conditional_headers if current_url == requested_url else None
            response = self._request(current_url, headers=request_headers)
            if response.status_code == 304:
                logger.info("Not modified (304): %s", current_url)
                raise NotModifiedError(f"{current_url} has not changed since the last crawl")
            http_hops = _http_redirect_hops(response)
            redirect_history.extend(http_hops)
            for hop in http_hops:
                logger.info(
                    "HTTP redirect (%s): %s -> %s",
                    hop.status_code,
                    hop.source_url,
                    hop.destination_url,
                )

            logger.info(
                "HTTP response reached final URL: %s (status=%s, redirect_history=%s)",
                response.url,
                response.status_code,
                [f"{hop.mechanism}:{hop.source_url}->{hop.destination_url}" for hop in redirect_history],
            )
            client_redirect = _detect_client_redirect(response.text)
            if client_redirect is None:
                logger.info(
                    "Downloaded final article candidate: requested=%s final=%s status=%s bytes=%s",
                    requested_url,
                    response.url,
                    response.status_code,
                    len(response.content),
                )
                return DownloadedDocument(
                    requested_url=requested_url,
                    final_url=response.url,
                    html=response.text,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    redirect_history=tuple(redirect_history),
                    content_type=response.headers.get("Content-Type"),
                    encoding=response.encoding,
                )

            if client_redirect.destination is None:
                raise RedirectResolutionError(
                    f"Detected {client_redirect.mechanism} redirect page at {response.url}, "
                    "but it did not declare a destination"
                )
            if client_redirect_count == self._max_client_redirects:
                raise RedirectResolutionError(
                    f"Exceeded {self._max_client_redirects} client-side redirects while fetching {requested_url}"
                )

            destination_url = urljoin(response.url, client_redirect.destination)
            if destination_url in seen_urls:
                raise RedirectResolutionError(
                    f"Client-side redirect loop detected while fetching {requested_url}: {destination_url}"
                )
            seen_urls.add(destination_url)
            client_hop = RedirectHop(
                source_url=response.url,
                destination_url=destination_url,
                status_code=response.status_code,
                mechanism=client_redirect.mechanism,
            )
            redirect_history.append(client_hop)
            logger.info(
                "Resolving %s redirect: %s -> %s",
                client_redirect.mechanism,
                response.url,
                destination_url,
            )
            current_url = destination_url

        raise RedirectResolutionError(f"Unable to reach final page for {requested_url}")

    def _request(self, url: str, *, headers: dict[str, str] | None = None) -> requests.Response:
        try:
            extra_kwargs = {"headers": headers} if headers else {}
            response = self._session.get(
                url,
                timeout=self._timeout,
                allow_redirects=True,
                **extra_kwargs,
            )
            if response.status_code == 304:
                return response
            response.raise_for_status()
            return response
        except requests.HTTPError as exc:
            status_code = exc.response.status_code if exc.response is not None else "unknown"
            final_url = exc.response.url if exc.response is not None else url
            logger.warning("HTTP error: requested=%s final=%s status=%s", url, final_url, status_code)
            raise DownloaderError(f"HTTP {status_code} while reaching {final_url}") from exc
        except requests.RequestException as exc:
            logger.warning("Network error reaching %s: %s", url, exc)
            raise DownloaderError(f"Network error while reaching {url}") from exc

    def close(self) -> None:
        """Close the internally-created HTTP session, if any."""

        if self._owns_session:
            self._session.close()

    def __enter__(self) -> "Downloader":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


def _http_redirect_hops(response: requests.Response) -> list[RedirectHop]:
    responses = [*response.history, response]
    return [
        RedirectHop(
            source_url=previous.url,
            destination_url=following.url,
            status_code=previous.status_code,
            mechanism="http",
        )
        for previous, following in zip(responses, responses[1:])
    ]


def _detect_client_redirect(html: str) -> _ClientRedirect | None:
    """Identify redirect-only HTML patterns and return a declared destination."""

    soup = BeautifulSoup(html, "html.parser")
    meta_refresh = soup.find("meta", attrs={"http-equiv": re.compile(r"^refresh$", re.IGNORECASE)})
    if meta_refresh is not None:
        content = str(meta_refresh.get("content", ""))
        match = re.search(r"(?:^|;)\s*url\s*=\s*['\"]?([^'\";]+)", content, re.IGNORECASE)
        return _ClientRedirect(match.group(1).strip() if match else None, "meta refresh")

    scripts = "\n".join(script.get_text(" ") for script in soup.find_all("script"))
    javascript_redirect = re.search(
        r"(?:window\.)?location(?:\.href)?\s*=\s*['\"]([^'\"]+)['\"]|"
        r"window\.location\.(?:assign|replace)\(\s*['\"]([^'\"]+)['\"]\s*\)",
        scripts,
        re.IGNORECASE,
    )
    if javascript_redirect:
        return _ClientRedirect(next(value for value in javascript_redirect.groups() if value), "JavaScript location")
    if re.search(r"(?:window\.)?location(?:\.href)?\s*=|window\.location\.(?:assign|replace)", scripts, re.IGNORECASE):
        return _ClientRedirect(None, "JavaScript location")

    page_text = " ".join(soup.stripped_strings)
    if re.fullmatch(r"redirecting(?:\s+to)?[.\s…]*", page_text, re.IGNORECASE):
        link = soup.find("a", href=True)
        return _ClientRedirect(str(link["href"]) if link else None, "redirecting page")
    return None
