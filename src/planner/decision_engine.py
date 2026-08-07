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
        # Set by decide() only when it rejects a decision specifically due
        # to a target/url/host param being out of scope — never for other
        # rejection reasons (missing tool, no next_action at all). The
        # planner reads this after a None return to decide whether a
        # same-cycle correction retry makes sense: retrying is only
        # useful when we know *what* was wrong and *what the right value
        # is*, which is exactly the scope-drift case.
        self.last_block_reason: dict | None = None

    def correction_message(self, canonical_target: str | None) -> str | None:
        """Human-readable explanation of the last decide() scope block, for
        re-prompting the model within the same cycle instead of silently
        discarding the whole cycle. Returns None if the last decide() call
        didn't fail due to a scope block, so callers can tell "safe to
        retry" apart from "retrying won't help" without inspecting
        last_block_reason's shape themselves."""
        block = self.last_block_reason
        if not block:
            return None
        key, value, tool = block["key"], block["value"], block.get("tool")

        if tool == "diff_requests":
            # diff_requests is the odd one out: its two target-like params
            # (url_a, url_b) are SUPPOSED to differ from each other and
            # from the canonical target — that's the entire mechanism of
            # an IDOR comparison test (same endpoint, two different id
            # values, diff the responses). The generic branch below tells
            # the model to reuse the canonical target "verbatim,
            # unmodified" — correct for a single-target tool, actively
            # wrong here, and was observed causing the model to abandon
            # diff_requests entirely on its next attempt (falling back to
            # re-running arjun with an empty reason) rather than retry
            # with a fixed URL. Give the real fix instead: correct
            # query-string syntax, anchored to the canonical target.
            return (
                f"Your previous next_action was REJECTED by scope enforcement: "
                f"the value {value!r} you gave for params[{key!r}] is not in "
                f"scope. For diff_requests, url_a and url_b are SUPPOSED to "
                f"differ from each other — that's the whole point, same "
                f"endpoint with two different id values, compare the "
                f"responses — so don't just reuse the canonical target "
                f"unmodified for both. The likely problem is query-string "
                f"syntax: a URL has exactly ONE '?', and every parameter "
                f"after the first is joined with '&', never a second '?'. "
                f"The canonical target is exactly {canonical_target!r} — "
                f"build url_a and url_b by appending '&paramname=value1' and "
                f"'&paramname=value2' to that exact string, not by replacing "
                f"or duplicating its existing '?'."
            )

        return (
            f"Your previous next_action was REJECTED by scope enforcement: "
            f"the value {value!r} you gave for params[{key!r}] "
            f"is not in scope. This almost always means the target was "
            f"retyped from memory, shortened, or invented instead of copied "
            f"verbatim. The canonical target is exactly: {canonical_target!r}. "
            f"Use that exact string this time, completely unmodified, in "
            f"whichever param your chosen tool expects it."
        )

    def decide(self, next_action: dict | None, target_hint: str | None,
               top_hypothesis_id: str | None) -> Decision | None:
        self.last_block_reason = None  # reset every call — stale reasons from
        # a prior cycle must never leak into this cycle's retry logic.
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
            self.last_block_reason = {"key": "target_hint", "value": target_hint, "tool": tool}
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
                self.last_block_reason = {"key": key, "value": value, "tool": tool}
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