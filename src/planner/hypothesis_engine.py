"""Hypothesis Engine — Vol II Ch9, Vol III Ch7, Vol X (ranking).

States: Pending -> Testing -> Confirmed / Rejected / Needs More Evidence
"""
from __future__ import annotations
import datetime as dt
from dataclasses import dataclass, field
from enum import Enum
from ..logging_setup import get_logger
from ..learning.observation_extractor import CATEGORY_ALIASES, BROAD_ALIASES

log = get_logger("planner.hypothesis_engine")


# Deliberately NOT the full CATEGORY_ALIASES table. That table is tuned
# for classifying playbook/observation TITLES, where a single alias
# reliably names the whole finding. A hypothesis's free-text reasoning is
# messier — e.g. a legitimate sql_injection hypothesis can say "auth
# bypass payload" as its technique without being an authentication
# finding at all — so blindly reusing every alias there produced false
# overrides on hypotheses that were correctly tagged already (see
# test_rank_scope_filter_prefers_matching_category).
#
# This set is scoped narrowly to the ONE failure mode actually observed
# in practice (sessions 43-45): the model relabeling an IDOR-flavored
# hypothesis under an in-scope category to slip past the scope gate.
# idor_bola aliases are unusually safe to trust at face value here
# because they name a specific, unambiguous concept (IDOR/BOLA) that
# essentially never shows up as an incidental technique-mention inside a
# hypothesis actually about something else — unlike "auth bypass",
# "session", or "password", which cut across many categories.
_LAUNDERING_WATCH_ALIASES = {
    alias: category for alias, category in CATEGORY_ALIASES.items()
    if category == "idor_bola" and alias not in BROAD_ALIASES
}


def _infer_category_from_text(text: str) -> str | None:
    """Scan a hypothesis's own reasoning text (observation + attack_strategy)
    for an unambiguous signal that it's actually about a category different
    from whatever the model self-reported.

    This exists to close a gap the self-reported `category` field left
    open: the model can (observed session 45, cycle 5) write a hypothesis
    whose text is plainly about IDOR ("identify potential IDOR vectors...
    user_id...") while tagging it with a DIFFERENT, in-scope category
    string ("authentication") — which sails straight through
    decision_engine's category_out_of_scope gate, since that gate only
    ever inspects the tag, never the content it's supposedly describing.

    Returns None when no watched alias is found, never a fabricated
    category from the raw text — absence of signal should never itself
    become an override.
    """
    key = (text or "").lower()
    if not key:
        return None
    hits = [
        (key.find(alias), -len(alias), category)
        for alias, category in _LAUNDERING_WATCH_ALIASES.items()
        if alias in key
    ]
    if not hits:
        return None
    hits.sort()
    return hits[0][2]

# qwen3:4b occasionally answers "confidence" with a word ("low"/"medium"/
# "high") instead of the requested 0.0-1.0 float, despite the schema. A bare
# float(h["confidence"]) on that raises ValueError and previously crashed
# the ENTIRE ingest() call — not just that one hypothesis — losing every
# other hypothesis generated in the same cycle and killing the whole run
# (observed: session 44 cycle 5, "could not convert string to float: 'low'").
_WORD_CONFIDENCE = {"none": 0.0, "very low": 0.1, "low": 0.25, "medium": 0.5,
                     "moderate": 0.5, "high": 0.75, "very high": 0.9, "certain": 1.0}


def _parse_confidence(value) -> float:
    if isinstance(value, (int, float)):
        return max(0.0, min(1.0, float(value)))
    if isinstance(value, str):
        s = value.strip().lower()
        if s in _WORD_CONFIDENCE:
            return _WORD_CONFIDENCE[s]
        try:
            return max(0.0, min(1.0, float(s)))
        except ValueError:
            pass
    log.warning(f"Unparseable confidence value {value!r} — defaulting to 0.0")
    return 0.0


class HypothesisStatus(str, Enum):
    PENDING = "pending"
    TESTING = "testing"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    NEEDS_MORE_EVIDENCE = "needs_more_evidence"


@dataclass
class Hypothesis:
    id: str
    observation: str
    attack_strategy: str
    confidence: float
    knowledge_grounded: bool
    # Vulnerability class this hypothesis actually tests for, as declared
    # by the reasoning model (see prompt_builder's OUTPUT_FORMAT). None
    # when the model omitted it (older prompt version, or a malformed
    # response) — callers that scope by category should treat None as
    # "unknown," never as "matches everything."
    category: str | None = None
    status: HypothesisStatus = HypothesisStatus.PENDING
    retry_count: int = 0
    max_retries: int = 3
    evidence_ids: list = field(default_factory=list)
    created_at: str = field(default_factory=lambda: dt.datetime.utcnow().isoformat())
    # Set once a mid-flight "needs_more_evidence" signal has been recorded
    # as a partial Experience — prevents every retry cycle of the same
    # hypothesis from re-recording the same non-terminal signal.
    partial_recorded: bool = False


class HypothesisEngine:
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
        self._store: dict[str, Hypothesis] = {}

    def ingest(self, raw_hypotheses: list[dict]) -> list[Hypothesis]:
        """Validate reasoning-engine output before it becomes an actionable hypothesis.
        Rejects anything unsupported (Vol III Ch12 anti-hallucination).

        Each hypothesis is isolated in its own try/except: one malformed
        field (wrong type, unexpected shape) must never crash the whole
        cycle and discard every OTHER hypothesis the model generated this
        turn — it should just be skipped, logged, and the rest ingested
        normally."""
        created = []
        for i, h in enumerate(raw_hypotheses):
            if not h.get("observation") or not h.get("attack_strategy"):
                continue  # incomplete — never accept partial fabrications
            try:
                self_reported = (str(h.get("category") or "")).strip().lower() or None
                inferred = _infer_category_from_text(
                    f"{h['observation']} {h['attack_strategy']}"
                )
                category = self_reported
                if inferred and inferred != self_reported:
                    log.warning(
                        f"Hypothesis category mismatch: model tagged "
                        f"{self_reported!r} but its own text specifically "
                        f"signals {inferred!r} — overriding to {inferred!r} "
                        f"so scope enforcement sees the real category. "
                        f"observation={h['observation']!r}"
                    )
                    category = inferred
                hyp = Hypothesis(
                    id=f"hyp_{dt.datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{i}",
                    observation=h["observation"],
                    attack_strategy=h["attack_strategy"],
                    confidence=_parse_confidence(h.get("confidence", 0.0)),
                    knowledge_grounded=bool(h.get("knowledge_grounded", False)),
                    category=category,
                    max_retries=self.max_retries,
                )
            except Exception as e:
                log.warning(f"Skipping malformed hypothesis entry {h!r}: {e}")
                continue
            self._store[hyp.id] = hyp
            created.append(hyp)
        return created

    def rank(self, scope_categories: list[str] | None = None) -> list[Hypothesis]:
        """Vol X — score by evidence/knowledge support, novelty, verification history.

        scope_categories: when the current goal has an explicit vulnerability-
        class scope (inferred from goal text or passed via --vuln-category),
        prefer hypotheses tagged with a matching category over ones tagged
        with something else. Untagged hypotheses (category is None — an
        older/malformed model response) are treated as ambiguous, not as
        automatically in- or out-of-scope, and are ranked alongside in-scope
        ones rather than excluded outright. If scoping would eliminate every
        pending hypothesis, scoping is dropped for this call (fall back to
        the full ranked list) rather than returning nothing — an over-eager
        filter should never be able to fully stall the cycle.
        """
        pending = [h for h in self._store.values() if h.status == HypothesisStatus.PENDING]

        def score(h: Hypothesis) -> float:
            grounding_bonus = 0.15 if h.knowledge_grounded else 0.0
            retry_penalty = 0.1 * h.retry_count
            return h.confidence + grounding_bonus - retry_penalty

        if scope_categories:
            scoped = {c.lower() for c in scope_categories}
            in_scope = [h for h in pending if h.category is None or h.category in scoped]
            if in_scope:
                pending = in_scope

        return sorted(pending, key=score, reverse=True)

    def mark_testing(self, hyp_id: str):
        self._store[hyp_id].status = HypothesisStatus.TESTING

    def record_result(self, hyp_id: str, confirmed: bool, evidence_id: str | None = None):
        hyp = self._store[hyp_id]
        if evidence_id:
            hyp.evidence_ids.append(evidence_id)
        if confirmed:
            hyp.status = HypothesisStatus.CONFIRMED
            hyp.confidence = min(1.0, hyp.confidence + 0.2)
        else:
            hyp.retry_count += 1
            if hyp.retry_count >= hyp.max_retries:
                hyp.status = HypothesisStatus.REJECTED
                hyp.confidence = max(0.0, hyp.confidence - 0.3)
            else:
                hyp.status = HypothesisStatus.NEEDS_MORE_EVIDENCE

    def active(self) -> list[dict]:
        return [
            {"id": h.id, "observation": h.observation, "status": h.status.value,
             "confidence": round(h.confidence, 2), "category": h.category}
            for h in self._store.values()
            if h.status in (HypothesisStatus.PENDING, HypothesisStatus.TESTING,
                             HypothesisStatus.NEEDS_MORE_EVIDENCE)
        ]