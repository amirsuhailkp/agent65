"""Observation Extraction — spec 'Observation Database'.

Turns ONE immutable knowledge document into zero or more structured
observations. Documents are never queried directly during planning —
only the observations (and the playbooks synthesized from them) are.

The LLM is used here purely as an extraction tool over text that is
already in front of it (Vol III Ch12 anti-hallucination principle still
applies): it may only report what the source text supports, and any
observation missing its core fields is dropped rather than guessed at.
"""
from __future__ import annotations
import json
import re
from dataclasses import dataclass, field

from ..knowledge.repository import RawKnowledgeDoc
from ..logging_setup import get_logger

log = get_logger("learning.observation_extractor")

_SYSTEM_PROMPT = """You extract structured security-testing observations from a single \
source document. You NEVER invent facts not present in the text. If the document does not \
describe a concrete vulnerability methodology, return an empty list. A document may contain \
more than one distinct observation (e.g. multiple vulnerability classes) — extract each \
separately.

Respond ONLY with JSON matching:
{
  "observations": [
    {
      "vulnerability": "short name, e.g. 'Subdomain Takeover' or 'IDOR'",
      "target_technology": "technology/stack this applies to, or '' if generic",
      "preconditions": ["..."],
      "discovery_sequence": ["ordered step 1", "ordered step 2", "..."],
      "payloads": ["..."],
      "tool_usage": ["..."],
      "decision_points": ["..."],
      "false_positives": ["..."],
      "failure_reasons": ["..."],
      "successful_validation_steps": ["..."],
      "severity": "info|low|medium|high|critical or '' if not stated",
      "references": ["..."]
    }
  ]
}
Omit fields you cannot support from the text — use an empty list/string, never a guess."""

# Lightweight canonicalization so near-duplicate phrasing (e.g. "Sub-domain
# Takeover" vs "subdomain takeover") lands in the same playbook category
# instead of spawning a duplicate. Extend as real data reveals more aliases.
# Public (no leading underscore) — LearningEngine reuses this for cheap
# keyword-based playbook retrieval without a second LLM/embedding call.
CATEGORY_ALIASES = {
    "subdomain takeover": "subdomain_takeover",
    "sub-domain takeover": "subdomain_takeover",
    "dns takeover": "subdomain_takeover",
    "idor": "idor_bola",
    "insecure direct object reference": "idor_bola",
    "insecure direct object references": "idor_bola",
    "bola": "idor_bola",
    "broken object level authorization": "idor_bola",
    "broken access control": "authorization",
    "business logic": "business_logic",
    "business logic flaw": "business_logic",
    "authentication bypass": "authentication",
    "auth bypass": "authentication",
    "session management": "session_management",
    "jwt": "authentication",
    "ssrf": "ssrf",
    "server-side request forgery": "ssrf",
    "xss": "xss",
    "cross-site scripting": "xss",
    "api security": "api_security",
}


def normalize_category(vulnerability: str) -> str:
    """Maps free-text vulnerability names to a stable playbook category
    slug so the synthesizer can find "the same tactic" across many
    differently-worded reports."""
    key = (vulnerability or "").strip().lower()
    if key in CATEGORY_ALIASES:
        return CATEGORY_ALIASES[key]
    slug = re.sub(r"[^a-z0-9]+", "_", key).strip("_")
    return slug or "uncategorized"


@dataclass
class ExtractedObservation:
    vulnerability: str
    target_technology: str = ""
    preconditions: list = field(default_factory=list)
    discovery_sequence: list = field(default_factory=list)
    payloads: list = field(default_factory=list)
    tool_usage: list = field(default_factory=list)
    decision_points: list = field(default_factory=list)
    false_positives: list = field(default_factory=list)
    failure_reasons: list = field(default_factory=list)
    successful_validation_steps: list = field(default_factory=list)
    severity: str = ""
    references: list = field(default_factory=list)
    category: str = ""

    def __post_init__(self):
        if not self.category:
            self.category = normalize_category(self.vulnerability)


class ObservationExtractor:
    def __init__(self, llm_client):
        """`llm_client` only needs a `.chat(messages, format=None) -> str`
        method — same duck-typed interface as OllamaClient, so tests can
        inject a stub without a real Ollama backend."""
        self.llm = llm_client

    def _build_messages(self, doc: RawKnowledgeDoc, body: str) -> list[dict]:
        # Documents can be long; the extraction task only needs the body,
        # trimmed defensively so it stays inside the 8B model's context window.
        trimmed = body[:6000]
        user = (
            f"Document title: {doc.title}\n"
            f"Source: {doc.source}\n"
            f"Category (collector-assigned): {doc.category}\n\n"
            f"--- DOCUMENT TEXT ---\n{trimmed}"
        )
        return [
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": user},
        ]

    def extract(self, doc: RawKnowledgeDoc, body: str) -> list[ExtractedObservation]:
        messages = self._build_messages(doc, body)
        try:
            raw = self.llm.chat(messages, format="json")
        except Exception as e:
            log.error(f"Observation extraction LLM call failed for {doc.doc_id}: {e}")
            return []

        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            log.warning(f"Non-JSON extraction output for {doc.doc_id}, discarding")
            return []

        results = []
        for item in parsed.get("observations", []):
            vuln = (item.get("vulnerability") or "").strip()
            sequence = item.get("discovery_sequence") or []
            # Anti-hallucination guard: an observation with no named
            # vulnerability AND no discovery sequence carries no evidence
            # value — drop it rather than let it seed a hollow playbook.
            if not vuln and not sequence:
                continue
            results.append(ExtractedObservation(
                vulnerability=vuln or "uncategorized",
                target_technology=item.get("target_technology", "") or "",
                preconditions=item.get("preconditions") or [],
                discovery_sequence=sequence,
                payloads=item.get("payloads") or [],
                tool_usage=item.get("tool_usage") or [],
                decision_points=item.get("decision_points") or [],
                false_positives=item.get("false_positives") or [],
                failure_reasons=item.get("failure_reasons") or [],
                successful_validation_steps=item.get("successful_validation_steps") or [],
                severity=item.get("severity", "") or "",
                references=item.get("references") or [],
            ))
        return results
