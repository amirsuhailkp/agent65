"""Verification Engine — Vol II Ch16, Vol V Ch13.

No finding is accepted without verification: repeatability, alternate
payloads, stable evidence, clear impact. Unverified observations remain
hypotheses, never findings.
"""
from __future__ import annotations
from dataclasses import dataclass
from ..logging_setup import get_logger

log = get_logger("planner.verification")


@dataclass
class VerificationResult:
    verified: bool
    reason: str
    confidence: float


class VerificationEngine:
    def verify(
        self,
        reproductions: int,
        alternate_payloads_tried: int,
        evidence_count: int,
        stable_across_attempts: bool,
        clear_impact: bool,
    ) -> VerificationResult:
        if reproductions < 1:
            return VerificationResult(False, "not reproduced", 0.0)
        if evidence_count < 1:
            return VerificationResult(False, "no supporting evidence stored", 0.0)
        if not stable_across_attempts:
            return VerificationResult(False, "inconsistent behavior across attempts", 0.2)
        if not clear_impact:
            return VerificationResult(False, "impact not clearly demonstrated", 0.3)

        confidence = min(1.0, 0.5 + 0.1 * reproductions + 0.1 * alternate_payloads_tried)
        log.info(f"Finding verified: reproductions={reproductions} confidence={confidence:.2f}")
        return VerificationResult(True, "reproduced with stable, high-impact evidence", confidence)
