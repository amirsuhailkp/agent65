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
    "broken access control": "authorization",  # broad catch-all
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

    # --- expanded aliases (session 38 recategorization pass) ---
    # IDOR / BOLA / access control — strategic-priority category, was
    # split across mass_assignment_*, orm_leak_*, authorization_bypass_*.
    "mass assignment": "idor_bola",
    "authorization bypass": "idor_bola",
    "authorization bypass through user controlled key": "idor_bola",
    "orm leak": "idor_bola",
    "excessive data exposure": "idor_bola",
    "broken tenant isolation": "authorization",
    "tenant context injection": "authorization",
    "insecure design": "insecure_design",

    # SSRF / injection family already have a canonical bucket — fold in
    # near-duplicate compound names instead of minting new ones.
    "xxe": "xml_external_entity_xxe",
    "xml external entity": "xml_external_entity_xxe",
    "blind xxe": "xml_external_entity_xxe",
    "server-side template injection": "server_side_template_injection",
    "ssti": "server_side_template_injection",
    "client-side template injection": "client_side_template_injection",
    "ldap injection": "ldap_injection",
    "xpath injection": "injection",
    "os command injection": "command_injection",
    "command injection": "command_injection",
    "expression language injection": "injection",
    "ognl injection": "injection",
    "graphql injection": "injection",
    "json injection": "injection",
    "html injection": "injection",
    "markdown injection": "injection",
    "prototype pollution": "prototype_pollution",
    "client-side prototype pollution": "prototype_pollution",
    "dom clobbering": "dom_clobbering",

    # HTTP request smuggling — was fragmented into 9 near-duplicate
    # technique-specific slugs (cl.te, te.cl, 0.cl, h2 downgrade, etc.).
    # Fold all technique variants into one canonical bucket; the specific
    # technique still lives in the observation's own text/payloads.
    "request smuggling": "http_request_smuggling",
    "http smuggling": "http_request_smuggling",
    "cl.te": "http_request_smuggling",
    "te.cl": "http_request_smuggling",
    "desync": "http_request_smuggling",
    "http/2 downgrade": "http_request_smuggling",
    "http request smuggling": "http_request_smuggling",

    # Security misconfiguration — was fragmented into 15+ near-duplicate
    # slugs (default creds, directory listing, verbose errors, missing
    # headers, cloud storage perms — all separately worded).
    "security misconfiguration": "security_misconfiguration",
    "default credentials": "security_misconfiguration",
    "default accounts": "security_misconfiguration",
    "directory listing": "security_misconfiguration",
    "missing security header": "security_misconfiguration",
    "misconfigured security header": "security_misconfiguration",
    "insecure cloud storage": "security_misconfiguration",
    "over-permissive cloud storage": "security_misconfiguration",
    "cloud storage permission": "security_misconfiguration",
    "outdated component": "vulnerable_and_outdated_components",
    "known vulnerable component": "vulnerable_and_outdated_components",
    "vulnerable and outdated component": "vulnerable_and_outdated_components",
    "vulnerable or outdated component": "vulnerable_and_outdated_components",

    # Information disclosure — was fragmented into 20+ near-duplicate
    # slugs by disclosure vector (error messages, directory listing,
    # identifier enumeration, GraphQL introspection, CSS selectors...).
    # Vector-level detail belongs in the observation text, not the
    # category, or this stays permanently fragmented.
    "information disclosure": "information_disclosure",
    "identifier enumeration": "information_disclosure",
    "username enumeration": "information_disclosure",
    "email enumeration": "information_disclosure",
    "verbose error": "information_disclosure",
    "stack trace": "information_disclosure",
    "sensitive data exposure": "sensitive_data_exposure",
    "sensitive data logging": "sensitive_data_exposure",

    # Crypto / transport — was fragmented by specific weakness
    # (weak cipher, weak IV, cert validation, downgrade attacks).
    "weak cryptographic algorithm": "cryptographic_failures",
    "weak or deprecated cryptographic algorithm": "cryptographic_failures",
    "weak or broken cryptographic algorithm": "cryptographic_failures",
    "insufficient entropy": "cryptographic_failures",
    "insecure cryptographic storage": "cryptographic_failures",
    "hardcoded cryptographic key": "cryptographic_failures",
    "hard-coded cryptographic key": "cryptographic_failures",
    "weak key management": "cryptographic_failures",
    "insufficient key management": "cryptographic_failures",
    "padding oracle": "cryptographic_failures",
    "certificate validation": "cryptographic_failures",
    "certificate chain validation": "cryptographic_failures",
    "ssl/tls downgrade": "cryptographic_failures",
    "ssl strip": "cryptographic_failures",
    "weak cipher": "cryptographic_failures",
    "weak diffie-hellman": "cryptographic_failures",
    "cleartext transmission": "insecure_communication",
    "insecure transport": "insecure_communication",

    # Reconnaissance / attack-surface mapping — was fragmented by tool
    # or technique (openapi discovery, js-based discovery, forced
    # browsing, subdomain enumeration variants).
    "endpoint discovery": "attack_surface_enumeration",
    "api endpoint discovery": "attack_surface_enumeration",
    "shadow api": "attack_surface_enumeration",
    "deprecated route discovery": "attack_surface_enumeration",
    "undocumented endpoint": "attack_surface_enumeration",
    "forced browsing": "attack_surface_enumeration",
    "force browsing": "attack_surface_enumeration",
    # Exact-string override: this exact reversed-order phrasing recurs in
    # the corpus ("Forced Browsing" stated first, "Broken Access Control"
    # in parentheses second). Both terms are broad-tier, so without an
    # exact match the tiebreak falls to primary-segment position, which
    # picks "forced browsing" (wrong -- the parenthetical is the actual
    # classification here, forced browsing is just the technique).
    "forced browsing (broken access control)": "authorization",
    "content discovery": "attack_surface_enumeration",
    "hidden file": "attack_surface_enumeration",
    "subdomain enumeration": "subdomain_takeover",

    # Rate limiting / DoS
    "rate limiting": "denial_of_service",
    "resource exhaustion": "denial_of_service",
    "denial of wallet": "denial_of_service",

    # CORS / open redirect
    "cors misconfiguration": "cors_misconfiguration",
    "open redirect": "open_redirect",
    "open redirection": "open_redirect",

    # Supply chain / dependency
    "dependency confusion": "supply_chain",
    "license risk": "supply_chain",
    "typosquatting": "supply_chain",
    "malicious update": "supply_chain",

    # LLM / prompt-injection family (kept distinct from web-app categories
    # since tooling and payloads differ substantially).
    "prompt injection": "prompt_injection",
    "jailbreak": "prompt_injection",
    "excessive agency": "prompt_injection",
    "model theft": "prompt_injection",
    "model inversion": "prompt_injection",
    "data poisoning": "prompt_injection",
    "tool poisoning": "prompt_injection",
    "insecure output handling": "prompt_injection",

    # WebSocket family
    "websocket": "websocket_vulnerabilities",

    # Container / cloud infra
    "container escape": "container_security",
    "kubernetes": "container_security",
    "docker": "container_security",
    "iam role": "container_security",
    "infrastructure as code": "container_security",
}

# Aliases that are broad/generic enough to appear as an incidental term
# inside an otherwise unrelated compound description (e.g. "SQL Injection
# - leads to sensitive data exposure" is fundamentally a SQL injection,
# not a sensitive-data-exposure finding). normalize_category() always
# prefers a match NOT in this set over one that is, regardless of which
# is longer or where it appears in the string. Keep this in sync with
# any similarly generic alias added to CATEGORY_ALIASES above.
BROAD_ALIASES = frozenset({
    "access control",
    "broken access control",
    "session",
    "security misconfiguration",
    "default credentials",
    "default accounts",
    "directory listing",
    "missing security header",
    "misconfigured security header",
    "insecure cloud storage",
    "over-permissive cloud storage",
    "cloud storage permission",
    "outdated component",
    "known vulnerable component",
    "information disclosure",
    "identifier enumeration",
    "username enumeration",
    "email enumeration",
    "verbose error",
    "stack trace",
    "sensitive data exposure",
    "sensitive data logging",
    "insecure transport",
    "cleartext transmission",
    "rate limiting",
    "resource exhaustion",
    "denial of wallet",
    "content discovery",
    # Generic single-word auth-mechanism terms — these appear as
    # incidental substrings across many unrelated finding types
    # ("Session Token Tampering", "Broken Access Control - JWT
    # Manipulation") and previously outranked the correct root
    # classification (broken_access_control/session_management) simply
    # for being tagged "specific" by default. session 39 fix.
    "token",
    "jwt",
    "oauth",
    "sso",
    "password",
    # Attack techniques/mechanisms used to reach an access-control
    # finding, not a distinct root vulnerability class on their own —
    # "Broken Access Control - Forced Browsing" is an access-control
    # finding reached via forced browsing, not a recon/attack-surface
    # finding. Standalone "Forced Browsing" with no other alias present
    # still correctly resolves to attack_surface_enumeration.
    "forced browsing",
    "force browsing",
    "hidden file",
    "docker",
    "kubernetes",
    "iam role",
    "infrastructure as code",
})


def normalize_category(vulnerability: str) -> str:
    """Maps free-text vulnerability names to a stable playbook category
    slug so the synthesizer can find "the same tactic" across many
    differently-worded reports.

    Matching is tiered, in this priority order:
      1. exact full-string alias match
      2. any SPECIFIC (non-broad) substring alias match — preferring one
         found in the leading/primary segment of the string, then the
         longest
      3. any BROAD (see BROAD_ALIASES) substring alias match, same
         preference order

    Why tiered instead of "longest substring wins" (the original
    approach): a compound description like "SQL Injection - leads to
    sensitive data exposure via database dump" contains both a specific
    alias ("sql injection") and a long broad/generic one ("sensitive
    data exposure"). Pure longest-match picked the broad one and
    silently reclassified real sql_injection/xss/mfa_bypass observations
    into unrelated categories during a live recategorization run.
    Requiring specific aliases to always outrank broad ones fixes that,
    while still correctly resolving cases like "Broken Access Control -
    Horizontal Privilege Escalation" (broad term first, specific term
    second) to the specific category (idor_bola), since tier is checked
    before position.

    Within the same tier, when neither match falls in the primary
    segment (common for list-style titles like "Injection (e.g., XSS,
    Command Injection)", where the real subject is a generic word like
    "Injection" and every specific vuln name is just an example listed
    in parentheses), ties break on LEFTMOST POSITION in the string, not
    alias length. A prior version used length here, which meant a long
    alias like "command injection" always beat the short "xss" even
    when XSS was the one actually named first -- e.g. "Blind
    Vulnerabilities (SQLi, XSS, OS Command Injection)" incorrectly
    became command_injection instead of xss.
    """
    key = (vulnerability or "").strip().lower()
    if not key:
        return "uncategorized"
    if key in CATEGORY_ALIASES:
        return CATEGORY_ALIASES[key]

    primary = re.split(
        r"\s*(?:-|–|:|\(|\bvia\b|\bleading to\b|\bcauses?\b|\bresulting in\b|\bthrough\b)\s*",
        key,
        maxsplit=1,
    )[0].strip()

    matches = []  # (is_broad, not_in_primary, position, -length, category)
    for alias, category in CATEGORY_ALIASES.items():
        pos = key.find(alias)
        if pos != -1:
            matches.append((
                alias in BROAD_ALIASES,
                alias not in primary,
                pos,
                -len(alias),
                category,
            ))
    if matches:
        matches.sort()
        return matches[0][4]

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