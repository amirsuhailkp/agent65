"""SQLite relational schema — Vol II Ch22 / Vol IV Ch16.
Sessions, Tasks, Findings, Evidence, Reports, Checkpoints.
Idempotent init per Vol VI Ch10.
"""
from __future__ import annotations
import datetime as dt
from sqlalchemy import (
    create_engine, Column, Integer, String, Text, Float, DateTime, ForeignKey, Boolean
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()


class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True)
    program_name = Column(String, nullable=False)
    scope_snapshot = Column(Text)  # JSON of scope.yaml at engagement start
    status = Column(String, default="active")  # active | paused | completed
    created_at = Column(DateTime, default=dt.datetime.utcnow)
    updated_at = Column(DateTime, default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow)

    tasks = relationship("Task", back_populates="session")
    findings = relationship("Finding", back_populates="session")
    checkpoints = relationship("Checkpoint", back_populates="session")


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    parent_task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    category = Column(String)  # recon | auth | authz | api | business_logic | validation | reporting
    description = Column(Text)
    priority = Column(Float, default=0.0)
    status = Column(String, default="pending")  # pending|queued|running|completed|failed|cancelled
    assigned_tool = Column(String)
    dependencies = Column(Text)  # JSON list of task ids
    created_at = Column(DateTime, default=dt.datetime.utcnow)
    updated_at = Column(DateTime, default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow)

    session = relationship("Session", back_populates="tasks")
    evidence_items = relationship("Evidence", back_populates="task")


class Hypothesis(Base):
    __tablename__ = "hypotheses"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    observation = Column(Text)
    reasoning = Column(Text)
    attack_strategy = Column(Text)
    confidence = Column(Float, default=0.0)
    status = Column(String, default="pending")  # pending|testing|confirmed|rejected|needs_more_evidence
    retry_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=dt.datetime.utcnow)
    updated_at = Column(DateTime, default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow)


class Evidence(Base):
    __tablename__ = "evidence"
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    hypothesis_id = Column(Integer, ForeignKey("hypotheses.id"), nullable=True)
    endpoint = Column(String)
    request_ref = Column(Text)   # path to stored raw request
    response_ref = Column(Text)  # path to stored raw response
    screenshot_ref = Column(Text)
    tool_output_ref = Column(Text)
    planner_reasoning = Column(Text)
    confidence = Column(Float, default=0.0)
    content_hash = Column(String)  # dedup / integrity
    created_at = Column(DateTime, default=dt.datetime.utcnow)

    task = relationship("Task", back_populates="evidence_items")


class Finding(Base):
    __tablename__ = "findings"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    hypothesis_id = Column(Integer, ForeignKey("hypotheses.id"), nullable=True)
    title = Column(String)
    category = Column(String)  # idor|bola|business_logic|auth|api|xss|ssrf|...
    severity = Column(String)  # human-reviewed, never auto-finalized
    confidence = Column(Float, default=0.0)
    description = Column(Text)
    steps_to_reproduce = Column(Text)
    impact = Column(Text)
    remediation = Column(Text)
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=dt.datetime.utcnow)

    session = relationship("Session", back_populates="findings")


class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    finding_id = Column(Integer, ForeignKey("findings.id"), nullable=True)
    format = Column(String)  # markdown|html|pdf|json
    file_ref = Column(Text)
    template = Column(String)  # hackerone|bugcrowd|generic|internal
    created_at = Column(DateTime, default=dt.datetime.utcnow)


class Checkpoint(Base):
    __tablename__ = "checkpoints"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    planner_state = Column(Text)     # JSON
    memory_snapshot = Column(Text)   # JSON
    attack_graph = Column(Text)      # JSON
    task_queue = Column(Text)        # JSON
    resource_status = Column(Text)   # JSON
    created_at = Column(DateTime, default=dt.datetime.utcnow)

    session = relationship("Session", back_populates="checkpoints")


def get_engine(db_path: str):
    engine = create_engine(f"sqlite:///{db_path}", future=True)
    Base.metadata.create_all(engine)  # idempotent
    return engine


def get_session_factory(db_path: str):
    engine = get_engine(db_path)
    return sessionmaker(bind=engine, future=True)
