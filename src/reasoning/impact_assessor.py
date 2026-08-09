"""Impact Assessor — the one deliberately "deep thinking" call in the
cognitive cycle.

Everything else in a cycle (hypothesis generation, ranking, decisions)
runs on the fast model (qwen3:4b) so the loop stays quick and the GPU
stays cool. This module is the escalation point: it calls the deep model
(qwen3:8b) to make the one judgment call that actually benefits from
deeper reasoning — "did this hypothesis just get demonstrated with real,
clear impact, the way an experienced pentester would judge it, or does
it just look interesting?"

This directly answers VerificationEngine's `clear_impact` gate, which
previously was always hardcoded to False in the planner (nothing could
ever reach `verified=True`). Escalation is gated so the expensive model
is only invoked when it's actually worth it:
  - the hypothesis must have cleared a minimum confidence bar
  - the tool execution must have actually completed (no point judging
    impact from a crashed/timed-out run)

If the deep model is unavailable or fails, this fails CLOSED — impact is
never assumed clear just because the judgment call couldn't be made.
"""
from __future__ import annotations
import json

from ..logging_setup import get_logger

log = get_logger("reasoning.impact_assessor")

_SYSTEM_PROMPT = """You are a senior penetration tester making the final call on whether a \
finding has been demonstrated with clear, real-world impact — not just a plausible-looking \
signal. Be skeptical: most "interesting" tool output is a false positive or needs more work \
before it counts as a verified finding. You are NOT deciding whether to keep investigating —
that decision is already made. You are ONLY judging the evidence already gathered.

Respond ONLY with JSON:
{
  "clear_impact": true/false,
  "severity": "info|low|medium|high|critical",
  "false_positive_risk": "low|medium|high",
  "reasoning": "1-3 sentences, specific to the evidence given"
}
clear_impact must be false unless the evidence itself (not the hypothesis's stated intent) \
demonstrates concrete, exploitable impact — e.g., actual unauthorized data returned, an \
actual auth bypass observed, not just a request that "might" have worked."""


class ImpactAssessor:
    def __init__(self, deep_llm_client, min_confidence_to_escalate: float = 0.5):
        """`deep_llm_client` is duck-typed like OllamaClient (`.chat(messages,
        format=None) -> str`) — normally pointed at a larger/slower model
        than the one driving the rest of the cognitive cycle."""
        self.llm = deep_llm_client
        self.min_confidence_to_escalate = min_confidence_to_escalate

    def should_escalate(
        self, hypothesis_confidence: float, exec_status: str, tool_output: str | None = None
    ) -> bool:
        """Cheap, deterministic gate — decides whether this cycle's
        finding is even worth spending the deep model on. Keeps the
        expensive call rare (heat/latency stay bounded) rather than
        firing on every cycle.

        Escalates if EITHER of two things is true:
          - the fast model's own pre-test confidence in the hypothesis
            clears the bar, OR
          - the tool's own output already reports a concrete evidence
            signal (e.g. diff_requests' `idor_suggestive` flag — same
            status code, non-identical bodies).

        The second path exists because pre-test confidence and
        post-test evidence answer different questions. A small local
        model's self-reported confidence in a hypothesis it just wrote
        is frequently miscalibrated and says nothing about whether the
        test that just RAN found something. A well-targeted test (e.g.
        known-good usernames against a suspected IDOR parameter) that
        comes back with an actual observed difference should never be
        skipped just because the model felt lukewarm about it going in
        — that's exactly the kind of result the deep model exists to
        judge carefully."""
        if exec_status != "completed":
            return False
        if hypothesis_confidence >= self.min_confidence_to_escalate:
            return True
        return self._has_evidence_signal(tool_output)

    @staticmethod
    def _has_evidence_signal(tool_output: str | None) -> bool:
        """Best-effort, tool-agnostic check for a strong signal a tool
        already computed for itself. Currently recognizes
        diff_requests' `diff.idor_suggestive` flag. Deliberately
        narrow and fails closed: any output that isn't JSON, or doesn't
        have this exact shape, just returns False and falls through to
        the existing confidence-based path — this widens escalation,
        it never replaces or weakens the confidence gate for tools that
        don't report a signal like this."""
        if not tool_output:
            return False
        try:
            parsed = json.loads(tool_output)
        except (json.JSONDecodeError, TypeError):
            return False
        if not isinstance(parsed, dict):
            return False
        diff = parsed.get("diff")
        if isinstance(diff, dict):
            return bool(diff.get("idor_suggestive"))
        return False

    def assess(
        self,
        vulnerability: str,
        attack_strategy: str,
        tool_output: str,
        decision_reasoning: str,
    ) -> dict:
        """Returns {"clear_impact": bool, "severity": str,
        "false_positive_risk": str, "reasoning": str}. Fails closed —
        any error keeps clear_impact False rather than risk a false
        "verified" finding."""
        trimmed_output = (tool_output or "")[:4000]
        user = (
            f"Hypothesis: {vulnerability}\n"
            f"Attack strategy: {attack_strategy}\n"
            f"Why this action was taken: {decision_reasoning}\n\n"
            f"--- RAW TOOL OUTPUT / EVIDENCE ---\n{trimmed_output or '(no output captured)'}"
        )
        messages = [
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": user},
        ]
        try:
            raw = self.llm.chat(messages, format="json")
            parsed = json.loads(raw)
            result = {
                "clear_impact": bool(parsed.get("clear_impact", False)),
                "severity": parsed.get("severity", "info"),
                "false_positive_risk": parsed.get("false_positive_risk", "high"),
                "reasoning": parsed.get("reasoning", ""),
            }
            log.info(f"Deep impact assessment: clear_impact={result['clear_impact']} "
                      f"severity={result['severity']}")
            return result
        except Exception as e:
            log.error(f"Impact assessment failed, failing closed (clear_impact=False): {e}")
            return {"clear_impact": False, "severity": "info",
                    "false_positive_risk": "high", "reasoning": f"assessment_failed: {e}"}

    def skipped_result(self, reason: str) -> dict:
        """Used when should_escalate() said no — keeps the same shape as
        assess() so callers don't need a branch for the not-escalated case."""
        return {"clear_impact": False, "severity": "info",
                "false_positive_risk": "unknown", "reasoning": reason}
