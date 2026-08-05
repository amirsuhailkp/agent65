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
    tool: str  # guaranteed non-empty by decide()'s validation below — a
    # Decision object is only ever constructed and returned after tool has
    # already been checked truthy/str, so this is not "should be str" but
    # "is always str by the time anything sees a Decision instance"
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

        if not tool or not isinstance(tool, str) or not tool.strip():
            # A Decision with tool=None/missing would otherwise pass the
            # `if not decision` check downstream (a Decision object is
            # truthy regardless of its fields) and flow through the ENTIRE
            # cycle — evidence collection, impact assessment, hypothesis
            # recording, report generation — before finally failing at
            # dispatch. Reject it here instead: no wasted cycle, no
            # tool=None garbage in the learning/report data.
            log.warning(f"next_action missing a valid 'tool': {next_action!r}")
            return None

        if target_hint and not self.scope_checker(target_hint):
            log.warning(f"BLOCKED: target_hint out of scope: {target_hint}")
            return None

        # Previously ONLY target_hint (the fixed --target CLI argument) was
        # scope-checked. It was never verified that the actual per-cycle
        # `params` the model chose for THIS tool call matched target_hint
        # at all — a model that picked a different, hallucinated, or
        # malformed target in `params` sailed straight through, because
        # the check was validating an unrelated string. Concretely: cycle
        # decided params={'target': 'http://target.com'} while target_hint
        # was still the original in-scope URL — that decision was never
        # blocked, because nothing ever looked at params['target'].
        # Check every param whose KEY suggests it's a target/URL/host
        # (covers every current tool: 'target' for httpx/nuclei/nmap/etc,
        # 'url_a'/'url_b' for diff_requests) rather than every param
        # value, so non-target params like nuclei's severity/tags strings
        # don't get run through scope matching and false-block a decision.
        target_like_keys = [
            k for k in params
            if any(s in k.lower() for s in ("target", "url", "host", "domain"))
        ]
        for key in target_like_keys:
            value = params.get(key)
            if isinstance(value, str) and value and not self.scope_checker(value):
                log.warning(f"BLOCKED: params['{key}']={value!r} out of scope (tool={tool})")
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