"""Knowledge Repository — Vol IV Ch2, integration note.

This module NEVER crawls, scrapes, or downloads anything. That job belongs
entirely to the existing Knowledge Collector Framework (production-ready,
tested, do not touch).

Real output contract (confirmed against metadata/metadata_generator.py and
storage/filesystem.py): ONE markdown file per document, with YAML front
matter prepended by MetadataGenerator.generate() — no sidecar .meta.json.

    ---
    title: A01:2021 – Broken Access Control
    source: owasp.org
    url: https://owasp.org/Top10/2021/A01_2021-Broken_Access_Control/
    collector: owasp
    category: web-security
    tags: [web-security, access, control, ...]
    date_collected: '2026-07-25T14:25:13.353015Z'
    language: en
    ---

    <body markdown>

There is no `trust_level` or `technology` field in the collector's output —
those are Agent Cyber concepts (Vol IV Ch8 metadata design), so this layer
derives them rather than inventing collector behavior that doesn't exist.
"""
from __future__ import annotations
import re
import yaml
from pathlib import Path
from dataclasses import dataclass
from typing import Iterator
from ..logging_setup import get_logger

log = get_logger("knowledge.repository")

_FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z", re.DOTALL)

# Sources the spec (Vol I Ch9, Vol IV Ch5) names as trusted knowledge origins.
# Anything collected under these collector names is treated as verified;
# everything else stays unverified until a human promotes it.
_TRUSTED_COLLECTORS = {
    "owasp", "portswigger", "hacktricks", "payloadsallthethings",
    "cwe", "capec", "cve", "cisa-kev",
}


@dataclass
class RawKnowledgeDoc:
    doc_id: str
    title: str
    source: str
    category: str
    tags: list
    trust_level: str
    technology: str
    file_path: Path | None = None  # absolute path to the source .md, for hashing/audit


class KnowledgeRepository:
    """Reads the collector's `processed/` directory directly — single .md
    files with embedded YAML front matter, exactly as MetadataGenerator
    and FilesystemStorage produce them."""

    def __init__(self, processed_output_path: str):
        self.root = Path(processed_output_path)
        if not self.root.exists():
            log.warning(
                f"Knowledge collector output path not found: {self.root}. "
                f"Check config.yaml knowledge_collector.processed_output_path."
            )

    def _parse_front_matter(self, md_file: Path) -> tuple[dict, str] | None:
        raw = md_file.read_text(encoding="utf-8")
        m = _FRONT_MATTER.match(raw)
        if not m:
            log.warning(f"No YAML front matter found in {md_file.name}, skipping")
            return None
        try:
            meta = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError as e:
            log.warning(f"Malformed front matter in {md_file.name}: {e}")
            return None
        body = m.group(2)
        return meta, body

    def iter_documents(self) -> Iterator[tuple[RawKnowledgeDoc, str]]:
        """Yields (RawKnowledgeDoc, body_markdown) pairs."""
        if not self.root.exists():
            return
        for md_file in sorted(self.root.glob("*.md")):
            parsed = self._parse_front_matter(md_file)
            if not parsed:
                continue
            meta, body = parsed
            if not body.strip():
                log.warning(f"Empty body after front matter in {md_file.name}, skipping")
                continue

            collector_name = str(meta.get("collector", "")).strip().lower()
            trust_level = "verified" if collector_name in _TRUSTED_COLLECTORS else "unverified"

            doc = RawKnowledgeDoc(
                doc_id=md_file.stem,
                title=meta.get("title", md_file.stem),
                source=meta.get("source", "unknown"),
                category=meta.get("category", "uncategorized"),
                tags=meta.get("tags", []) or [],
                trust_level=trust_level,
                technology="",  # collector doesn't emit this; left for future enrichment
                file_path=md_file,
            )
            yield doc, body

    def count_available(self) -> int:
        return sum(1 for _ in self.iter_documents())
