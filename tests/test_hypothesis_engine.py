from src.planner.hypothesis_engine import HypothesisEngine, HypothesisStatus


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