"""Regression tests for DecisionEngine.

No test file existed for this module before — added specifically because
of a real bug: scope checking only ever validated target_hint (the fixed
--target CLI argument), never the actual per-cycle `params` a tool call
would use. A model that picked a different/hallucinated target in params
sailed straight through undetected (observed live: params={'target':
'http://target.com'} while target_hint was still the original in-scope
URL). These tests pin the fixed behavior down.
"""
import fnmatch
import pytest
from src.planner.decision_engine import DecisionEngine


def make_scope_checker(patterns):
    return lambda t: any(fnmatch.fnmatch(t, p) for p in patterns)


IN_SCOPE = make_scope_checker(["192.168.56.101", "http://192.168.56.101*"])


def test_in_scope_target_hint_and_params_passes():
    de = DecisionEngine(scope_checker=IN_SCOPE)
    result = de.decide(
        next_action={"tool": "httpx", "params": {"target": "http://192.168.56.101/x"},
                     "reason": "r", "risk_level": "low"},
        target_hint="http://192.168.56.101/mutillidae",
        top_hypothesis_id=None,
    )
    assert result is not None
    assert result.tool == "httpx"


def test_out_of_scope_target_hint_blocked():
    de = DecisionEngine(scope_checker=IN_SCOPE)
    result = de.decide(
        next_action={"tool": "httpx", "params": {"target": "http://192.168.56.101/x"},
                     "reason": "r", "risk_level": "low"},
        target_hint="http://evil.example.com",
        top_hypothesis_id=None,
    )
    assert result is None


def test_out_of_scope_params_target_blocked_even_when_target_hint_is_in_scope():
    """The actual bug: target_hint in scope, but the tool's own params
    point somewhere else entirely — must be blocked, not silently allowed."""
    de = DecisionEngine(scope_checker=IN_SCOPE)
    result = de.decide(
        next_action={"tool": "arjun", "params": {"target": "http://target.com"},
                     "reason": "r", "risk_level": "low"},
        target_hint="http://192.168.56.101/mutillidae",
        top_hypothesis_id=None,
    )
    assert result is None


def test_diff_requests_url_a_url_b_both_checked():
    de = DecisionEngine(scope_checker=IN_SCOPE)
    # url_b out of scope should block even though url_a is fine
    result = de.decide(
        next_action={
            "tool": "diff_requests",
            "params": {"url_a": "http://192.168.56.101/x?id=1", "url_b": "http://evil.example.com/x?id=2"},
            "reason": "r", "risk_level": "low",
        },
        target_hint="http://192.168.56.101/mutillidae",
        top_hypothesis_id=None,
    )
    assert result is None

    # both in scope should pass
    result2 = de.decide(
        next_action={
            "tool": "diff_requests",
            "params": {"url_a": "http://192.168.56.101/x?id=1", "url_b": "http://192.168.56.101/x?id=2"},
            "reason": "r", "risk_level": "low",
        },
        target_hint="http://192.168.56.101/mutillidae",
        top_hypothesis_id=None,
    )
    assert result2 is not None


def test_non_target_params_not_scope_checked():
    """nuclei's severity/tags are plain strings, not targets — they must
    not be run through scope matching or every nuclei decision would
    false-block."""
    de = DecisionEngine(scope_checker=IN_SCOPE)
    result = de.decide(
        next_action={
            "tool": "nuclei",
            "params": {"target": "http://192.168.56.101", "severity": "high", "tags": "idor,auth"},
            "reason": "r", "risk_level": "medium",
        },
        target_hint="http://192.168.56.101/mutillidae",
        top_hypothesis_id=None,
    )
    assert result is not None


def test_no_next_action_returns_none():
    de = DecisionEngine(scope_checker=IN_SCOPE)
    assert de.decide(next_action=None, target_hint=None, top_hypothesis_id=None) is None
    assert de.decide(next_action={}, target_hint=None, top_hypothesis_id=None) is None


def test_non_dict_next_action_does_not_crash():
    """Regression: a malformed LLM output (next_action as a plain string)
    previously crashed the whole run with AttributeError on .get()."""
    de = DecisionEngine(scope_checker=IN_SCOPE)
    result = de.decide(
        next_action="run httpx on the endpoint",  # type: ignore[arg-type]  # intentionally malformed input under test
        target_hint="http://192.168.56.101/mutillidae",
        top_hypothesis_id=None,
    )
    assert result is None


@pytest.mark.parametrize("malformed_tool", [None, 123, "", "   "])
def test_missing_or_invalid_tool_rejected(malformed_tool):
    """Regression: Decision.tool=None previously passed straight through
    (a Decision object is truthy regardless of its fields) and would only
    fail later, deep inside dispatch — wasting a full cycle (evidence
    collection, impact assessment, hypothesis recording, report
    generation) on a decision with no real tool."""
    de = DecisionEngine(scope_checker=IN_SCOPE)
    result = de.decide(
        next_action={"tool": malformed_tool, "params": {"target": "http://192.168.56.101"},
                     "reason": "r", "risk_level": "low"},
        target_hint="http://192.168.56.101/mutillidae",
        top_hypothesis_id=None,
    )
    assert result is None


def test_missing_tool_key_entirely_rejected():
    de = DecisionEngine(scope_checker=IN_SCOPE)
    result = de.decide(
        next_action={"params": {"target": "http://192.168.56.101"}, "reason": "r", "risk_level": "low"},
        target_hint="http://192.168.56.101/mutillidae",
        top_hypothesis_id=None,
    )
    assert result is None