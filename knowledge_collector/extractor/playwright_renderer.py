"""Optional JavaScript-rendered HTML retrieval using Playwright."""

import importlib.util
import logging
from typing import Final


logger = logging.getLogger("knowledge_collector.extractor.playwright")

DEFAULT_NAVIGATION_TIMEOUT_MS: Final[int] = 30_000


class BrowserRenderError(RuntimeError):
    """Raised when browser-based rendering cannot produce HTML."""


def is_playwright_available() -> bool:
    """Return whether the ``playwright`` package is importable in this environment.

    Used to log a one-time warning and continue crawling without JavaScript
    rendering, rather than failing the crawl, when Playwright is absent.
    """

    return importlib.util.find_spec("playwright") is not None


class PlaywrightRenderer:
    """Render modern JavaScript-heavy pages and return final HTML."""

    def __init__(self, *, timeout_ms: int = DEFAULT_NAVIGATION_TIMEOUT_MS) -> None:
        if timeout_ms < 1:
            raise ValueError("timeout_ms must be positive")
        self._timeout_ms = timeout_ms

    def render(self, url: str) -> str:
        """Load one URL in a headless browser and return rendered HTML."""

        if not isinstance(url, str) or not url.strip():
            raise ValueError("url must be a non-empty string")

        try:
            from playwright.sync_api import Error as PlaywrightError
            from playwright.sync_api import sync_playwright
        except ImportError as exc:
            raise BrowserRenderError(
                "Playwright fallback is unavailable because playwright is not installed"
            ) from exc

        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()
                page.goto(url, wait_until="networkidle", timeout=self._timeout_ms)
                html = page.content()
                context.close()
                browser.close()
        except PlaywrightError as exc:
            raise BrowserRenderError(f"Playwright failed to render {url}: {exc}") from exc

        if not html.strip():
            raise BrowserRenderError(f"Playwright returned empty HTML for {url}")
        logger.info("Rendered HTML with Playwright for %s (html_chars=%s)", url, len(html))
        return html