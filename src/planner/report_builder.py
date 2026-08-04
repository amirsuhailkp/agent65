"""Turns a terminal hypothesis outcome into a FindingDraft for ReportEngine.

Deliberately fires for REJECTED hypotheses too, not just CONFIRMED ones —
a real pentest report documents what was tested and ruled out, not only
what succeeded. An engagement with ten tested theories and one real bug
should produce eleven records of what happened, not one.
"""
from __future__ import annotations
from ..reporting.report_engine import FindingDraft


def build_finding_draft(
    hypothesis,          # Hypothesis (planner.hypothesis_engine)
    decision,            # Decision (planner.decision_engine)
    exec_result,         # ExecutionResult (dispatcher.kali_dispatcher)
    impact: dict,
    verification,        # VerificationResult (planner.verification_engine)
    category: str,
    evidence_id: int | None,
    target_hint: str | None,
) -> FindingDraft:
    verified = hypothesis.status.value == "confirmed"

    title = f"{category.replace('_', ' ').title()}: {hypothesis.observation}"[:120]

    description = (
        f"**Observation:** {hypothesis.observation}\n\n"
        f"**Attack strategy tested:** {hypothesis.attack_strategy}\n\n"
        f"**Outcome:** {'Confirmed' if verified else 'Not confirmed / ruled out'} "
        f"after {hypothesis.retry_count + 1} attempt(s).\n\n"
        f"**Verification engine's reason:** {verification.reason}"
    )

    steps_to_reproduce = (
        f"1. Target: `{target_hint or '(not set)'}`\n"
        f"2. Tool: `{decision.tool}`\n"
        f"3. Command executed:\n   ```\n   {exec_result.command}\n   ```\n"
        f"4. Result: `{exec_result.status}` (exit_code={exec_result.exit_code})\n"
        f"5. Planner's stated reasoning at decision time: {decision.reason}"
    )

    impact_text = (
        f"**Draft severity (impact assessor, human review required):** {impact.get('severity', 'info')}\n"
        f"**Clear impact demonstrated:** {impact.get('clear_impact', False)}\n"
        f"**False positive risk:** {impact.get('false_positive_risk', 'unknown')}\n"
        f"**Assessor reasoning:** {impact.get('reasoning', '(none recorded)')}"
    )

    if verified:
        remediation = (
            f"Draft only — requires human review. General guidance for "
            f"{category.replace('_', ' ')} findings: enforce server-side "
            f"authorization checks on every object reference; do not rely on "
            f"client-supplied IDs without verifying the requesting session "
            f"owns that resource."
        )
    else:
        remediation = (
            "Not applicable — hypothesis was not confirmed as exploitable. "
            "Retained here as a record of what was tested and ruled out, "
            "so it isn't re-tested identically in a future run."
        )

    evidence_refs = [f"hypothesis_id={hypothesis.id}"]
    if evidence_id is not None:
        evidence_refs.append(f"evidence_id={evidence_id}")

    return FindingDraft(
        title=title,
        category=category,
        severity=impact.get("severity", "info"),
        confidence=hypothesis.confidence,
        verified=verified,
        description=description,
        steps_to_reproduce=steps_to_reproduce,
        impact=impact_text,
        remediation=remediation,
        evidence_refs=evidence_refs,
    )