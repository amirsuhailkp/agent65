"""Fence-aware cleanup for article Markdown."""

import logging
import re
from dataclasses import dataclass


logger = logging.getLogger("knowledge_collector.cleaner")

_FENCE_START = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
_BASE64_MARKDOWN_IMAGE = re.compile(r"!\[[^]]*\]\(\s*data:image/.*?\)", re.IGNORECASE | re.DOTALL)
_BASE64_HTML_IMAGE = re.compile(
    r"<img\b[^>]*\bsrc\s*=\s*(['\"])data:image/.*?\1[^>]*>",
    re.IGNORECASE | re.DOTALL,
)
_HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
_SCRIPT_BLOCK = re.compile(r"<script\b[^>]*>.*?</script\s*>", re.IGNORECASE | re.DOTALL)
_JAVASCRIPT_LINK = re.compile(r"!?\[[^]]*\]\(\s*javascript:[^\r\n]*\)", re.IGNORECASE)
_JAVASCRIPT_LINE = re.compile(
    r"^\s*(?:javascript:|<script\b|</script\s*>|(?:window|document)\.[\w.]+\s*\()",
    re.IGNORECASE,
)
_HEADING = re.compile(r"^(\s{0,3})(#{1,6})\s*(.*?)\s*#*\s*$")
_MARKDOWN_LINK = re.compile(r"\[([^]]+)\]\([^)]*\)")
_NAVIGATION_LABELS = frozenset(
    {
        "back",
        "contents",
        "home",
        "index",
        "menu",
        "navigation",
        "next",
        "previous",
        "up",
    }
)
_DONATION_LABELS = re.compile(
    r"\b(?:buy me a coffee|donate|donation|sponsor|support (?:us|this project))\b",
    re.IGNORECASE,
)
_EDIT_LABELS = re.compile(r"\b(?:edit (?:this )?page|edit on github|improve this page)\b", re.IGNORECASE)
_COOKIE_NOTICE = re.compile(
    r"\b(?:cookie settings|cookie notice|cookies? (?:policy|preferences)|"
    r"we use cookies?|accept cookies?|manage cookies?)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True, slots=True)
class _Segment:
    is_code: bool
    content: str


class MarkdownCleaner:
    """Remove common website boilerplate while retaining meaningful Markdown."""

    def clean(self, markdown: str) -> str:
        """Return normalized Markdown, leaving fenced code blocks byte-for-byte intact."""

        if not isinstance(markdown, str):
            raise TypeError("markdown must be a string")
        if not markdown.strip():
            return ""

        segments = _split_fenced_blocks(markdown)
        cleaned_segments = [
            segment.content if segment.is_code else self._clean_prose(segment.content)
            for segment in segments
        ]
        cleaned = _collapse_blank_lines("".join(cleaned_segments)).strip("\n")
        result = f"{cleaned}\n" if cleaned else ""
        logger.info(
            "Cleaned Markdown (%s characters to %s characters; %s fenced code blocks preserved)",
            len(markdown),
            len(result),
            sum(segment.is_code for segment in segments),
        )
        return result

    def _clean_prose(self, prose: str) -> str:
        prose = _BASE64_MARKDOWN_IMAGE.sub("", prose)
        prose = _BASE64_HTML_IMAGE.sub("", prose)
        prose = _HTML_COMMENT.sub("", prose)
        prose = _SCRIPT_BLOCK.sub("", prose)
        prose = _JAVASCRIPT_LINK.sub("", prose)

        output: list[str] = []
        for line in prose.splitlines():
            line = line.rstrip()
            if self._should_remove_line(line):
                continue
            output.append(_normalise_heading(line))
        return "\n".join(output)

    @staticmethod
    def _should_remove_line(line: str) -> bool:
        stripped = line.strip()
        if not stripped:
            return False
        if _JAVASCRIPT_LINE.match(stripped):
            return True
        if _COOKIE_NOTICE.search(stripped):
            return True
        if _DONATION_LABELS.search(stripped) or _EDIT_LABELS.search(stripped):
            return True
        return _is_navigation_line(stripped)


def _split_fenced_blocks(markdown: str) -> list[_Segment]:
    """Split Markdown while treating complete and unterminated fences as code."""

    segments: list[_Segment] = []
    prose_lines: list[str] = []
    code_lines: list[str] = []
    fence_character = ""
    fence_length = 0

    def append_prose() -> None:
        if prose_lines:
            segments.append(_Segment(is_code=False, content="".join(prose_lines)))
            prose_lines.clear()

    for line in markdown.splitlines(keepends=True):
        if not fence_character:
            match = _FENCE_START.match(line)
            if match:
                append_prose()
                marker = match.group(1)
                fence_character, fence_length = marker[0], len(marker)
                code_lines = [line]
            else:
                prose_lines.append(line)
            continue

        code_lines.append(line)
        closing = re.match(rf"^\s{{0,3}}{re.escape(fence_character)}{{{fence_length},}}\s*$", line)
        if closing:
            segments.append(_Segment(is_code=True, content="".join(code_lines)))
            code_lines = []
            fence_character = ""
            fence_length = 0

    if code_lines:
        segments.append(_Segment(is_code=True, content="".join(code_lines)))
    append_prose()
    return segments


def _normalise_heading(line: str) -> str:
    match = _HEADING.match(line)
    if not match:
        return line
    indentation, hashes, title = match.groups()
    title = title.strip()
    return f"{indentation}{hashes} {title}" if title else ""


def _is_navigation_line(line: str) -> bool:
    """Remove link-only rows only when every label is a navigation control."""

    labels = [label.strip().casefold() for label in _MARKDOWN_LINK.findall(line)]
    if not labels:
        return False
    remainder = _MARKDOWN_LINK.sub("", line).strip(" \t|-–—•»«‹›")
    return not remainder and all(label in _NAVIGATION_LABELS for label in labels)


def _collapse_blank_lines(markdown: str) -> str:
    """Retain at most one blank line between Markdown blocks."""

    return re.sub(r"\n[ \t]*\n(?:[ \t]*\n)+", "\n\n", markdown)
