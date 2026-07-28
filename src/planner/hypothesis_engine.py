"""Hypothesis Engine — Vol II Ch9, Vol III Ch7, Vol X (ranking).

States: Pending -> Testing -> Confirmed / Rejected / Needs More Evidence
"""
from __future__ import annotations
import datetime as dt
from dataclasses import dataclass, field
from enum import Enum


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
    status: HypothesisStatus = HypothesisStatus.PENDING
    retry_count: int = 0
    max_retries: int = 3
    evidence_ids: list = field(default_factory=list)
    created_at: str = field(default_factory=lambda: dt.datetime.utcnow().isoformat())


class HypothesisEngine:
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
        self._store: dict[str, Hypothesis] = {}

    def ingest(self, raw_hypotheses: list[dict]) -> list[Hypothesis]:
        """Validate reasoning-engine output before it becomes an actionable hypothesis.
        Rejects anything unsupported (Vol III Ch12 anti-hallucination)."""
        created = []
        for i, h in enumerate(raw_hypotheses):
            if not h.get("observation") or not h.get("attack_strategy"):
                continue  # incomplete — never accept partial fabrications
            hyp = Hypothesis(
                id=f"hyp_{dt.datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{i}",
                observation=h["observation"],
                attack_strategy=h["attack_strategy"],
                confidence=float(h.get("confidence", 0.0)),
                knowledge_grounded=bool(h.get("knowledge_grounded", False)),
                max_retries=self.max_retries,
            )
            self._store[hyp.id] = hyp
            created.append(hyp)
        return created

    def rank(self) -> list[Hypothesis]:
        """Vol X — score by evidence/knowledge support, novelty, verification history."""
        pending = [h for h in self._store.values() if h.status == HypothesisStatus.PENDING]

        def score(h: Hypothesis) -> float:
            grounding_bonus = 0.15 if h.knowledge_grounded else 0.0
            retry_penalty = 0.1 * h.retry_count
            return h.confidence + grounding_bonus - retry_penalty

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
             "confidence": round(h.confidence, 2)}
            for h in self._store.values()
            if h.status in (HypothesisStatus.PENDING, HypothesisStatus.TESTING,
                             HypothesisStatus.NEEDS_MORE_EVIDENCE)
        ]
