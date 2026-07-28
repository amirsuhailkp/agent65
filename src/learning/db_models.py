"""Playbook Learning Engine — relational schema.

Shares the existing SQLite engine/Base from src/memory/db_models.py
(same `Base.metadata.create_all()` call in scripts/init_db.py picks
these tables up automatically — no second database to manage).

Four tables, one per learning layer:

  DocumentIndex -> incremental-import bookkeeping (SHA256, never reprocess)
  Observation   -> structured facts extracted from ONE document
  Playbook      -> synthesized methodology, versioned, append-only history
  Experience    -> every real engagement outcome (success/fail/duplicate/...)

All JSON-shaped columns are stored as TEXT (json.dumps/json.loads at the
boundary) to keep this portable across SQLite without extra dependencies,
consistent with the rest of src/memory/db_models.py.
"""
from __future__ import annotations
import datetime as dt
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Boolean, UniqueConstraint

from ..memory.db_models import Base


class DocumentIndex(Base):
    """Incremental Knowledge Import bookkeeping (spec: 'never reprocess
    already indexed documents'). One row per raw document ever seen."""
    __tablename__ = "learning_document_index"
    __table_args__ = (UniqueConstraint("doc_id", name="uq_learning_doc_id"),)

    id = Column(Integer, primary_key=True)
    doc_id = Column(String, nullable=False)
    filename = Column(String)
    sha256 = Column(String, nullable=False)
    status = Column(String, default="indexed")  # indexed | failed | skipped
    observation_count = Column(Integer, default=0)
    indexed_at = Column(DateTime, default=dt.datetime.utcnow)
    updated_at = Column(DateTime, default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow)


class Observation(Base):
    """One structured observation extracted from one immutable source
    document. Never queried directly by the planner — only Playbooks and
    (transitively) Experiences are, per spec Section 2."""
    __tablename__ = "learning_observations"

    id = Column(Integer, primary_key=True)
    doc_id = Column(String, nullable=False)
    source_title = Column(String)
    source = Column(String)          # e.g. "portswigger.net", "hackerone"
    trust_level = Column(String)     # verified | unverified (from KnowledgeRepository)
    category = Column(String)        # normalized bucket used for playbook matching

    vulnerability = Column(String)
    target_technology = Column(String)
    preconditions = Column(Text)               # JSON list[str]
    discovery_sequence = Column(Text)           # JSON list[str] (ordered steps)
    payloads = Column(Text)                     # JSON list[str]
    tool_usage = Column(Text)                   # JSON list[str]
    decision_points = Column(Text)               # JSON list[str]
    false_positives = Column(Text)               # JSON list[str]
    failure_reasons = Column(Text)                # JSON list[str]
    successful_validation_steps = Column(Text)    # JSON list[str]
    severity = Column(String)
    references = Column(Text)                     # JSON list[str]

    raw_extraction = Column(Text)  # full LLM JSON, kept verbatim for audit
    created_at = Column(DateTime, default=dt.datetime.utcnow)


class Playbook(Base):
    """Synthesized methodology. Append-only versioning: a "logical"
    playbook is identified by `playbook_key` and accumulates rows with
    increasing `version`; only one row per key has `is_latest=True`.
    Nothing is ever deleted or overwritten (spec: Versioning Rules)."""
    __tablename__ = "learning_playbooks"
    __table_args__ = (UniqueConstraint("playbook_key", "version", name="uq_playbook_key_version"),)

    id = Column(Integer, primary_key=True)
    playbook_key = Column(String, nullable=False)  # stable slug, e.g. "subdomain_takeover"
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    version = Column(Integer, nullable=False, default=1)
    is_latest = Column(Boolean, default=True)

    workflow = Column(Text)          # JSON ordered list[str] — the investigation sequence
    decision_tree = Column(Text)     # JSON — branching guidance
    common_mistakes = Column(Text)   # JSON list[str]
    false_positives = Column(Text)   # JSON list[str]
    best_tools = Column(Text)        # JSON list[str]

    confidence = Column(Float, default=0.0)  # 0.0 - 1.0, see confidence.py
    supporting_observation_ids = Column(Text)  # JSON list[int]
    supporting_document_ids = Column(Text)     # JSON list[str], deduped doc_ids
    provenance = Column(Text)        # JSON: {"derived_from": {...}, "supporting_observations": n}
    change_summary = Column(Text)    # why this version differs from the previous one

    created_at = Column(DateTime, default=dt.datetime.utcnow)


class Experience(Base):
    """Every real engagement outcome — successes, failures, duplicates,
    invalid reports, partial discoveries, tool failures, false positives.
    Every experience becomes future evidence (spec Section 4)."""
    __tablename__ = "learning_experiences"

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, nullable=True)     # loosely coupled to sessions.id (no hard FK
                                                      # constraint — experiences must survive even
                                                      # if a session row is pruned)
    playbook_key = Column(String, nullable=True)     # which methodology this engagement relates to
    technology = Column(String)
    category = Column(String)
    outcome = Column(String, nullable=False)  # success|failure|duplicate|invalid|partial|
                                               # tool_failure|false_positive
    description = Column(Text)
    reason = Column(Text)         # why it failed / why it was invalid, etc.
    environment = Column(Text)    # target/tech/tool context at time of engagement
    failure_type = Column(String)

    explained_by_doc_id = Column(String, nullable=True)  # set later, once a document explains WHY
    confidence_delta = Column(Float, default=0.0)          # nudge applied to the related playbook

    created_at = Column(DateTime, default=dt.datetime.utcnow)
