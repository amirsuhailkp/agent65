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
    def __init__(self, scope_checker, url_rewrite_rules: dict | None = None):
        """scope_checker: callable(target:str) -> bool

        url_rewrite_rules: optional dict shaped like scope.yaml's
        `url_structure_ground_truth` (correct_pattern/wrong_pattern_example
        using a `<page-name>` placeholder). When set, a target/url param
        that fails scope_checker AND matches the wrong-pattern shape gets
        deterministically rewritten to the correct-pattern shape and
        re-checked, rather than being blocked outright.

        This exists because relying on a prompt instruction alone to stop
        the model guessing a bare-path URL failed in practice: stale
        experience/hypothesis records already contain the wrong literal
        URL as concrete text, which a small model reliably prefers over an
        abstract system-prompt rule. Six full retry-cycles were burned
        this way across three separate sessions (view-someones-blog.php
        x2, profile.php x4) before this deterministic fix was added.
        Fixing it in code costs zero LLM calls and can't be out-attended.
        """
        self.scope_checker = scope_checker
        self.url_rewrite_rules = url_rewrite_rules or {}
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
        kind = block.get("kind")

        if kind == "malformed_query":
            key, value, tool = block["key"], block["value"], block.get("tool")
            return (
                f"Your previous next_action was REJECTED: the value {value!r} "
                f"you gave for params[{key!r}] has a malformed query string — "
                f"it contains more than one '?'. A URL has exactly ONE '?'; "
                f"every parameter after the first must be joined with '&', "
                f"never a second '?'. This isn't just a style issue: a "
                f"second '?' does NOT start a new parameter — everything "
                f"after the first '?' (including that second '?' itself) "
                f"gets treated as part of the FIRST parameter's value, so "
                f"your test silently tests nothing at all. The canonical "
                f"target is exactly {canonical_target!r} — append your "
                f"parameter as '&paramname=value' directly onto that exact "
                f"string."
            )

        if kind == "duplicate_action":
            tool, params = block["tool"], block["params"]
            prior_cycle = block.get("prior_cycle")
            prior_summary = block.get("prior_summary") or "(no summary recorded)"
            return (
                f"Your previous next_action was REJECTED: you already ran "
                f"tool={tool!r} with these EXACT params {params!r} at cycle "
                f"{prior_cycle} — running it again will produce the "
                f"identical result, not new evidence. That prior result "
                f"was: {prior_summary!r}. Pick a genuinely different next "
                f"step: a different parameter NAME (not just a different "
                f"value — if you tried 'user_id', consider a name "
                f"mentioned explicitly in prior evidence instead), a "
                f"different tool, or a different endpoint."
            )

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

    def _try_rewrite_url(self, value: str) -> str | None:
        """If value matches url_rewrite_rules' wrong-pattern shape, return
        the corrected value built from correct_pattern. Returns None if
        rules aren't configured or value doesn't match the wrong shape.
        """
        import re
        wrong = self.url_rewrite_rules.get("wrong_pattern_example")
        correct = self.url_rewrite_rules.get("correct_pattern")
        if not wrong or not correct or "<page-name>" not in wrong or "<page-name>" not in correct:
            return None
        # Build a regex from wrong_pattern_example by escaping everything
        # except the <page-name> placeholder, which becomes a capture group.
        pattern = "^" + re.escape(wrong).replace(re.escape("<page-name>"), r"([\w\-/]+)") + r"(\?.*)?$"
        m = re.match(pattern, value)
        if not m:
            return None
        page_name, query = m.group(1), (m.group(2) or "")
        rewritten = correct.replace("<page-name>", page_name)
        # Preserve any extra query string already present, appended with &
        if query:
            rewritten += "&" + query.lstrip("?")
        return rewritten

    def decide(self, next_action: dict | None, target_hint: str | None,
               top_hypothesis_id: str | None,
               recent_actions: list[dict] | None = None) -> Decision | None:
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
            if not isinstance(value, str) or not value:
                continue
            # Checked BEFORE scope: a malformed URL can still accidentally
            # pass a wildcard scope pattern (fnmatch's '*' swallows
            # anything after it) while being functionally broken. Observed
            # case: params['target']='...view-someones-blog.php?user_id=1'
            # (a SECOND '?') passed scope fine, dispatched fine, and
            # silently tested nothing — the target app treats everything
            # after the first '?' as part of the FIRST param's value, so
            # this wasn't really testing user_id at all. It just looked
            # like a normal completed cycle. Scope enforcement alone can't
            # catch this since it's a syntax bug, not an authorization one.
            if value.count("?") > 1:
                log.warning(
                    f"BLOCKED: params['{key}']={value!r} has a malformed "
                    f"query string (more than one '?') (tool={tool})"
                )
                self.last_block_reason = {
                    "key": key, "value": value, "tool": tool, "kind": "malformed_query",
                }
                return None
            if not self.scope_checker(value):
                rewritten = self._try_rewrite_url(value)
                if rewritten and self.scope_checker(rewritten):
                    log.info(
                        f"AUTO-CORRECTED: params['{key}']={value!r} -> "
                        f"{rewritten!r} (matched known wrong-pattern shape, "
                        f"rewritten to canonical URL structure, tool={tool})"
                    )
                    params[key] = rewritten
                    continue
                log.warning(f"BLOCKED: params['{key}']={value!r} out of scope (tool={tool})")
                self.last_block_reason = {"key": key, "value": value, "tool": tool}
                return None

        # Duplicate-action guard: request_history is already in the prompt,
        # but observed behavior was the model re-running an EXACT already-
        # answered diff_requests comparison three cycles running, identical
        # result each time — expecting a 4B model to notice one exact-match
        # entry among up to 50 JSON blobs and treat that as decisive is the
        # same mistake as burying Target/Correction early in a long prompt.
        # Deterministic and cheap to catch here instead of hoping it's
        # attended to.
        #
        # `params` deliberately NOT required to be truthy here (was
        # `if recent_actions and params:` until 2026-08-16) — an empty
        # dict is falsy in Python, so any tool call relying entirely on
        # defaults (params={}) silently bypassed this whole guard. That's
        # exactly how session 43 re-ran an identical `arjun` scan on the
        # same endpoint twice (cycles 3 and 5) despite the tool's own
        # first-run output explicitly saying re-running it wouldn't find
        # anything new — the guard never even evaluated the comparison
        # because `params` was `{}`. `tool is not None` is the real
        # precondition; an empty params dict is still a valid, comparable
        # value and should be deduped just like any other.
        if recent_actions and tool is not None:
            for entry in recent_actions:
                if entry.get("tool") == tool and entry.get("params") == params:
                    log.warning(
                        f"BLOCKED: duplicate action tool={tool} params={params} "
                        f"already run at cycle {entry.get('cycle')}"
                    )
                    self.last_block_reason = {
                        "kind": "duplicate_action", "tool": tool, "params": params,
                        "prior_cycle": entry.get("cycle"), "prior_summary": entry.get("summary"),
                    }
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