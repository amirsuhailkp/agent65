"""Decision Engine — Vol III Ch8.

Chooses next action from confidence, impact, coverage gain, cost, scope
compliance, risk. High-risk actions require user approval (Vol I Ch13).
"""
from __future__ import annotations
from dataclasses import dataclass
from ..logging_setup import get_logger

log = get_logger("planner.decision_engine")

RISK_REQUIRES_APPROVAL = {"high"}


@dataclass
class Decision:
    hypothesis_id: str | None
    tool: str | None
    params: dict
    reason: str
    risk_level: str
    requires_approval: bool
    approved: bool = False


class DecisionEngine:
    def __init__(self, scope_checker):
        """scope_checker: callable(target:str) -> bool"""
        self.scope_checker = scope_checker

    def decide(self, next_action: dict | None, target_hint: str | None,
               top_hypothesis_id: str | None) -> Decision | None:
        if not next_action:
            log.info("No actionable next_action from reasoning engine this cycle")
            return None
        if not isinstance(next_action, dict):
            log.error(f"decide() received non-dict next_action ({type(next_action).__name__}): {next_action!r}")
            return None

        tool = next_action.get("tool")
        params = next_action.get("params", {}) or {}
        reason = next_action.get("reason", "")
        risk_level = next_action.get("risk_level", "medium")

        if target_hint and not self.scope_checker(target_hint):
            log.warning(f"BLOCKED: target out of scope: {target_hint}")
            return None

        requires_approval = risk_level in RISK_REQUIRES_APPROVAL
        decision = Decision(
            hypothesis_id=top_hypothesis_id,
            tool=tool,
            params=params,
            reason=reason,
            risk_level=risk_level,
            requires_approval=requires_approval,
        )
        log.info(
            f"Decision: tool={tool} params={params} risk={risk_level} "
            f"approval_required={requires_approval} reason={reason}"
        )
        return decision