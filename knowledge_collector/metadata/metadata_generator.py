"""YAML front-matter generation for collected Markdown documents."""

import re
import logging
from collections import Counter
from collections.abc import Callable
from datetime import UTC, datetime
from urllib.parse import urlsplit

import yaml


logger = logging.getLogger("knowledge_collector.metadata")


_FRONT_MATTER = re.compile(r"\A---\s*\n.*?\n---\s*(?:\n|\Z)", re.DOTALL)
_ATX_HEADING = re.compile(r"^\s{0,3}#\s+(.+?)(?:\s+#+)?\s*$")
_SETEXT_UNDERLINE = re.compile(r"^\s*(?:=+|-+)\s*$")
_FENCE = re.compile(r"^\s{0,3}(?:`{3,}|~{3,})")
_MARKDOWN_LINK = re.compile(r"\[([^]]+)\]\([^)]*\)")
_MARKDOWN_NOISE = re.compile(r"[`*_>#|~\[\](){}]")
_WORD = re.compile(r"[a-zA-Z][a-zA-Z0-9_-]{2,}")
_STOP_WORDS = frozenset(
    {
        "about", "after", "also", "and", "are", "article", "because", "been", "being",
        "between", "but", "can", "code", "content", "could", "does", "for", "from", "has",
        "have", "here", "into", "its", "more", "most", "not", "one", "only", "other", "our",
        "out", "page", "should", "such", "than", "that", "the", "their", "there", "these",
        "this", "those", "through", "using", "was", "were", "what", "when", "which", "with",
        "would", "you", "your",
    }
)


class MetadataGenerator:
    """Prepend stable YAML front matter to cleaned Markdown content."""

    def __init__(self, clock: Callable[[], datetime] | None = None) -> None:
        self._clock = clock or (lambda: datetime.now(UTC))

    def generate(
        self,
        markdown: str,
        *,
        url: str,
        collector: str,
        category: str = "uncategorized",
        language: str = "unknown",
    ) -> str:
        """Return Markdown prefixed with generated YAML front matter.

        Args:
            markdown: Cleaned Markdown, with or without existing front matter.
            url: Canonical source URL for the collected document.
            collector: Stable name of the collector that obtained the document.
            category: Optional caller-provided classification.
            language: Optional ISO language code when known upstream.
        """

        if not isinstance(markdown, str):
            raise TypeError("markdown must be a string")
        if not collector.strip():
            raise ValueError("collector cannot be empty")
        if not category.strip():
            raise ValueError("category cannot be empty")
        if not language.strip():
            raise ValueError("language cannot be empty")

        source = _extract_domain(url)
        body = _strip_front_matter(markdown).strip()
        title = extract_title(body)
        metadata = {
            "title": title,
            "source": source,
            "url": url,
            "collector": collector.strip(),
            "category": category.strip(),
            "tags": generate_tags(body, category=category),
            "date_collected": _utc_timestamp(self._clock()),
            "language": language.strip(),
        }
        front_matter = yaml.safe_dump(
            metadata,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
        ).strip()
        document = (
            f"---\n{front_matter}\n---\n\n{body}\n"
            if body
            else f"---\n{front_matter}\n---\n"
        )
        logger.info(
            "Generated metadata for %s (collector=%s, tags=%s)",
            source,
            metadata["collector"],
            len(metadata["tags"]),
        )
        return document


def extract_title(markdown: str) -> str:
    """Extract the first Markdown heading, with a readable text fallback."""

    lines = markdown.splitlines()
    in_code_block = False
    for index, line in enumerate(lines):
        if _FENCE.match(line):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        if match := _ATX_HEADING.match(line):
            return _plain_text(match.group(1)) or "Untitled"
        if line.strip() and index + 1 < len(lines) and _SETEXT_UNDERLINE.match(lines[index + 1]):
            return _plain_text(line) or "Untitled"

    for line in lines:
        if line.strip() and not _FENCE.match(line):
            return _plain_text(line) or "Untitled"
    return "Untitled"


def generate_tags(markdown: str, *, category: str | None = None, limit: int = 5) -> list[str]:
    """Generate deterministic keyword tags from article text where possible."""

    if limit < 1:
        raise ValueError("limit must be greater than zero")

    title = extract_title(markdown)
    searchable_text = _remove_code_blocks(markdown)
    words = _tag_words(searchable_text)
    first_position: dict[str, int] = {}
    for position, word in enumerate(words):
        first_position.setdefault(word, position)

    counts = Counter(words)
    for word in _tag_words(title):
        counts[word] += 3

    tags: list[str] = []
    if category and category.strip().casefold() != "uncategorized":
        tags.extend(_tag_words(category))

    ranked_words = sorted(
        counts,
        key=lambda word: (-counts[word], first_position.get(word, -1), word),
    )
    for word in ranked_words:
        if word not in tags:
            tags.append(word)
        if len(tags) >= limit:
            break
    return tags[:limit]


def _extract_domain(url: str) -> str:
    parsed = urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("url must be an absolute HTTP(S) URL")
    return parsed.hostname.casefold().removeprefix("www.")


def _strip_front_matter(markdown: str) -> str:
    return _FRONT_MATTER.sub("", markdown, count=1)


def _utc_timestamp(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _remove_code_blocks(markdown: str) -> str:
    lines: list[str] = []
    in_code_block = False
    for line in markdown.splitlines():
        if _FENCE.match(line):
            in_code_block = not in_code_block
            continue
        if not in_code_block:
            lines.append(line)
    return "\n".join(lines)


def _tag_words(text: str) -> list[str]:
    text = _MARKDOWN_LINK.sub(r"\1", text)
    text = _MARKDOWN_NOISE.sub(" ", text)
    return [
        word.casefold()
        for word in _WORD.findall(text)
        if word.casefold() not in _STOP_WORDS
    ]


def _plain_text(markdown: str) -> str:
    text = _MARKDOWN_LINK.sub(r"\1", markdown)
    text = _MARKDOWN_NOISE.sub(" ", text)
    return " ".join(text.split())
