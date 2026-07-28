"""Main-article extraction from raw HTML documents."""

import logging
import re
from collections.abc import Callable
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from typing import Final

import trafilatura
from bs4 import BeautifulSoup, Tag

from config.settings import settings


logger = logging.getLogger("knowledge_collector.extractor")

MINIMUM_ARTICLE_CHARACTERS: Final[int] = 500

_NOISE_SELECTORS: Final[tuple[str, ...]] = (
    "script",
    "style",
    "noscript",
    "template",
    "iframe",
    "nav",
    "aside",
    "footer",
    "[role='navigation']",
    "[role='banner']",
    "[role='contentinfo']",
    "[role='complementary']",
)
_NOISE_KEYWORDS: Final[frozenset[str]] = frozenset(
    {
        "ad",
        "ads",
        "advert",
        "advertisement",
        "banner",
        "cookie",
        "consent",
        "menu",
        "navigation",
        "newsletter",
        "popup",
        "sidebar",
        "sponsor",
    }
)


class ExtractionError(RuntimeError):
    """Base exception for invalid or suspicious extraction input/output."""

    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(reason)


class RedirectPageError(ExtractionError):
    """Raised when HTML is a client-side redirect page rather than an article."""


class ErrorPageError(ExtractionError):
    """Raised when HTML represents an HTTP/error landing page."""


class LoginPageError(ExtractionError):
    """Raised when HTML is an authentication page rather than an article."""


class CaptchaPageError(ExtractionError):
    """Raised when HTML requires CAPTCHA verification."""


class SuspiciousExtractionError(ExtractionError):
    """Raised when extracted content is too small to be a reliable article."""


class HTMLExtractor:
    """Extract clean, main-article HTML without downloading or parsing content.

    Trafilatura is the primary content detector. If it returns no usable HTML or
    raises an error, BeautifulSoup provides a deterministic structural fallback.
    The extraction callable is injectable to make failure scenarios testable.
    """

    def __init__(
        self,
        extractor: Callable[..., str | None] = trafilatura.extract,
        *,
        minimum_article_characters: int = MINIMUM_ARTICLE_CHARACTERS,
        debug_directory: Path | None = None,
    ) -> None:
        if minimum_article_characters < 1:
            raise ValueError("minimum_article_characters must be at least one")
        self._extractor = extractor
        self._minimum_article_characters = minimum_article_characters
        self._debug_directory = debug_directory or settings.logs_directory / "debug"

    def extract(self, raw_html: str) -> str:
        """Return the document's main article as clean HTML.

        Empty input is rejected. A failed primary extraction is normalised to a
        BeautifulSoup fallback rather than exposing library-specific failures.
        """

        if not isinstance(raw_html, str):
            raise TypeError("raw_html must be a string")
        if not raw_html.strip():
            raise ValueError("raw_html cannot be empty")

        self._validate_article_candidate(raw_html)
        logger.info("Starting article extraction (html_chars=%s)", len(raw_html))

        try:
            extracted_html = self._extractor(
                raw_html,
                output_format="html",
                include_comments=False,
                include_tables=True,
                include_links=True,
                include_formatting=True,
            )
        except Exception as exc:  # Third-party extractors can reject malformed HTML.
            logger.warning("Trafilatura extraction failed; using BeautifulSoup fallback: %s", exc)
        else:
            if extracted_html and extracted_html.strip():
                cleaned_html = self._remove_noise(extracted_html)
                if cleaned_html:
                    return self._validate_extracted_article(cleaned_html, raw_html, "Trafilatura")
            logger.info("Trafilatura returned no usable article; using BeautifulSoup fallback")

        fallback_html = self._extract_with_beautifulsoup(raw_html)
        return self._validate_extracted_article(fallback_html, raw_html, "BeautifulSoup fallback")

    def _validate_article_candidate(self, raw_html: str) -> None:
        """Reject known non-article pages before invoking an extractor."""

        soup = BeautifulSoup(raw_html, "html.parser")
        page_text = " ".join(soup.stripped_strings)
        normalized_text = " ".join(page_text.casefold().split())
        title = soup.title.get_text(" ", strip=True).casefold() if soup.title else ""

        if soup.find("meta", attrs={"http-equiv": re.compile(r"^refresh$", re.IGNORECASE)}):
            self._raise_non_article(RedirectPageError, "meta refresh redirect page", raw_html)
        scripts = "\n".join(script.get_text(" ") for script in soup.find_all("script"))
        if re.search(r"(?:window\.)?location(?:\.href)?\s*=|window\.location\.(?:assign|replace)", scripts, re.IGNORECASE):
            self._raise_non_article(RedirectPageError, "JavaScript window.location redirect page", raw_html)
        if re.fullmatch(r"redirecting(?:\s+to)?[.\s…]*", page_text, re.IGNORECASE):
            self._raise_non_article(RedirectPageError, "redirect-only page", raw_html)
        redirect_phrase = re.search(
            r"\b(?:redirect(?:ing|ed)?|forward(?:ing|ed)?|moved\s+(?:temporarily|permanently))\b",
            normalized_text,
            re.IGNORECASE,
        )
        has_article_structure = soup.find(["article", "main"]) is not None
        has_content_blocks = len(soup.find_all(["p", "h1", "h2", "li", "table", "pre"])) >= 2
        if redirect_phrase and len(page_text) < 500 and not has_article_structure and not has_content_blocks:
            self._raise_non_article(RedirectPageError, "text redirect landing page", raw_html)

        login_form = soup.find("form", attrs={"action": re.compile(r"(?:log ?in|sign ?in|auth)", re.IGNORECASE)})
        has_password_field = soup.find("input", attrs={"type": re.compile(r"^password$", re.IGNORECASE)}) is not None
        has_login_phrase = re.search(r"\b(?:log ?in|sign ?in|authenticate)\b", normalized_text) is not None
        if (has_password_field and has_login_phrase) or (login_form is not None and has_password_field):
            self._raise_non_article(LoginPageError, "login page with password form", raw_html)
        if (
            re.search(r"\b(?:captcha|recaptcha|hcaptcha|verify you are human|security check)\b", normalized_text)
            or soup.find(attrs={"class": re.compile(r"(?:captcha|recaptcha|hcaptcha)", re.IGNORECASE)})
            or soup.find(attrs={"id": re.compile(r"(?:captcha|recaptcha|hcaptcha)", re.IGNORECASE)})
            or soup.find("iframe", attrs={"src": re.compile(r"(?:captcha|recaptcha|hcaptcha)", re.IGNORECASE)})
        ):
            self._raise_non_article(CaptchaPageError, "CAPTCHA verification page", raw_html)
        if _is_error_page(title, normalized_text, soup):
            self._raise_non_article(ErrorPageError, "error page", raw_html)

        if not has_article_structure and (len(page_text) < 80 or not has_content_blocks):
            self._raise_non_article(ExtractionError, "HTML does not contain a recognizable article structure", raw_html)

    def _validate_extracted_article(self, article_html: str, raw_html: str, method: str) -> str:
        article_size = len(article_html)
        ratio = article_size / len(raw_html) if raw_html else 0.0
        logger.info(
            "Article extraction completed with %s (html_chars=%s, article_chars=%s, extraction_ratio=%.4f)",
            method,
            len(raw_html),
            article_size,
            ratio,
        )
        if article_size < self._minimum_article_characters:
            debug_path = self._save_debug_html(raw_html, reason="suspicious-extraction")
            reason = (
                f"extracted article is suspiciously small ({article_size} characters; "
                f"minimum is {self._minimum_article_characters}); raw HTML saved to {debug_path}"
            )
            logger.warning("%s", reason)
            raise SuspiciousExtractionError(reason)
        return article_html

    def _raise_non_article(
        self,
        exception_type: type[ExtractionError],
        reason: str,
        raw_html: str,
    ) -> None:
        debug_path = self._save_debug_html(raw_html, reason="non-article-page")
        message = f"{reason}; raw HTML saved to {debug_path}"
        logger.warning("Rejected HTML before extraction: %s", message)
        raise exception_type(message)

    def _save_debug_html(self, raw_html: str, *, reason: str) -> Path:
        """Persist raw suspicious HTML for diagnostics without overwriting files."""

        try:
            self._debug_directory.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ")
            digest = sha256(raw_html.encode("utf-8")).hexdigest()[:12]
            path = self._debug_directory / f"{reason}-{timestamp}-{digest}.html"
            path.write_text(raw_html, encoding="utf-8", newline="\n")
            logger.info("Saved debug HTML to %s", path)
            return path
        except OSError as exc:
            logger.warning("Failed to save debug HTML: %s", exc)
            return self._debug_directory / f"{reason}-unsaved.html"

    def _extract_with_beautifulsoup(self, raw_html: str) -> str:
        soup = BeautifulSoup(raw_html, "html.parser")
        self._remove_noise_tags(soup)

        article = soup.find("article")
        main = soup.find("main")
        role_main = soup.find(attrs={"role": "main"})
        content = article or main or role_main or soup.body or soup
        return self._normalise_fragment(content)

    def _remove_noise(self, html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        self._remove_noise_tags(soup)
        content = soup.body or soup
        return self._normalise_fragment(content)

    @staticmethod
    def _normalise_fragment(content: Tag | BeautifulSoup) -> str:
        """Return HTML while dropping whitespace-only nodes around the article."""

        for text_node in list(content.find_all(string=lambda value: not value.strip())):
            text_node.extract()
        return str(content).strip()

    @staticmethod
    def _attribute_has_noise_keyword(tag: Tag) -> bool:
        values = [tag.get("id", ""), *tag.get("class", [])]
        tokens = {
            token
            for value in values
            for token in re.split(r"[^a-z0-9]+", str(value).lower())
            if token
        }
        return bool(tokens & _NOISE_KEYWORDS)

    def _remove_noise_tags(self, soup: BeautifulSoup) -> None:
        for selector in _NOISE_SELECTORS:
            for tag in soup.select(selector):
                tag.decompose()

        for tag in list(soup.find_all(self._attribute_has_noise_keyword)):
            tag.decompose()


def _is_error_page(title: str, page_text: str, soup: BeautifulSoup) -> bool:
    """Identify high-confidence error documents without rejecting normal articles."""

    error_indicator = re.compile(
        r"\b(?:400|401|403|404|405|408|429|500|502|503|504)\b|"
        r"\b(?:access denied|page not found|not found|internal server error|service unavailable)\b",
        re.IGNORECASE,
    )
    heading = soup.find(["h1", "h2"])
    heading_text = heading.get_text(" ", strip=True).casefold() if heading else ""
    return bool(error_indicator.search(title) or error_indicator.search(heading_text)) and len(page_text) < 1_500
