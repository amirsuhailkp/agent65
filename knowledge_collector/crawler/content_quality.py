"""Quality scoring for extracted page content.

The extractor's fixed minimum-character gate (see
``extractor/html_extractor.py``) is preserved for backward compatibility
with existing tests and behavior. This module adds an additive, generic
quality *score* used by the new classification-aware crawl path
(``crawler/page_processor.ClassifyingCrawlPageProcessor``) to reject only
genuinely empty or unusable pages instead of applying one arbitrary
character threshold to every source.
"""

from __future__ import annotations

from dataclasses import dataclass

from bs4 import BeautifulSoup

_HEADING_TAGS = ("h1", "h2", "h3", "h4", "h5", "h6")
_NAV_SELECTOR = "nav, [role='navigation'], header, footer, aside"


@dataclass(frozen=True, slots=True)
class ContentQualityScore:
    """Composite quality signal for one page's HTML."""

    score: float
    meaningful_text_ratio: float
    paragraph_count: int
    heading_count: int
    code_block_count: int
    boilerplate_ratio: float
    navigation_ratio: float
    is_acceptable: bool


class ContentQualityScorer:
    """Score HTML content quality using several structural signals at once.

    A single fixed character count cannot tell a short-but-complete API
    reference page from genuine boilerplate. Instead this combines text
    density, structural richness (paragraphs/headings/code), and the
    proportion of navigation/boilerplate text into one 0-1 score.
    """

    def __init__(self, *, acceptance_threshold: float = 0.30, minimum_text_length: int = 40) -> None:
        if not 0.0 <= acceptance_threshold <= 1.0:
            raise ValueError("acceptance_threshold must be between 0 and 1")
        if minimum_text_length < 0:
            raise ValueError("minimum_text_length cannot be negative")
        self._threshold = acceptance_threshold
        self._minimum_text_length = minimum_text_length

    def score(self, html: str) -> ContentQualityScore:
        """Return a quality score for ``html``, a full page or article fragment."""

        if not isinstance(html, str):
            raise TypeError("html must be a string")

        soup = BeautifulSoup(html, "html.parser")
        text = " ".join(soup.stripped_strings)
        text_length = len(text)
        html_length = max(len(html), 1)

        paragraphs = soup.find_all("p")
        headings = soup.find_all(_HEADING_TAGS)
        code_blocks = soup.find_all(["pre", "code"])
        nav_elements = soup.select(_NAV_SELECTOR)
        nav_text_length = sum(len(" ".join(element.stripped_strings)) for element in nav_elements)

        navigation_ratio = min(1.0, nav_text_length / max(text_length, 1))
        meaningful_text_length = max(0, text_length - nav_text_length)
        meaningful_text_ratio = min(1.0, (meaningful_text_length / html_length) * 3)
        boilerplate_ratio = min(1.0, navigation_ratio + (0.1 if not paragraphs else 0.0))

        composite = _clamp(
            0.40 * meaningful_text_ratio
            + 0.20 * min(1.0, len(paragraphs) / 5)
            + 0.15 * min(1.0, len(headings) / 3)
            + 0.10 * min(1.0, len(code_blocks) / 2)
            + 0.15 * (1 - boilerplate_ratio)
        )

        is_acceptable = text_length >= self._minimum_text_length and composite >= self._threshold
        return ContentQualityScore(
            score=round(composite, 4),
            meaningful_text_ratio=round(meaningful_text_ratio, 4),
            paragraph_count=len(paragraphs),
            heading_count=len(headings),
            code_block_count=len(code_blocks),
            boilerplate_ratio=round(boilerplate_ratio, 4),
            navigation_ratio=round(navigation_ratio, 4),
            is_acceptable=is_acceptable,
        )


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))
