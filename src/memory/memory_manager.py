"""Memory Manager — Vol II Ch10, Vol IV Ch9-11.

Layers:
  Working Memory  -> in-process, cleared when irrelevant (active endpoint, cookies, JWTs, temp obs)
  Session Memory  -> persists for one engagement (scope, planner state, tasks, attack graph, auth state)
  Long-Term Memory -> reusable, verified only (methodologies, validated attack chains, lessons)

Learning rule (Vol IV Ch14): never learn from hallucinated output, unverified findings,
failed experiments, or unvalidated internet content.
"""
from __future__ import annotations
import json
import datetime as dt
from dataclasses import dataclass, field
from typing import Any, Optional

from .db_models import get_session_factory, Session as SessionRow, Checkpoint
from ..logging_setup import get_logger

log = get_logger("memory")


@dataclass
class WorkingMemory:
    active_endpoint: Optional[str] = None
    current_hypothesis_id: Optional[int] = None
    cookies: dict = field(default_factory=dict)
    jwts: dict = field(default_factory=dict)
    request_history: list = field(default_factory=list)
    temp_observations: list = field(default_factory=list)

    def clear(self):
        self.active_endpoint = None
        self.current_hypothesis_id = None
        self.temp_observations.clear()
        log.debug("Working memory cleared")

    def to_dict(self) -> dict:
        return {
            "active_endpoint": self.active_endpoint,
            "current_hypothesis_id": self.current_hypothesis_id,
            "cookies": self.cookies,
            "jwts": self.jwts,
            "request_history": self.request_history[-50:],  # bounded
            "temp_observations": self.temp_observations,
        }


class MemoryManager:
    def __init__(self, db_path: str, session_id: Optional[int] = None):
        self.SessionFactory = get_session_factory(db_path)
        self.working = WorkingMemory()
        self.session_id = session_id

    # ---- Session Memory ----
    def start_session(self, program_name: str, scope_snapshot: dict) -> int:
        with self.SessionFactory() as db:
            row = SessionRow(
                program_name=program_name,
                scope_snapshot=json.dumps(scope_snapshot),
                status="active",
            )
            db.add(row)
            db.commit()
            db.refresh(row)
            self.session_id = row.id
            log.info(f"Session started id={row.id} program={program_name}")
            return row.id

    def resume_session(self, session_id: int) -> Optional[dict]:
        with self.SessionFactory() as db:
            row = db.get(SessionRow, session_id)
            if not row:
                log.warning(f"No session found id={session_id}")
                return None
            self.session_id = session_id
            latest_ckpt = (
                db.query(Checkpoint)
                .filter(Checkpoint.session_id == session_id)
                .order_by(Checkpoint.created_at.desc())
                .first()
            )
            if latest_ckpt:
                self.working = WorkingMemory(**json.loads(latest_ckpt.memory_snapshot))
                log.info(f"Resumed session {session_id} from checkpoint {latest_ckpt.id}")
                return {
                    "planner_state": json.loads(latest_ckpt.planner_state),
                    "attack_graph": json.loads(latest_ckpt.attack_graph),
                    "task_queue": json.loads(latest_ckpt.task_queue),
                }
            log.info(f"Resumed session {session_id}, no prior checkpoint")
            return None

    # ---- Checkpointing (Vol IV Ch13) ----
    def save_checkpoint(self, planner_state: dict, attack_graph: dict, task_queue: dict,
                         resource_status: dict) -> int:
        if not self.session_id:
            raise RuntimeError("No active session — call start_session() first")
        with self.SessionFactory() as db:
            ckpt = Checkpoint(
                session_id=self.session_id,
                planner_state=json.dumps(planner_state),
                memory_snapshot=json.dumps(self.working.to_dict()),
                attack_graph=json.dumps(attack_graph),
                task_queue=json.dumps(task_queue),
                resource_status=json.dumps(resource_status),
            )
            db.add(ckpt)
            db.commit()
            db.refresh(ckpt)
            log.info(f"Checkpoint saved id={ckpt.id} session={self.session_id}")
            return ckpt.id

    # ---- Long-Term Memory (Vol IV Ch11, Ch14) ----
    def promote_to_long_term(self, knowledge_writer, item: dict, verified: bool):
        """Only verified, evidence-backed items may enter long-term / knowledge store.
        `knowledge_writer` is the KnowledgeManager.add_verified_item callable.
        """
        if not verified:
            log.warning("Refused to promote unverified item to long-term memory")
            return False
        item = {**item, "trust_level": "verified", "promoted_at": dt.datetime.utcnow().isoformat()}
        knowledge_writer(item)
        log.info(f"Promoted verified item to long-term memory: {item.get('title', 'untitled')}")
        return True
