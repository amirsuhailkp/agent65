from src.reasoning.prompt_builder import _split_goal_items, build_prompt


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