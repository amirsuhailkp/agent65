from src.planner.hypothesis_engine import HypothesisEngine, HypothesisStatus


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
