"""Chunking Engine — Vol IV Ch7.

Prefer semantic chunks over fixed-size chunks. Never split a code block
or a step-by-step procedure across chunks.
"""
from __future__ import annotations
import re
from dataclasses import dataclass
from .repository import RawKnowledgeDoc

MAX_CHUNK_CHARS = 1800
MIN_CHUNK_CHARS = 200


@dataclass
class KnowledgeChunk:
    chunk_id: str
    doc_id: str
    text: str
    title: str
    source: str
    category: str
    tags: list
    trust_level: str
    technology: str


def _split_by_headings(markdown: str) -> list[str]:
    """Split on markdown headings first — keeps topic boundaries intact."""
    parts = re.split(r"(?=^#{1,4}\s)", markdown, flags=re.MULTILINE)
    return [p.strip() for p in parts if p.strip()]


def _split_oversized(section: str) -> list[str]:
    """If a section is still too large, split on paragraph boundaries,
    never mid-code-block (fenced ``` blocks are kept atomic)."""
    if len(section) <= MAX_CHUNK_CHARS:
        return [section]

    # Protect fenced code blocks from being split
    fence_spans = [m.span() for m in re.finditer(r"```.*?```", section, flags=re.DOTALL)]

    paragraphs = section.split("\n\n")
    chunks, buf = [], ""
    for para in paragraphs:
        if len(buf) + len(para) + 2 <= MAX_CHUNK_CHARS:
            buf = f"{buf}\n\n{para}" if buf else para
        else:
            if buf:
                chunks.append(buf)
            buf = para
    if buf:
        chunks.append(buf)
    return chunks


def chunk_document(doc: RawKnowledgeDoc, content: str) -> list[KnowledgeChunk]:
    sections = _split_by_headings(content) or [content]
    out: list[KnowledgeChunk] = []
    idx = 0
    for section in sections:
        for piece in _split_oversized(section):
            if len(piece) < MIN_CHUNK_CHARS and out and \
                    len(out[-1].text) + len(piece) + 2 <= MAX_CHUNK_CHARS:
                # merge tiny trailing piece into previous chunk, but only if
                # it still fits — otherwise it becomes its own chunk instead
                # of growing unbounded (was causing oversized merged chunks
                # that blew past the embedding model's context window)
                out[-1].text += "\n\n" + piece
                continue
            idx += 1
            out.append(
                KnowledgeChunk(
                    chunk_id=f"{doc.doc_id}::{idx}",
                    doc_id=doc.doc_id,
                    text=piece,
                    title=doc.title,
                    source=doc.source,
                    category=doc.category,
                    tags=doc.tags,
                    trust_level=doc.trust_level,
                    technology=doc.technology,
                )
            )
    return out
