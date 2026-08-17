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


def test_unknown_tool_blocks_and_records_reason():
    """Regression test (session 45, cycle 5): the model invented a tool
    called "auth" that isn't in the registry. Previously this sailed
    through decide(), dispatched, and failed downstream with 'unknown
    tool' — wasting the whole cycle's LLM call + impact assessment for
    zero evidence. Must be caught here instead, before it becomes a
    Decision."""
    de = DecisionEngine(scope_checker=IN_SCOPE, valid_tools={"httpx", "diff_requests", "arjun"})
    result = de.decide(
        next_action={"tool": "auth", "params": {"username": "admin", "password": "admin"},
                     "reason": "try default creds", "risk_level": "medium"},
        target_hint="http://192.168.56.101/mutillidae",
        top_hypothesis_id="hyp_1",
    )
    assert result is None
    assert de.last_block_reason["kind"] == "unknown_tool"


def test_known_tool_passes_when_valid_tools_set():
    de = DecisionEngine(scope_checker=IN_SCOPE, valid_tools={"httpx", "diff_requests"})
    result = de.decide(
        next_action={"tool": "httpx", "params": {"target": "http://192.168.56.101/x"},
                     "reason": "r", "risk_level": "low"},
        target_hint="http://192.168.56.101/mutillidae",
        top_hypothesis_id="hyp_1",
    )
    assert result is not None


def test_no_valid_tools_set_never_blocks_on_tool_name():
    """Backward compatibility: callers that don't pass a registry (or in
    tests) must see identical behavior to before this fix."""
    de = DecisionEngine(scope_checker=IN_SCOPE)
    result = de.decide(
        next_action={"tool": "anything_at_all", "params": {"target": "http://192.168.56.101/x"},
                     "reason": "r", "risk_level": "low"},
        target_hint="http://192.168.56.101/mutillidae",
        top_hypothesis_id="hyp_1",
    )
    assert result is not None


def test_correction_message_for_unknown_tool_lists_valid_tools():
    de = DecisionEngine(scope_checker=IN_SCOPE, valid_tools={"httpx", "diff_requests"})
    de.decide(
        next_action={"tool": "auth", "params": {}, "reason": "r", "risk_level": "low"},
        target_hint="http://192.168.56.101/mutillidae",
        top_hypothesis_id="hyp_1",
    )
    msg = de.correction_message("http://192.168.56.101/mutillidae")
    assert "httpx" in msg
    assert "diff_requests" in msg
    assert "'auth'" in msg


def test_hypothesis_category_out_of_scope_blocks_and_records_reason():
    """Regression test for the hard-gate fix: even a single, otherwise-valid
    hypothesis must be blocked if its declared category isn't in scope —
    HypothesisEngine.rank()'s soft preference alone can't catch this when
    the model only proposes one hypothesis (observed: session 44, an
    idor_bola-tagged arjun call sailed through a sql_injection-scoped run)."""
    de = DecisionEngine(scope_checker=IN_SCOPE)
    result = de.decide(
        next_action={"tool": "arjun", "params": {"target": "http://192.168.56.101/x"},
                     "reason": "discover hidden params", "risk_level": "low"},
        target_hint="http://192.168.56.101/mutillidae",
        top_hypothesis_id="hyp_1",
        hypothesis_category="idor_bola",
        scope_categories=["sql_injection", "authentication"],
    )
    assert result is None
    assert de.last_block_reason["kind"] == "category_out_of_scope"


def test_hypothesis_category_in_scope_passes():
    de = DecisionEngine(scope_checker=IN_SCOPE)
    result = de.decide(
        next_action={"tool": "diff_requests", "params": {"url_a": "http://192.168.56.101/a",
                                                           "url_b": "http://192.168.56.101/b"},
                     "reason": "test sqli payload", "risk_level": "low"},
        target_hint="http://192.168.56.101/mutillidae",
        top_hypothesis_id="hyp_1",
        hypothesis_category="sql_injection",
        scope_categories=["sql_injection", "authentication"],
    )
    assert result is not None


def test_no_scope_categories_never_blocks_on_category():
    """Universal mode (no scope given) must be completely unaffected."""
    de = DecisionEngine(scope_checker=IN_SCOPE)
    result = de.decide(
        next_action={"tool": "arjun", "params": {"target": "http://192.168.56.101/x"},
                     "reason": "r", "risk_level": "low"},
        target_hint="http://192.168.56.101/mutillidae",
        top_hypothesis_id="hyp_1",
        hypothesis_category="idor_bola",
        scope_categories=None,
    )
    assert result is not None


def test_untagged_hypothesis_never_blocks_on_category():
    """A hypothesis with no category (older/malformed model response) is
    ambiguous, not out-of-scope — must not be blocked."""
    de = DecisionEngine(scope_checker=IN_SCOPE)
    result = de.decide(
        next_action={"tool": "httpx", "params": {"target": "http://192.168.56.101/x"},
                     "reason": "r", "risk_level": "low"},
        target_hint="http://192.168.56.101/mutillidae",
        top_hypothesis_id="hyp_1",
        hypothesis_category=None,
        scope_categories=["sql_injection"],
    )
    assert result is not None


def test_correction_message_for_category_out_of_scope_names_allowed_categories():
    de = DecisionEngine(scope_checker=IN_SCOPE)
    de.decide(
        next_action={"tool": "arjun", "params": {"target": "http://192.168.56.101/x"},
                     "reason": "r", "risk_level": "low"},
        target_hint="http://192.168.56.101/mutillidae",
        top_hypothesis_id="hyp_1",
        hypothesis_category="idor_bola",
        scope_categories=["sql_injection", "authentication"],
    )
    msg = de.correction_message("http://192.168.56.101/mutillidae")
    assert "sql injection" in msg
    assert "authentication" in msg
    assert "idor_bola" in msg
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


# Realistic Mutillidae scope pattern set — bare /mutillidae/<page>.php paths
# are NOT matched by any of these (only exact "/mutillidae" and the
# index.php?page=* wildcard are), matching config/scope.yaml in production.
MUTILLIDAE_SCOPE = make_scope_checker([
    "192.168.56.101",
    "http://192.168.56.101",
    "http://192.168.56.101/mutillidae",
    "http://192.168.56.101/mutillidae/index.php?page=login.php*",
    "http://192.168.56.101/mutillidae/index.php?page=*",
])

URL_REWRITE_RULES = {
    "correct_pattern": "http://192.168.56.101/mutillidae/index.php?page=<page-name>.php",
    "wrong_pattern_example": "http://192.168.56.101/mutillidae/<page-name>.php",
}


def test_bare_path_url_auto_rewritten_instead_of_blocked():
    # Regression test: this exact bare-path guess for profile.php cost 6
    # full wasted retry-cycles across 3 sessions because a prompt-only
    # instruction couldn't reliably out-compete a stale literal URL
    # already sitting in Relevant Experience text. Fixing it
    # deterministically here means it can never happen again regardless
    # of what the model does or doesn't attend to.
    de = DecisionEngine(scope_checker=MUTILLIDAE_SCOPE, url_rewrite_rules=URL_REWRITE_RULES)
    result = de.decide(
        next_action={
            "tool": "diff_requests",
            "params": {
                "url_a": "http://192.168.56.101/mutillidae/profile.php",
                "url_b": "http://192.168.56.101/mutillidae/profile.php",
                "cookie_a": "uid=admin", "cookie_b": "uid=samurai",
            },
            "reason": "r", "risk_level": "low",
        },
        target_hint="http://192.168.56.101/mutillidae/index.php?page=login.php",
        top_hypothesis_id=None,
    )
    assert result is not None
    assert result.params["url_a"] == "http://192.168.56.101/mutillidae/index.php?page=profile.php"
    assert result.params["url_b"] == "http://192.168.56.101/mutillidae/index.php?page=profile.php"


def test_bare_path_with_existing_query_string_preserved_on_rewrite():
    de = DecisionEngine(scope_checker=MUTILLIDAE_SCOPE, url_rewrite_rules=URL_REWRITE_RULES)
    result = de.decide(
        next_action={
            "tool": "httpx",
            "params": {"target": "http://192.168.56.101/mutillidae/user-info.php?username=admin"},
            "reason": "r", "risk_level": "low",
        },
        target_hint="http://192.168.56.101/mutillidae/index.php?page=login.php",
        top_hypothesis_id=None,
    )
    assert result is not None
    assert result.params["target"] == (
        "http://192.168.56.101/mutillidae/index.php?page=user-info.php&username=admin"
    )


def test_no_rewrite_rules_still_blocks_as_before():
    # Without url_rewrite_rules configured, behavior is unchanged from
    # before this feature existed — still blocks, no crash.
    de = DecisionEngine(scope_checker=MUTILLIDAE_SCOPE)
    result = de.decide(
        next_action={
            "tool": "httpx",
            "params": {"target": "http://192.168.56.101/mutillidae/profile.php"},
            "reason": "r", "risk_level": "low",
        },
        target_hint="http://192.168.56.101/mutillidae/index.php?page=login.php",
        top_hypothesis_id=None,
    )
    assert result is None


def test_rewrite_that_is_still_out_of_scope_stays_blocked():
    # If the rewritten URL is STILL out of scope (e.g. a genuinely
    # different host), don't silently let it through — still block.
    de = DecisionEngine(scope_checker=MUTILLIDAE_SCOPE, url_rewrite_rules=URL_REWRITE_RULES)
    result = de.decide(
        next_action={
            "tool": "httpx",
            "params": {"target": "http://evil.example.com/mutillidae/profile.php"},
            "reason": "r", "risk_level": "low",
        },
        target_hint="http://192.168.56.101/mutillidae/index.php?page=login.php",
        top_hypothesis_id=None,
    )
    assert result is None

def test_duplicate_action_with_nonempty_params_is_blocked():
    de = DecisionEngine(scope_checker=IN_SCOPE)
    prior = [{"cycle": 1, "tool": "httpx", "params": {"target": "http://192.168.56.101/x"}}]
    result = de.decide(
        next_action={
            "tool": "httpx",
            "params": {"target": "http://192.168.56.101/x"},
            "reason": "r", "risk_level": "low",
        },
        target_hint="http://192.168.56.101/mutillidae",
        top_hypothesis_id=None,
        recent_actions=prior,
    )
    assert result is None


def test_duplicate_action_with_empty_params_is_also_blocked():
    # Regression test: session 43 re-ran an identical `arjun` scan on the
    # same endpoint twice (cycles 3 and 5) despite arjun's own cycle-3
    # output explicitly saying a re-run "will not find anything new".
    # Root cause: the old guard was `if recent_actions and params:` —
    # since params={} (a tool relying entirely on defaults) is falsy in
    # Python, the whole duplicate check was silently skipped for any
    # such call, not just arjun. This locks in that an empty params dict
    # is still compared and still blocks a genuine repeat.
    de = DecisionEngine(scope_checker=IN_SCOPE)
    prior = [{"cycle": 3, "tool": "arjun", "params": {}, "summary": "0 hidden parameters found"}]
    result = de.decide(
        next_action={"tool": "arjun", "params": {}, "reason": "r", "risk_level": "low"},
        target_hint="http://192.168.56.101/mutillidae",
        top_hypothesis_id=None,
        recent_actions=prior,
    )
    assert result is None


def test_non_duplicate_action_with_empty_params_is_not_blocked():
    # Different tool, same (empty) params — must NOT be treated as a
    # duplicate just because both params dicts are empty.
    de = DecisionEngine(scope_checker=IN_SCOPE)
    prior = [{"cycle": 3, "tool": "arjun", "params": {}}]
    result = de.decide(
        next_action={"tool": "katana", "params": {}, "reason": "r", "risk_level": "low"},
        target_hint="http://192.168.56.101/mutillidae",
        top_hypothesis_id=None,
        recent_actions=prior,
    )
    assert result is not None