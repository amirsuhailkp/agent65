"""Tests for ImpactAssessor — the deep-model escalation point.

Checks the escalation gate is cheap/deterministic (doesn't call the LLM
unless warranted), and that failures/ambiguity fail CLOSED (clear_impact
stays False) rather than risk a false "verified" finding.
"""
import json
import pytest

from src.reasoning.impact_assessor import ImpactAssessor


class StubDeepLLM:
    def __init__(self, response=None, raise_error=False):
        self._response = response
        self._raise = raise_error
        self.calls = 0

    def chat(self, messages, format=None):
        self.calls += 1
        if self._raise:
            raise RuntimeError("ollama backend unavailable")
        return self._response


def test_should_escalate_requires_completed_execution():
    assessor = ImpactAssessor(StubDeepLLM(), min_confidence_to_escalate=0.5)
    assert assessor.should_escalate(hypothesis_confidence=0.9, exec_status="timeout") is False
    assert assessor.should_escalate(hypothesis_confidence=0.9, exec_status="completed") is True


def test_should_escalate_requires_minimum_confidence():
    assessor = ImpactAssessor(StubDeepLLM(), min_confidence_to_escalate=0.5)
    assert assessor.should_escalate(hypothesis_confidence=0.2, exec_status="completed") is False
    assert assessor.should_escalate(hypothesis_confidence=0.5, exec_status="completed") is True


def test_assess_parses_valid_deep_model_response():
    llm = StubDeepLLM(response=json.dumps({
        "clear_impact": True, "severity": "high",
        "false_positive_risk": "low", "reasoning": "Returned another user's private data.",
    }))
    assessor = ImpactAssessor(llm)
    result = assessor.assess(
        vulnerability="IDOR on /api/orders/{id}",
        attack_strategy="Increment order id as low-privilege user",
        tool_output="HTTP 200, order belonging to user_42 returned while authenticated as user_7",
        decision_reasoning="Confidence high, worth confirming",
    )
    assert result["clear_impact"] is True
    assert result["severity"] == "high"
    assert llm.calls == 1


def test_assess_fails_closed_on_llm_error():
    assessor = ImpactAssessor(StubDeepLLM(raise_error=True))
    result = assessor.assess("X", "Y", "some output", "some reasoning")
    assert result["clear_impact"] is False
    assert "assessment_failed" in result["reasoning"]


def test_assess_fails_closed_on_invalid_json():
    assessor = ImpactAssessor(StubDeepLLM(response="not json"))
    result = assessor.assess("X", "Y", "some output", "some reasoning")
    assert result["clear_impact"] is False


def test_skipped_result_never_claims_clear_impact():
    assessor = ImpactAssessor(StubDeepLLM())
    result = assessor.skipped_result("confidence too low")
    assert result["clear_impact"] is False
    assert result["reasoning"] == "confidence too low"


def test_assess_defaults_missing_fields_conservatively():
    # Deep model returns valid JSON but omits clear_impact entirely —
    # must default to False, never assume impact.
    llm = StubDeepLLM(response=json.dumps({"severity": "medium"}))
    assessor = ImpactAssessor(llm)
    result = assessor.assess("X", "Y", "output", "reason")
    assert result["clear_impact"] is False
