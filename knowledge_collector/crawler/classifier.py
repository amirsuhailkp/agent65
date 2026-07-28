"""Generic page classification for crawl traversal.

The crawler previously assumed every page was an article, which broke on
listing/hub pages such as ``https://portswigger.net/research``. This module
classifies a downloaded page as one of five generic types using structural
and URL signals only (link density, heading density, breadcrumbs, navigation
ratio, ``<article>``/``<main>`` presence, and URL shape). No site is ever
named in this logic, so the same classifier works for OWASP, PortSwigger,
HackTricks, ProjectDiscovery, Assetnote, and any future source described in
``config/sources.yaml``.

Downstream routing (crawler/page_processor.py) decides what to do with each
type:
    - LISTING / INDEX  -> queue child links, never save as an article.
    - ARTICLE / DOCUMENTATION -> extract, convert, and save.
    - UNKNOWN -> skip safely.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from urllib.parse import urlsplit

from bs4 import BeautifulSoup


class PageType(str, Enum):
    """Generic page categories used to route crawl handling."""

    LISTING = "listing"
    ARTICLE = "article"
    DOCUMENTATION = "documentation"
    INDEX = "index"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class PageClassification:
    """Outcome of classifying one page, with the signals that produced it."""

    page_type: PageType
    confidence: float
    scores: dict[str, float] = field(default_factory=dict)
    signals: dict[str, float | int | bool] = field(default_factory=dict)


# URL-shape hints are advisory signals only; they never solely decide the
# outcome, so sources that don't follow these conventions still classify
# correctly from structural signals alone.
_LISTING_URL_HINTS = re.compile(
    r"/(research|blog|news|articles|posts|insights|advisories|category|categories|tag|tags|archive)s?/?$",
    re.IGNORECASE,
)
_INDEX_URL_HINTS = re.compile(
    r"(?:^/$|/index/?$|/docs/?$|/documentation/?$|/sitemap/?$|/home/?$)",
    re.IGNORECASE,
)
_DOC_URL_HINTS = re.compile(
    r"/(docs?|documentation|guide|guides|manual|wiki|reference|handbook)(?:/|$)",
    re.IGNORECASE,
)

_MINIMUM_CONFIDENCE = 0.32
_HEADING_TAGS = ("h1", "h2", "h3", "h4", "h5", "h6")


class PageClassifier:
    """Classify one downloaded HTML page into a generic page type."""

    def classify(self, html: str, url: str) -> PageClassification:
        """Return the most likely page type for ``html`` fetched from ``url``."""

        if not isinstance(html, str):
            raise TypeError("html must be a string")
        if not isinstance(url, str) or not url.strip():
            raise ValueError("url must be a non-empty string")

        soup = BeautifulSoup(html, "html.parser")
        signals = self._collect_signals(soup, url)
        scores = self._score(signals)

        best_type = max(scores, key=lambda key: scores[key])
        confidence = scores[best_type]
        if confidence < _MINIMUM_CONFIDENCE:
            best_type = PageType.UNKNOWN.value
            confidence = scores[PageType.UNKNOWN.value]

        return PageClassification(
            page_type=PageType(best_type),
            confidence=round(confidence, 4),
            scores={key: round(value, 4) for key, value in scores.items()},
            signals=signals,
        )

    def _collect_signals(self, soup: BeautifulSoup, url: str) -> dict[str, float | int | bool]:
        path = urlsplit(url).path or "/"
        text = " ".join(soup.stripped_strings)
        text_length = max(len(text), 1)

        all_links = soup.select("a[href]")
        nav_links = soup.select(
            "nav a[href], header a[href], footer a[href], "
            "[role='navigation'] a[href], aside a[href]"
        )
        headings = soup.find_all(_HEADING_TAGS)
        paragraphs = soup.find_all("p")
        code_blocks = soup.find_all(["pre", "code"])
        breadcrumbs = soup.select(
            "[class*=breadcrumb i], [aria-label*=breadcrumb i], nav[aria-label*=breadcrumb i]"
        )
        has_article_tag = soup.find(["article", "main"]) is not None or soup.find(
            attrs={"role": "main"}
        ) is not None
        sidebar_nav = soup.select("[class*=sidebar i] a[href], [class*=toc i] a[href], aside a[href]")

        total_links = len(all_links)
        link_density = total_links / (text_length / 100)
        nav_density = (len(nav_links) / total_links) if total_links else 0.0
        heading_density = len(headings) / max(text_length / 500, 0.5)
        similar_card_links = _count_repeated_link_patterns(all_links)
        card_ratio = (similar_card_links / total_links) if total_links else 0.0

        return {
            "path": path,
            "text_length": text_length,
            "total_links": total_links,
            "link_density": round(link_density, 4),
            "nav_density": round(nav_density, 4),
            "heading_density": round(heading_density, 4),
            "paragraph_count": len(paragraphs),
            "code_block_count": len(code_blocks),
            "breadcrumb_count": len(breadcrumbs),
            "sidebar_link_count": len(sidebar_nav),
            "has_article_structure": has_article_tag,
            "card_link_ratio": round(card_ratio, 4),
            "matches_listing_url": bool(_LISTING_URL_HINTS.search(path)),
            "matches_index_url": bool(_INDEX_URL_HINTS.search(path)),
            "matches_doc_url": bool(_DOC_URL_HINTS.search(path)),
        }

    def _score(self, signals: dict[str, float | int | bool]) -> dict[str, float]:
        text_length = float(signals["text_length"])
        total_links = float(signals["total_links"])
        link_density = float(signals["link_density"])
        nav_density = float(signals["nav_density"])
        heading_density = float(signals["heading_density"])
        paragraphs = float(signals["paragraph_count"])
        code_blocks = float(signals["code_block_count"])
        breadcrumbs = float(signals["breadcrumb_count"])
        sidebar_links = float(signals["sidebar_link_count"])
        has_article = bool(signals["has_article_structure"])
        card_ratio = float(signals["card_link_ratio"])

        prose_density = min(1.0, paragraphs / max(text_length / 400, 1))

        listing_score = _clamp(
            0.35 * min(1.0, link_density / 8)
            + 0.25 * card_ratio
            + 0.15 * (1 - prose_density)
            + 0.15 * (0.5 if signals["matches_listing_url"] else 0.0)
            + 0.10 * min(1.0, total_links / 30)
        )

        index_score = _clamp(
            0.30 * (0.6 if signals["matches_index_url"] else 0.0)
            + 0.25 * min(1.0, link_density / 10)
            + 0.20 * min(1.0, sidebar_links / 15)
            + 0.15 * (1 - prose_density)
            + 0.10 * (1.0 if breadcrumbs and paragraphs < 2 else 0.0)
        )

        documentation_score = _clamp(
            0.30 * (1.0 if has_article else 0.3)
            + 0.20 * (0.6 if signals["matches_doc_url"] else 0.0)
            + 0.15 * min(1.0, breadcrumbs / 2)
            + 0.15 * min(1.0, sidebar_links / 10)
            + 0.10 * min(1.0, code_blocks / 3)
            + 0.10 * min(1.0, heading_density / 4)
        )

        article_score = _clamp(
            0.35 * (1.0 if has_article else 0.4)
            + 0.30 * prose_density
            + 0.15 * min(1.0, paragraphs / 6)
            + 0.10 * (1 - nav_density)
            + 0.10 * (1 - min(1.0, link_density / 12))
        )

        unknown_score = _clamp(
            0.6 if text_length < 120 and total_links < 5 else 0.05
        )

        return {
            PageType.LISTING.value: listing_score,
            PageType.INDEX.value: index_score,
            PageType.DOCUMENTATION.value: documentation_score,
            PageType.ARTICLE.value: article_score,
            PageType.UNKNOWN.value: unknown_score,
        }


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def _count_repeated_link_patterns(links: list) -> int:
    """Count links that share a parent-tag pattern, a signal of card grids."""

    parent_tag_counts: dict[str, int] = {}
    for link in links:
        parent = link.parent
        key = f"{parent.name if parent else ''}:{'/'.join(sorted(parent.get('class', []))) if parent else ''}"
        parent_tag_counts[key] = parent_tag_counts.get(key, 0) + 1
    return sum(count for count in parent_tag_counts.values() if count >= 3)
