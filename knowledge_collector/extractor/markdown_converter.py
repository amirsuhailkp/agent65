"""Conversion of cleaned article HTML into Markdown."""

import re

from bs4 import BeautifulSoup, Tag
from markdownify import markdownify


_PRUNABLE_TAGS = frozenset(
    {
        "article",
        "div",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "li",
        "p",
        "section",
        "td",
        "th",
    }
)
_MEANINGFUL_EMPTY_CONTENT_TAGS = frozenset({"audio", "img", "svg", "video"})


def remove_empty_elements(html: str) -> str:
    """Remove empty article elements while preserving embedded media.

    Iterating from the leaves upward also removes sections whose only children
    are empty elements. This is intentionally performed before Markdown
    rendering so empty headings and list items cannot produce invalid output.
    """

    soup = BeautifulSoup(html, "html.parser")
    for element in reversed(list(soup.find_all(_PRUNABLE_TAGS))):
        if not element.get_text(strip=True) and not _contains_media(element):
            element.decompose()
    return str(soup)


def _contains_media(element: Tag) -> bool:
    return element.find(_MEANINGFUL_EMPTY_CONTENT_TAGS) is not None


def _code_language(element: Tag) -> str | None:
    """Return the fenced-code language declared through common CSS classes."""

    candidates = [element]
    if code_child := element.find("code"):
        candidates.append(code_child)

    for candidate in candidates:
        for class_name in candidate.get("class", []):
            match = re.match(
                r"(?:language|lang)-([a-z0-9_+-]+)$",
                class_name,
                re.IGNORECASE,
            )
            if match:
                return match.group(1)
    return None


def _normalise_markdown(markdown: str) -> str:
    """Return a stable document boundary without changing code-block content."""

    return markdown.strip() + "\n" if markdown.strip() else ""


class MarkdownConverter:
    """Convert cleaned HTML fragments into portable, GitHub-flavoured Markdown."""

    def convert(self, cleaned_html: str) -> str:
        """Convert cleaned HTML while preserving core article structures.

        Headings, lists, tables, fenced code blocks, links, and image markup are
        rendered by ``markdownify``. Empty sections are pruned before conversion.
        """

        if not isinstance(cleaned_html, str):
            raise TypeError("cleaned_html must be a string")
        if not cleaned_html.strip():
            return ""

        normalized_html = remove_empty_elements(cleaned_html)
        has_text = bool(BeautifulSoup(normalized_html, "html.parser").get_text(strip=True))
        if not has_text and not _has_media(normalized_html):
            return ""

        markdown = markdownify(
            normalized_html,
            heading_style="ATX",
            bullets="-",
            code_language_callback=_code_language,
            table_infer_header=True,
        )
        return _normalise_markdown(markdown)


def _has_media(html: str) -> bool:
    soup = BeautifulSoup(html, "html.parser")
    return soup.find(_MEANINGFUL_EMPTY_CONTENT_TAGS) is not None
