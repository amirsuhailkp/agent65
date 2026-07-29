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
source document. You NEVER invent facts not present in the text. A document may contain \
more than one distinct observation (e.g. multiple vulnerability classes) — extract each \
separately.

IMPORTANT — a document counts as extractable even if it is phrased as a "how to test" or \
"testing workflow" guide rather than an incident report or writeup. It does NOT need to use \
the word "vulnerability" anywhere. If the text describes a concrete, ordered technique for \
discovering or testing a vulnerability class — even using tool-documentation language like \
"go to this tab, click this button" — extract it. Name the "vulnerability" field using the \
general vulnerability class the technique tests for (e.g. "Broken Access Control - Horizontal \
Privilege Escalation"), even if the source document itself never uses that exact term and \
only describes the testing steps.

Example: a Burp Suite documentation page titled "Testing horizontal access controls" that \
walks through logging in as two users, capturing each user's session cookie, replaying one \
user's request with the other user's cookie, and reviewing whether the response leaks the \
first user's data — THIS COUNTS. vulnerability="Broken Access Control - Horizontal Privilege \
Escalation", discovery_sequence=["Obtain two accounts with identical privileges", "Capture \
first user's authenticated request", "Replace session cookie with second user's session", \
"Resend request", "Compare response to see if first user's data is returned"], \
tool_usage=["Burp Repeater", "Burp Proxy HTTP history", "Compare site maps", "Autorize extension"].

Only return an empty list if the document truly contains no testing technique at all (e.g. \
pure marketing content, changelogs, or feature announcements with no how-to steps).

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
    "horizontal privilege escalation": "idor_bola",
    "horizontal access control": "idor_bola",
    "broken access control": "authorization",
    "access control": "authorization",  # broad catch-all — missing/inadequate/insecure access control
    "broken function level authorization": "authorization",
    "privilege escalation": "privilege_escalation",
    "vertical privilege escalation": "privilege_escalation",
    "vertical escalation": "privilege_escalation",
    "business logic": "business_logic",
    "business logic flaw": "business_logic",
    "authentication bypass": "authentication",
    "auth bypass": "authentication",
    "broken user authentication": "authentication",
    "poor authentication": "authentication",
    "improper authentication": "authentication",
    "password": "authentication",  # weak/hardcoded password issues -> auth bucket
    "session management": "session_management",
    "session": "session_management",  # broad catch-all — hijacking/fixation/id predictability/etc.
    "jwt": "authentication",
    "oauth": "authentication",
    "sso": "authentication",
    "token": "authentication",
    "mfa": "mfa_bypass",
    "2fa": "mfa_bypass",
    "two factor": "mfa_bypass",
    "two-factor": "mfa_bypass",
    "ssrf": "ssrf",
    "server-side request forgery": "ssrf",
    "xss": "xss",
    "cross-site scripting": "xss",
    "csrf": "csrf",
    "cross-site request forgery": "csrf",
    "deserialization": "insecure_deserialization",
    "supply chain": "supply_chain",
    "code injection": "code_injection",
    "sql injection": "sql_injection",
    "api security": "api_security",
}


def normalize_category(vulnerability: str) -> str:
    """Maps free-text vulnerability names to a stable playbook category
    slug so the synthesizer can find "the same tactic" across many
    differently-worded reports. Tries an exact alias match first, then
    falls back to substring matching (longest alias first, so e.g.
    "horizontal privilege escalation" wins over a shorter unrelated
    substring) — this matters for compound names like "Broken Access
    Control - Horizontal Privilege Escalation" that won't exact-match
    any single alias key."""
    key = (vulnerability or "").strip().lower()
    if key in CATEGORY_ALIASES:
        return CATEGORY_ALIASES[key]
    for alias in sorted(CATEGORY_ALIASES, key=len, reverse=True):
        if alias in key:
            return CATEGORY_ALIASES[alias]
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
