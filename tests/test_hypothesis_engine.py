from src.planner.hypothesis_engine import HypothesisEngine, HypothesisStatus


def test_ingest_handles_word_confidence_without_crashing():
    """Regression test for the actual crash (session 44, cycle 5):
    qwen3:4b returned {"confidence": "low"} — a bare float() on that raised
    ValueError and killed the entire run, not just that hypothesis."""
    engine = HypothesisEngine()
    [h] = engine.ingest([
        {"observation": "obs", "attack_strategy": "strat", "confidence": "low"},
    ])
    assert h.confidence == 0.25


def test_ingest_handles_unparseable_confidence_without_crashing():
    engine = HypothesisEngine()
    [h] = engine.ingest([
        {"observation": "obs", "attack_strategy": "strat", "confidence": "extremely likely!!"},
    ])
    assert h.confidence == 0.0


def test_ingest_isolates_malformed_hypothesis_keeps_the_rest():
    """A batch with one incomplete/bad hypothesis must not discard the
    well-formed ones around it — same principle as the confidence-crash
    fix: one bad entry from the model shouldn't cost the whole cycle."""
    engine = HypothesisEngine()
    created = engine.ingest([
        {"observation": "good one", "attack_strategy": "x", "confidence": 0.6},
        {"observation": None, "attack_strategy": "y", "confidence": 0.5},  # bad type
        {"observation": "another good one", "attack_strategy": "z", "confidence": "high"},
    ])
    assert len(created) == 2
    assert created[1].confidence == 0.75


def test_ingest_captures_category():
    engine = HypothesisEngine()
    [h] = engine.ingest([
        {"observation": "obs", "attack_strategy": "strat", "confidence": 0.6,
         "category": "SQL_Injection"},
    ])
    assert h.category == "sql_injection"  # normalized to lowercase


def test_ingest_leaves_category_none_when_omitted():
    engine = HypothesisEngine()
    [h] = engine.ingest([
        {"observation": "obs", "attack_strategy": "strat", "confidence": 0.6},
    ])
    assert h.category is None


def test_ingest_overrides_category_when_text_signals_a_different_specific_category():
    """Regression test for session 45, cycle 5: the model tagged a hypothesis
    'authentication' while its own text was plainly about IDOR ("identify
    potential IDOR vectors... user_id, session tokens"), letting it slip
    past decision_engine's category_out_of_scope gate undetected. The
    hypothesis's own text must win over a mislabeled self-reported tag."""
    engine = HypothesisEngine()
    [h] = engine.ingest([
        {"observation": "The login page contains hidden parameters that "
                         "include user IDs, which could be manipulated to "
                         "cause IDOR.",
         "attack_strategy": "Discover hidden/undocumented parameters to "
                             "identify potential IDOR vectors",
         "confidence": 0.5, "category": "authentication"},
    ])
    assert h.category == "idor_bola"


def test_ingest_keeps_self_reported_category_when_text_gives_no_specific_signal():
    """No specific alias hit in the text -> trust the model's own tag,
    never fabricate a category from generic wording."""
    engine = HypothesisEngine()
    [h] = engine.ingest([
        {"observation": "The endpoint behaves unexpectedly under load",
         "attack_strategy": "Send a crafted request and compare responses",
         "confidence": 0.5, "category": "authentication"},
    ])
    assert h.category == "authentication"


def test_ingest_keeps_self_reported_category_when_text_only_has_a_broad_alias_hit():
    """A broad/generic alias (e.g. 'session') appearing incidentally in the
    text is too weak a signal to override an explicit, specific self-report."""
    engine = HypothesisEngine()
    [h] = engine.ingest([
        {"observation": "The session cookie may not be validated correctly",
         "attack_strategy": "Attempt SQL injection in the username field",
         "confidence": 0.5, "category": "sql_injection"},
    ])
    assert h.category == "sql_injection"


def test_ingest_does_not_override_on_unrelated_category_technique_overlap():
    """Regression guard: a legitimately-tagged sql_injection hypothesis that
    happens to describe its technique as an 'auth bypass payload' must NOT
    get relabeled to authentication. The override is intentionally scoped
    to the one observed laundering pattern (idor_bola), not every alias in
    the shared classification table — anything broader risks flip-flopping
    correctly-tagged hypotheses in other categories."""
    engine = HypothesisEngine()
    [h] = engine.ingest([
        {"observation": "login form may be injectable",
         "attack_strategy": "auth bypass payload",
         "confidence": 0.3, "category": "sql_injection"},
    ])
    assert h.category == "sql_injection"


def test_ingest_fills_in_idor_category_from_text_when_self_report_omitted():
    engine = HypothesisEngine()
    [h] = engine.ingest([
        {"observation": "The endpoint may be vulnerable to IDOR",
         "attack_strategy": "Manipulate the user_id parameter",
         "confidence": 0.5},  # no category given at all
    ])
    assert h.category == "idor_bola"


def test_rank_scope_filter_prefers_matching_category():
    """Core regression test for the goal-drift bug: given a goal scoped to
    sql_injection, a higher-confidence idor_bola hypothesis must NOT
    outrank a lower-confidence sql_injection one."""
    engine = HypothesisEngine()
    engine.ingest([
        {"observation": "hidden param maybe IDOR", "attack_strategy": "arjun discovery",
         "confidence": 0.8, "category": "idor_bola"},
        {"observation": "login form may be injectable", "attack_strategy": "auth bypass payload",
         "confidence": 0.3, "category": "sql_injection"},
    ])
    ranked = engine.rank(scope_categories=["sql_injection"])
    assert ranked[0].category == "sql_injection"


def test_rank_scope_filter_falls_back_when_nothing_matches():
    """An over-eager scope filter must never fully stall the cycle."""
    engine = HypothesisEngine()
    engine.ingest([
        {"observation": "a", "attack_strategy": "x", "confidence": 0.4, "category": "xss"},
    ])
    ranked = engine.rank(scope_categories=["sql_injection"])
    assert len(ranked) == 1
    assert ranked[0].category == "xss"


def test_rank_scope_filter_includes_untagged_hypotheses():
    """Untagged (category=None) hypotheses are ambiguous, not excluded."""
    engine = HypothesisEngine()
    engine.ingest([
        {"observation": "a", "attack_strategy": "x", "confidence": 0.9},  # no category
        {"observation": "b", "attack_strategy": "y", "confidence": 0.2, "category": "idor_bola"},
    ])
    ranked = engine.rank(scope_categories=["sql_injection"])
    assert len(ranked) == 1
    assert ranked[0].category is None


def test_ingest_rejects_incomplete_hypotheses():
    engine = HypothesisEngine()
    created = engine.ingest([
        {"observation": "obs", "attack_strategy": "strat", "confidence": 0.6, "knowledge_grounded": True},
        {"observation": "obs only"},  # incomplete — must be rejected
    ])
    assert len(created) == 1


def test_rank_orders_by_confidence_and_grounding():
    engine = HypothesisEngine()
    engine.ingest([
        {"observation": "a", "attack_strategy": "x", "confidence": 0.5, "knowledge_grounded": False},
        {"observation": "b", "attack_strategy": "y", "confidence": 0.5, "knowledge_grounded": True},
    ])
    ranked = engine.rank()
    assert ranked[0].knowledge_grounded is True


def test_record_result_rejects_after_max_retries():
    engine = HypothesisEngine(max_retries=2)
    [h] = engine.ingest([{"observation": "a", "attack_strategy": "x", "confidence": 0.5}])
    engine.record_result(h.id, confirmed=False)
    engine.record_result(h.id, confirmed=False)
    assert h.status == HypothesisStatus.REJECTED


def test_partial_recorded_defaults_false_and_is_mutable_in_place():
    # planner.py relies on `top` being a live reference into the engine's
    # internal store so that setting `partial_recorded = True` after a
    # mid-flight "partial" experience is recorded actually persists and
    # prevents duplicate recording on the hypothesis's next retry cycle.
    engine = HypothesisEngine(max_retries=3)
    [h] = engine.ingest([{"observation": "a", "attack_strategy": "x", "confidence": 0.5}])
    assert h.partial_recorded is False

    engine.record_result(h.id, confirmed=False)  # -> needs_more_evidence
    assert h.status == HypothesisStatus.NEEDS_MORE_EVIDENCE

    h.partial_recorded = True
    same_object = engine._store[h.id]
    assert same_object.partial_recorded is True