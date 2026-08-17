from src.reasoning.prompt_builder import _split_goal_items, build_prompt


def test_system_identity_universal_mode_has_no_fixed_category_bias():
    """Regression test for the actual root cause of the SQLi goal producing
    only IDOR hypotheses: SYSTEM_IDENTITY must not permanently name IDOR/
    BOLA (or any class) as the agent's specialty when no scope is given."""
    messages = build_prompt(
        current_goal="Test SQL injection on the login form",
        scope={}, working_memory={}, retrieved_knowledge=[],
        active_hypotheses=[], available_tools=[], resource_status={},
        scope_categories=None,
    )
    content = messages[0]["content"]
    assert "no fixed vulnerability-class specialty" in content


def test_system_identity_scoped_mode_names_only_given_categories():
    messages = build_prompt(
        current_goal="Test SQL injection on the login form",
        scope={}, working_memory={}, retrieved_knowledge=[],
        active_hypotheses=[], available_tools=[], resource_status={},
        scope_categories=["sql_injection"],
    )
    content = messages[0]["content"]
    identity_section = content.split("# System Identity")[1].split("# Mission")[0]
    assert "focused specifically on: sql injection" in identity_section
    assert "idor" not in identity_section.lower().split("do not pivot")[0]


def test_output_format_requires_hypothesis_category():
    messages = build_prompt(
        current_goal="Find IDOR in the blog endpoint",
        scope={}, working_memory={}, retrieved_knowledge=[],
        active_hypotheses=[], available_tools=[], resource_status={},
    )
    content = messages[0]["content"]
    assert '"category"' in content


def test_split_goal_items_multi_clause():
    goal = (
        "predictable or non-rotating session tokens, authentication bypass "
        "via direct URL access or cookie/parameter manipulation, weak "
        "password reset token handling, and missing account lockout on "
        "repeated failed logins"
    )
    items = _split_goal_items(goal)
    assert len(items) == 4
    assert items[0] == "predictable or non-rotating session tokens"
    # leading "and " stripped from the final item only
    assert items[-1] == "missing account lockout on repeated failed logins"
    assert not items[-1].lower().startswith("and ")


def test_split_goal_items_single_clause_goal_unchanged():
    goal = "Find and confirm SSRF in the webhook URL field"
    items = _split_goal_items(goal)
    # no commas -> conservatively treated as one item, not split on " and "
    assert items == [goal]


def test_build_prompt_omits_checklist_for_single_item_goal():
    messages = build_prompt(
        current_goal="Find IDOR in the blog endpoint",
        scope={}, working_memory={}, retrieved_knowledge=[],
        active_hypotheses=[], available_tools=[], resource_status={},
    )
    assert "# Goal Checklist" not in messages[0]["content"]


def test_build_prompt_includes_checklist_for_multi_item_goal():
    messages = build_prompt(
        current_goal="Test IDOR on blog posts, and test IDOR on credit card records",
        scope={}, working_memory={}, retrieved_knowledge=[],
        active_hypotheses=[], available_tools=[], resource_status={},
    )
    content = messages[0]["content"]
    assert "# Goal Checklist" in content
    assert "Test IDOR on blog posts" in content
    assert "test IDOR on credit card records" in content
    # checklist must appear before Required Output Format (recency-zone placement)
    assert content.index("# Goal Checklist") < content.index("# Required Output Format")


def test_system_identity_explicitly_instructs_url_structure_ground_truth():
    # Regression test: url_structure_ground_truth existed in scope.yaml and was
    # threaded through goal_manager/planner correctly, but SYSTEM_IDENTITY never
    # told the model to actually apply it — it just sat as passive JSON in the
    # dumped # Scope block. The 4B model ignored it and guessed a wrong direct
    # path 3 cycles running (session 41 resume), burning ~59 minutes for zero
    # progress. Every *_ground_truth field needs an explicit instruction, not
    # just a place in the scope dict.
    from src.reasoning.prompt_builder import SYSTEM_IDENTITY
    assert "url_structure_ground_truth" in SYSTEM_IDENTITY
    assert "correct_pattern" in SYSTEM_IDENTITY


def test_all_ground_truth_scope_keys_have_explicit_instructions():
    # Broader guard against the same class of gap recurring for a future
    # ground-truth field: every key ending in _ground_truth that we actually
    # populate in config/scope.yaml must be named in SYSTEM_IDENTITY.
    import re
    from pathlib import Path
    from src.reasoning.prompt_builder import SYSTEM_IDENTITY

    scope_yaml = Path(__file__).resolve().parents[1] / "config" / "scope.yaml"
    keys = set(re.findall(r"^(\w+_ground_truth):", scope_yaml.read_text(), re.MULTILINE))
    assert keys, "expected at least one *_ground_truth key in scope.yaml"
    missing = [k for k in keys if k not in SYSTEM_IDENTITY]
    assert not missing, f"ground-truth keys missing an explicit prompt instruction: {missing}"


def test_available_tools_is_in_the_truncation_protected_tail():
    # Regression test: 2026-08-16, session 42. context_window was lowered
    # 8192 -> 3072 to fix VRAM-spillover latency (worked — cut per-call
    # time roughly 3-4x). But Available Tools was still positioned early
    # in the prompt at the time, and Ollama's num_ctx truncation drops
    # from the FRONT with no warning. On cycles with enough accumulated
    # Scope/Knowledge/Experience content, Available Tools got truncated
    # out entirely — the model, unable to see its real tools, hallucinated
    # tool names ('recon', 'con') that don't exist. Every cycle that hit
    # this failed outright (unknown tool). Available Tools must stay
    # adjacent to Target in the protected tail, not just "somewhere
    # before Target" — verified here by checking it's within the last
    # two sections rather than merely appearing before Target anywhere
    # in a long section list, since "appears before" alone doesn't
    # guarantee it survives truncation if a lot of front-loaded content
    # sits between it and Target.
    messages = build_prompt(
        current_goal="goal", scope={}, working_memory={}, retrieved_knowledge=[],
        active_hypotheses=[], resource_status={}, available_tools=[{"name": "httpx"}],
        target="http://x",
    )
    content = messages[0]["content"]
    tools_idx = content.index("# Available Tools")
    target_idx = content.index("# Target")
    output_format_idx = content.index("# Required Output Format")
    # Available Tools must come after every other major section (i.e. be
    # in the tail), and specifically be the section immediately
    # preceding Target — not separated from it by Resource Status or
    # anything else that could grow large enough to push it back out of
    # a truncated window.
    assert tools_idx < target_idx < output_format_idx
    between = content[tools_idx:target_idx]
    # Nothing but the Available Tools section body itself should sit
    # between the two headers (i.e. no OTHER "# Something" header
    # appears after this one and before Target).
    assert between.count("\n# ") == 0


def test_available_tools_says_list_is_authoritative():
    # The model needs to be told explicitly not to invent tool names —
    # this is what should have stopped the 'recon'/'con' hallucination
    # even on a cycle where truncation pressure was borderline.
    messages = build_prompt(
        current_goal="goal", scope={}, working_memory={}, retrieved_knowledge=[],
        active_hypotheses=[], resource_status={}, available_tools=[{"name": "httpx"}],
    )
    content = messages[0]["content"]
    tools_section = content[content.index("# Available Tools"):content.index("# Target")]
    assert "authoritative" in tools_section.lower()
    assert "does not exist" in tools_section.lower() or "do not invent" in tools_section.lower()

def test_summarize_recon_facts_keeps_only_most_recent_per_tool_target():
    from src.reasoning.prompt_builder import summarize_recon_facts
    history = [
        {"tool": "arjun", "cycle": 3, "params": {"target": "http://x/login.php"},
         "summary": "0 hidden parameters found"},
        {"tool": "arjun", "cycle": 5, "params": {"target": "http://x/login.php"},
         "summary": "0 hidden parameters found (re-run, same result)"},
    ]
    result = summarize_recon_facts(history)
    assert result.count("arjun on http://x/login.php") == 1
    assert "cycle 5" in result
    assert "cycle 3" not in result


def test_summarize_recon_facts_ignores_non_recon_tools():
    from src.reasoning.prompt_builder import summarize_recon_facts
    history = [
        {"tool": "diff_requests", "cycle": 2, "params": {"url_a": "http://x/a", "url_b": "http://x/b"},
         "summary": "bodies identical"},
    ]
    assert summarize_recon_facts(history) == "(no recon-tool results recorded yet for this session)"


def test_summarize_recon_facts_empty_history():
    from src.reasoning.prompt_builder import summarize_recon_facts
    assert summarize_recon_facts([]) == "(no recon-tool results recorded yet for this session)"


def test_summarize_recon_facts_distinguishes_different_targets():
    from src.reasoning.prompt_builder import summarize_recon_facts
    history = [
        {"tool": "arjun", "cycle": 1, "params": {"target": "http://x/login.php"}, "summary": "0 found"},
        {"tool": "arjun", "cycle": 2, "params": {"target": "http://x/user-info.php"}, "summary": "1 found: id"},
    ]
    result = summarize_recon_facts(history)
    assert "login.php" in result and "user-info.php" in result


def test_known_recon_facts_section_present_and_in_protected_tail():
    # Regression test: session 43 re-ran an identical arjun scan twice
    # despite the raw fact already sitting in Working Memory — burying it
    # in a 50-entry JSON dump wasn't enough. This section pre-extracts
    # and surfaces it in the same protected tail as Available Tools/
    # Target, per the pattern established for both of those.
    messages = build_prompt(
        current_goal="goal", scope={},
        working_memory={"request_history": [
            {"tool": "arjun", "cycle": 3, "params": {"target": "http://x/login.php"},
             "summary": "0 hidden parameters found"},
        ]},
        retrieved_knowledge=[], active_hypotheses=[], resource_status={},
        available_tools=[{"name": "httpx"}], target="http://x",
    )
    content = messages[0]["content"]
    assert "# Known Recon Facts" in content
    assert "arjun on http://x/login.php (cycle 3): 0 hidden parameters found" in content
    facts_idx = content.index("# Known Recon Facts")
    target_idx = content.index("# Target")
    assert facts_idx < target_idx