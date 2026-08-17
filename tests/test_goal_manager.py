"""Tests for GoalManager — particularly the scope-validation added after a
real failure: a malformed scope.yaml (nested list instead of flat strings
under in_scope/out_of_scope) used to crash deep inside fnmatch.fnmatch()
with a cryptic 'expected str, ... not list' TypeError on the first cycle,
instead of failing clearly at startup.
"""
import pytest

from src.planner.goal_manager import GoalManager


def _scope(**overrides):
    base = {
        "program_name": "local-lab",
        "in_scope": ["192.168.56.101", "192.168.56.102"],
        "out_of_scope": [],
        "forbidden_techniques": ["denial_of_service"],
        "rate_limit": {"requests_per_second": 5},
    }
    base.update(overrides)
    return base


def test_valid_scope_constructs_successfully():
    gm = GoalManager(_scope())
    assert gm.program_name == "local-lab"
    assert gm.is_in_scope("192.168.56.101") is True
    assert gm.is_in_scope("192.168.56.999") is False


def test_empty_in_scope_is_rejected():
    with pytest.raises(ValueError, match="no in_scope entries"):
        GoalManager(_scope(in_scope=[]))


def test_nested_list_in_in_scope_fails_clearly_at_construction():
    # This is the exact real-world failure: an indentation slip in
    # scope.yaml nests a list inside in_scope instead of a flat list of
    # strings. Must fail HERE with a clear message, not later inside
    # fnmatch.fnmatch() during a live cognitive cycle.
    malformed = _scope(in_scope=[["192.168.56.101", "192.168.56.102"]])
    with pytest.raises(ValueError, match="must be a flat list of strings"):
        GoalManager(malformed)


def test_nested_list_in_out_of_scope_also_fails_clearly():
    malformed = _scope(out_of_scope=[["10.0.0.1"]])
    with pytest.raises(ValueError, match="must be a flat list of strings"):
        GoalManager(malformed)


def test_non_string_scalar_in_scope_also_fails_clearly():
    # e.g. an unquoted number in YAML parsing as an int, not a str
    malformed = _scope(in_scope=[192, "192.168.56.102"])
    with pytest.raises(ValueError, match="must be a flat list of strings"):
        GoalManager(malformed)


def test_out_of_scope_takes_precedence_over_in_scope():
    gm = GoalManager(_scope(
        in_scope=["192.168.56.*"],
        out_of_scope=["192.168.56.254"],
    ))
    assert gm.is_in_scope("192.168.56.10") is True
    assert gm.is_in_scope("192.168.56.254") is False


def test_is_technique_allowed():
    gm = GoalManager(_scope(forbidden_techniques=["denial_of_service", "social_engineering"]))
    assert gm.is_technique_allowed("denial_of_service") is False
    assert gm.is_technique_allowed("recon") is True


def test_coverage_percent():
    gm = GoalManager(_scope())
    gm.mark_tested("auth")
    gm.mark_tested("idor")
    assert gm.coverage_percent(["auth", "idor", "xss", "csrf"]) == 50.0
    assert gm.coverage_percent([]) == 0.0


def test_session_auth_ground_truth_is_readable():
    # Regression test: this field was previously parsed nowhere — present
    # in scope.yaml but silently discarded, so it never reached the model
    # despite being written specifically to ground auth/session hypothesis
    # generation. Guards against it going inert again.
    truth = {
        "session_cookie_name": "PHPSESSID",
        "secondary_auth_cookie": "uid",
        "account_lockout_present": False,
    }
    gm = GoalManager(_scope(session_auth_ground_truth=truth))
    assert gm.session_auth_ground_truth == truth


def test_session_auth_ground_truth_defaults_to_empty_dict():
    gm = GoalManager(_scope())
    assert gm.session_auth_ground_truth == {}


def test_url_structure_ground_truth_is_readable():
    # Regression test: same class of bug as session_auth_ground_truth —
    # this field exists to stop the model re-guessing a wrong URL shape
    # (direct path instead of index.php?page=) on every new page name, but
    # only helps if it actually reaches GoalManager/the prompt.
    truth = {
        "correct_pattern": "http://x/index.php?page=<page-name>.php",
        "wrong_pattern_example": "http://x/<page-name>.php",
    }
    gm = GoalManager(_scope(url_structure_ground_truth=truth))
    assert gm.url_structure_ground_truth == truth


def test_url_structure_ground_truth_defaults_to_empty_dict():
    gm = GoalManager(_scope())
    assert gm.url_structure_ground_truth == {}


def test_lab_setup_ground_truth_is_readable():
    # Regression test: session 41 initially misdiagnosed a missing-table
    # SQL error as "DB never initialized" (wrong — set-up-database.php
    # ran cleanly every time). The real cause was a db-name mismatch in
    # config.inc ('metasploit' vs the 'owasp10' the reset script
    # actually creates), fixed directly on the target. This field exists
    # so the model knows that history and doesn't misdiagnose it again,
    # but only helps if it actually reaches GoalManager/the prompt.
    truth = {
        "db_setup_page": "http://x/index.php?page=set-up-database.php",
        "historical_error_now_fixed": "Table 'metasploit.accounts' doesn't exist",
        "fix_applied": "config.inc $dbname corrected from 'metasploit' to 'owasp10'",
    }
    gm = GoalManager(_scope(lab_setup_ground_truth=truth))
    assert gm.lab_setup_ground_truth == truth


def test_lab_setup_ground_truth_defaults_to_empty_dict():
    gm = GoalManager(_scope())
    assert gm.lab_setup_ground_truth == {}