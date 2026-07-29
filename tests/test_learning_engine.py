"""Tests for the Playbook Learning Engine — spec compliance checks:
  - never reprocess an unmodified document (Incremental Knowledge Import)
  - never fabricate an observation with no supporting text
  - never let a single report push confidence above the structural cap
  - synthesize (not copy) a playbook from many observations
  - version only on structural change; append-only history
  - experience outcomes become linkable future evidence
"""
import json
import pytest

from src.memory.db_models import get_session_factory
from src.knowledge.repository import KnowledgeRepository, RawKnowledgeDoc
from src.learning.db_models import Observation, Playbook, Experience  # noqa: F401 (registers tables)
from src.learning.incremental_indexer import IncrementalIndexer
from src.learning.observation_extractor import ObservationExtractor, normalize_category
from src.learning.confidence import calculate_confidence
from src.learning.playbook_synthesizer import PlaybookSynthesizer, _merge_workflow, _merge_frequency_list
from src.learning.experience_store import ExperienceStore
from src.learning.learning_engine import LearningEngine
from src.learning.recategorize import recategorize_all


class StubLLM:
    """Duck-typed stand-in for OllamaClient — no real Ollama needed."""
    def __init__(self, responses):
        self._responses = list(responses)

    def chat(self, messages, format=None):
        if not self._responses:
            return json.dumps({"observations": []})
        return self._responses.pop(0)


def _write_doc(tmp_path, name, title, collector="portswigger", body_extra=""):
    (tmp_path / name).write_text(
        "---\n"
        f"title: {title}\n"
        "source: portswigger.net\n"
        "url: https://example.test/x\n"
        f"collector: {collector}\n"
        "category: web-security\n"
        "tags: []\n"
        "date_collected: '2026-01-01T00:00:00Z'\n"
        "language: en\n"
        "---\n\n"
        f"# {title}\n\nBody text.{body_extra}\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------- Incremental Indexer

def test_incremental_indexer_skips_unchanged_documents(tmp_path):
    _write_doc(tmp_path, "a.md", "Doc A")
    db_path = str(tmp_path / "test.db")
    session_factory = get_session_factory(db_path)
    repo = KnowledgeRepository(str(tmp_path))
    indexer = IncrementalIndexer(repo, session_factory)

    pending = indexer.find_pending()
    assert len(pending) == 1
    indexer.mark_indexed(pending[0].doc.doc_id, "a.md", pending[0].sha256, 1)

    # Re-scan with no changes — must be empty (never reprocess).
    assert indexer.find_pending() == []


def test_incremental_indexer_detects_modified_document(tmp_path):
    _write_doc(tmp_path, "a.md", "Doc A")
    db_path = str(tmp_path / "test.db")
    session_factory = get_session_factory(db_path)
    repo = KnowledgeRepository(str(tmp_path))
    indexer = IncrementalIndexer(repo, session_factory)

    [p] = indexer.find_pending()
    indexer.mark_indexed(p.doc.doc_id, "a.md", p.sha256, 1)
    assert indexer.find_pending() == []

    _write_doc(tmp_path, "a.md", "Doc A", body_extra=" Updated content.")
    pending_again = indexer.find_pending()
    assert len(pending_again) == 1  # modified -> must be picked up again


def test_incremental_indexer_only_processes_new_files(tmp_path):
    _write_doc(tmp_path, "a.md", "Doc A")
    db_path = str(tmp_path / "test.db")
    session_factory = get_session_factory(db_path)
    repo = KnowledgeRepository(str(tmp_path))
    indexer = IncrementalIndexer(repo, session_factory)
    [p] = indexer.find_pending()
    indexer.mark_indexed(p.doc.doc_id, "a.md", p.sha256, 1)

    _write_doc(tmp_path, "b.md", "Doc B")
    pending = indexer.find_pending()
    assert len(pending) == 1
    assert pending[0].doc.doc_id == "b"


def test_incremental_indexer_prioritizes_auth_logic_docs_without_excluding_others(tmp_path):
    _write_doc(tmp_path, "a-clickjacking.md", "Clickjacking Defense Cheat Sheet")
    _write_doc(tmp_path, "b-csp.md", "Content Security Policy Cheat Sheet")
    _write_doc(tmp_path, "c-auth.md", "Authentication Bypass via JWT alg none")
    _write_doc(tmp_path, "d-xss.md", "XSS Prevention Cheat Sheet")
    db_path = str(tmp_path / "test.db")
    session_factory = get_session_factory(db_path)
    repo = KnowledgeRepository(str(tmp_path))
    indexer = IncrementalIndexer(repo, session_factory)

    pending = indexer.find_pending()
    doc_ids = [p.doc.doc_id for p in pending]

    assert len(doc_ids) == 4  # nothing excluded — only reordered
    assert doc_ids[0] == "c-auth"  # priority match moved to front
    assert set(doc_ids) == {"a-clickjacking", "b-csp", "c-auth", "d-xss"}


# ---------------------------------------------------------------- Category normalization

@pytest.mark.parametrize("raw,expected", [
    ("IDOR", "idor_bola"),
    ("Sub-domain Takeover", "subdomain_takeover"),
    ("Broken Object Level Authorization", "idor_bola"),
    ("Some Brand New Vuln Class", "some_brand_new_vuln_class"),
    # Compound names (from the extractor's own worked example / real
    # PortSwigger doc titles) must still resolve via substring match,
    # not fragment into a brand new uncategorized slug.
    ("Broken Access Control - Horizontal Privilege Escalation", "idor_bola"),
    ("Testing horizontal access controls", "idor_bola"),
])
def test_normalize_category_maps_compound_names_via_substring(raw, expected):
    assert normalize_category(raw) == expected


# ---------------------------------------------------------------- Observation extraction

def test_extractor_drops_observations_with_no_supporting_text():
    llm = StubLLM([json.dumps({"observations": [
        {"vulnerability": "", "discovery_sequence": []},           # nothing to support it -> drop
        {"vulnerability": "IDOR", "discovery_sequence": ["enum ids"]},  # valid
    ]})])
    extractor = ObservationExtractor(llm)
    doc = RawKnowledgeDoc(doc_id="d1", title="t", source="s", category="c",
                           tags=[], trust_level="verified", technology="")
    results = extractor.extract(doc, "body text")
    assert len(results) == 1
    assert results[0].vulnerability == "IDOR"
    assert results[0].category == "idor_bola"


def test_extractor_returns_empty_on_invalid_json():
    llm = StubLLM(["not json at all"])
    extractor = ObservationExtractor(llm)
    doc = RawKnowledgeDoc(doc_id="d1", title="t", source="s", category="c",
                           tags=[], trust_level="verified", technology="")
    assert extractor.extract(doc, "body") == []


# ---------------------------------------------------------------- Confidence

def test_confidence_never_rises_above_cap_from_one_report():
    c = calculate_confidence(supporting_observations=1, distinct_sources=1,
                              personal_successes=99)  # even with a huge (implausible) bonus
    assert c <= 0.3


def test_confidence_grows_with_more_independent_evidence():
    low = calculate_confidence(supporting_observations=2, distinct_sources=1)
    high = calculate_confidence(supporting_observations=30, distinct_sources=5)
    assert high > low


def test_confidence_penalized_by_contradictions():
    clean = calculate_confidence(supporting_observations=10, distinct_sources=3)
    contradicted = calculate_confidence(supporting_observations=10, distinct_sources=3,
                                         contradictions=5, personal_failures=3)
    assert contradicted < clean


# ---------------------------------------------------------------- Merge helpers

def test_merge_workflow_orders_by_average_position():
    sequences = [
        ["Asset Discovery", "DNS Enumeration", "Verification"],
        ["Asset Discovery", "DNS Enumeration", "Cloud Detection", "Verification"],
        ["Asset Discovery", "DNS Enumeration", "Cloud Detection", "Verification", "Evidence Collection"],
    ]
    merged = _merge_workflow(sequences)
    assert merged[0] == "Asset Discovery"
    assert merged.index("DNS Enumeration") < merged.index("Verification")


def test_merge_frequency_list_ranks_most_common_first():
    merged = _merge_frequency_list([["Burp Suite", "nuclei"], ["Burp Suite"], ["Burp Suite", "ffuf"]])
    assert merged[0] == "Burp Suite"


# ---------------------------------------------------------------- Playbook synthesis

def _make_observation(db, category, source, sequence, tools=None, doc_id="doc1", vuln="IDOR"):
    obs = Observation(
        doc_id=doc_id, source_title="t", source=source, trust_level="verified",
        category=category, vulnerability=vuln, target_technology="",
        preconditions="[]", discovery_sequence=json.dumps(sequence),
        payloads="[]", tool_usage=json.dumps(tools or []), decision_points="[]",
        false_positives="[]", failure_reasons="[]", successful_validation_steps="[]",
        severity="medium", references="[]",
    )
    db.add(obs)
    db.commit()
    db.refresh(obs)
    return obs


def test_synthesize_creates_new_playbook_from_observations(tmp_path):
    session_factory = get_session_factory(str(tmp_path / "t.db"))
    with session_factory() as db:
        _make_observation(db, "idor_bola", "hackerone", ["Enumerate IDs", "Swap ID", "Verify access"],
                           tools=["Burp Suite"], doc_id="d1")
        _make_observation(db, "idor_bola", "bugcrowd", ["Enumerate IDs", "Swap ID"],
                           tools=["Burp Suite"], doc_id="d2")

    synth = PlaybookSynthesizer(session_factory)
    result = synth.synthesize_category("idor_bola")
    assert result["action"] == "created"
    assert result["version"] == 1

    latest = synth.get_latest("idor_bola")
    assert latest is not None
    workflow = json.loads(latest.workflow)
    assert "Enumerate IDs" in workflow
    provenance = json.loads(latest.provenance)
    assert provenance["derived_from"]["hackerone"] == 1
    assert provenance["derived_from"]["bugcrowd"] == 1


def test_synthesize_never_duplicates_playbook_for_same_category(tmp_path):
    session_factory = get_session_factory(str(tmp_path / "t.db"))
    with session_factory() as db:
        _make_observation(db, "idor_bola", "hackerone", ["Enumerate IDs"], doc_id="d1")

    synth = PlaybookSynthesizer(session_factory)
    synth.synthesize_category("idor_bola")
    synth.synthesize_category("idor_bola")  # re-run must not create a second playbook lineage

    with session_factory() as db:
        count = db.query(Playbook).filter(Playbook.playbook_key == "idor_bola").count()
    assert count == 1  # same key, still just one row (no structural change yet)


def test_synthesize_versions_on_structural_change_without_deleting_history(tmp_path):
    session_factory = get_session_factory(str(tmp_path / "t.db"))
    with session_factory() as db:
        _make_observation(db, "idor_bola", "hackerone", ["Enumerate IDs"], doc_id="d1")
    synth = PlaybookSynthesizer(session_factory)
    r1 = synth.synthesize_category("idor_bola")
    assert r1["version"] == 1

    # Add enough new, differently-shaped evidence to force a structural change.
    with session_factory() as db:
        for i in range(5):
            _make_observation(db, "idor_bola", f"source_{i}",
                               ["Enumerate IDs", "Swap ID", "Verify access", "Report"],
                               tools=["Burp Suite", "ffuf"], doc_id=f"d{i+2}")

    r2 = synth.synthesize_category("idor_bola")
    assert r2["action"] in ("new_version", "evidence_updated")

    with session_factory() as db:
        rows = db.query(Playbook).filter(Playbook.playbook_key == "idor_bola").order_by(Playbook.version).all()
    # History must never be deleted, regardless of how many versions exist.
    assert rows[0].version == 1
    assert rows[-1].is_latest is True
    assert all(not r.is_latest for r in rows[:-1])


def test_synthesize_returns_early_for_unknown_category(tmp_path):
    session_factory = get_session_factory(str(tmp_path / "t.db"))
    synth = PlaybookSynthesizer(session_factory)
    result = synth.synthesize_category("nonexistent_category")
    assert result["changed"] is False


# ---------------------------------------------------------------- Experience store

def test_experience_store_records_and_links_explanation(tmp_path):
    session_factory = get_session_factory(str(tmp_path / "t.db"))
    store = ExperienceStore(session_factory)
    exp_id = store.record(outcome="failure", category="ssrf", reason="blocked by WAF",
                           environment="prod-like staging")

    unexplained = store.find_unexplained_failures(category="ssrf")
    assert len(unexplained) == 1

    assert store.link_explanation(exp_id, "doc_explaining_waf_bypass") is True
    assert store.find_unexplained_failures(category="ssrf") == []


def test_experience_store_rejects_unknown_outcome(tmp_path):
    session_factory = get_session_factory(str(tmp_path / "t.db"))
    store = ExperienceStore(session_factory)
    with pytest.raises(ValueError):
        store.record(outcome="not_a_real_outcome", category="ssrf")


# ---------------------------------------------------------------- End-to-end LearningEngine

def test_learning_engine_full_pipeline(tmp_path):
    _write_doc(tmp_path, "idor.md", "IDOR Report")
    session_factory = get_session_factory(str(tmp_path / "t.db"))
    repo = KnowledgeRepository(str(tmp_path))

    llm = StubLLM([json.dumps({"observations": [{
        "vulnerability": "IDOR",
        "discovery_sequence": ["Enumerate object IDs", "Swap ID as another user", "Confirm data returned"],
        "tool_usage": ["Burp Suite"],
        "severity": "high",
    }]})])

    engine = LearningEngine(repository=repo, session_factory=session_factory, llm_client=llm)
    summary = engine.import_knowledge()

    assert summary["documents_scanned"] == 1
    assert summary["observations_extracted"] == 1
    assert "idor_bola" in summary["categories_touched"]

    # Re-running immediately must not reprocess the same unmodified document.
    summary2 = engine.import_knowledge()
    assert summary2["documents_scanned"] == 0

    learned = engine.retrieve_for_planning("Test for IDOR on the orders API")
    assert any(p["category"] == "idor_bola" for p in learned["playbooks"])


def test_learning_engine_record_experience_updates_playbook_confidence(tmp_path):
    session_factory = get_session_factory(str(tmp_path / "t.db"))
    repo = KnowledgeRepository(str(tmp_path))
    with session_factory() as db:
        _make_observation(db, "ssrf", "hackerone", ["Find outbound request", "Redirect to metadata endpoint"],
                           doc_id="d1", vuln="SSRF")
        _make_observation(db, "ssrf", "bugcrowd", ["Find outbound request", "Redirect to metadata endpoint"],
                           doc_id="d2", vuln="SSRF")

    engine = LearningEngine(repository=repo, session_factory=session_factory, llm_client=StubLLM([]))
    synth_result = engine.synthesizer.synthesize_category("ssrf")
    before = synth_result["confidence"]

    result = engine.record_experience(outcome="success", category="ssrf", reason="confirmed on staging")
    after = result["playbook_synthesis"]["confidence"]
    assert after >= before  # a real success should never reduce confidence


# ---------------------------------------------------------------- Retroactive recategorization

@pytest.mark.parametrize("raw,expected", [
    ("Missing Access Control", "authorization"),
    ("Missing Access Control in APIs", "authorization"),
    ("Inadequate Access Control", "authorization"),
    ("Insecure Access Control", "authorization"),
    ("XSS via unsafeHTML", "xss"),
    ("XSS via innerHTML", "xss"),
    ("Deserialization (YAML)", "insecure_deserialization"),
    ("Deserialization (Java)", "insecure_deserialization"),
    ("Session Hijacking", "session_management"),
    ("Session ID Predictability", "session_management"),
    ("Weak Password Requirements", "authentication"),
    ("Missing MFA", "mfa_bypass"),
])
def test_new_aliases_consolidate_the_real_fragmentation_clusters(raw, expected):
    assert normalize_category(raw) == expected


def test_recategorize_all_merges_previously_fragmented_observations(tmp_path):
    """Reproduces the exact real-world scenario: several observations
    stored under near-duplicate category slugs (from before the alias
    table was expanded) should merge into one consolidated category
    once recategorize_all() runs — at zero LLM cost, using only the
    already-stored vulnerability text."""
    session_factory = get_session_factory(str(tmp_path / "t.db"))
    with session_factory() as db:
        # Simulate observations extracted BEFORE the alias expansion —
        # category field holds the stale, fragmented slug.
        _make_observation(db, "missing_access_control", "src1", ["Enumerate endpoints"],
                           doc_id="d1", vuln="Missing Access Control")
        _make_observation(db, "missing_access_control_in_apis", "src2", ["Call API without auth header"],
                           doc_id="d2", vuln="Missing Access Control in APIs")
        _make_observation(db, "inadequate_access_control", "src3", ["Access admin endpoint as normal user"],
                           doc_id="d3", vuln="Inadequate Access Control")

    summary = recategorize_all(session_factory)

    assert summary["observations_recategorized"] == 3
    with session_factory() as db:
        categories = {o.category for o in db.query(Observation).all()}
    assert categories == {"authorization"}  # all three merged into one

    synth = PlaybookSynthesizer(session_factory)
    playbook = synth.get_latest("authorization")
    assert playbook is not None
    provenance = json.loads(playbook.provenance)
    assert provenance["supporting_observations"] == 3  # now real evidence, not 3 separate count=1s


def test_recategorize_all_is_a_no_op_when_categories_already_correct(tmp_path):
    session_factory = get_session_factory(str(tmp_path / "t.db"))
    with session_factory() as db:
        _make_observation(db, "idor_bola", "hackerone", ["Enumerate IDs"], doc_id="d1", vuln="IDOR")

    summary = recategorize_all(session_factory)
    assert summary["observations_recategorized"] == 0
    assert summary["category_merges"] == []

