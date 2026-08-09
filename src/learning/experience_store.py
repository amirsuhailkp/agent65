"""Experience Database — spec 'Experience Database' & 'Experience Learning'.

Every engagement — successful findings, failed findings, duplicate
reports, invalid reports, partial discoveries, tool failures, false
positives — becomes future evidence. If a later-imported document
explains WHY a past technique failed, the two records get linked.
"""
from __future__ import annotations
import json

from .db_models import Experience
from ..logging_setup import get_logger

log = get_logger("learning.experience_store")

VALID_OUTCOMES = {
    "success", "failure", "duplicate", "invalid", "partial",
    "tool_failure", "false_positive",
}


class ExperienceStore:
    def __init__(self, session_factory):
        self.SessionFactory = session_factory

    def record(
        self,
        outcome: str,
        category: str,
        technology: str = "",
        description: str = "",
        reason: str = "",
        environment: str = "",
        failure_type: str = "",
        session_id: int | None = None,
        playbook_key: str | None = None,
        confidence_delta: float = 0.0,
    ) -> int:
        if outcome not in VALID_OUTCOMES:
            raise ValueError(f"Unknown experience outcome '{outcome}', expected one of {VALID_OUTCOMES}")
        with self.SessionFactory() as db:
            row = Experience(
                session_id=session_id,
                playbook_key=playbook_key or category,
                technology=technology,
                category=category,
                outcome=outcome,
                description=description,
                reason=reason,
                environment=environment,
                failure_type=failure_type,
                confidence_delta=confidence_delta,
            )
            db.add(row)
            db.commit()
            db.refresh(row)
            log.info(f"Experience recorded id={row.id} category={category} outcome={outcome}")
            return row.id

    def link_explanation(self, experience_id: int, doc_id: str) -> bool:
        """'If another document later explains why, link both records.'"""
        with self.SessionFactory() as db:
            row = db.get(Experience, experience_id)
            if not row:
                log.warning(f"Cannot link explanation — experience {experience_id} not found")
                return False
            row.explained_by_doc_id = doc_id
            db.commit()
            log.info(f"Experience {experience_id} linked to explaining document {doc_id}")
            return True

    def find_unexplained_failures(self, category: str | None = None) -> list[dict]:
        """Surfaces failures/tool_failures with no linked explanation yet —
        useful when new knowledge is imported, to check if it now explains
        a past mystery failure."""
        with self.SessionFactory() as db:
            q = db.query(Experience).filter(
                Experience.outcome.in_(["failure", "tool_failure", "false_positive"]),
                Experience.explained_by_doc_id.is_(None),
            )
            if category:
                q = q.filter(Experience.category == category)
            rows = q.all()
        return [
            {"id": r.id, "category": r.category, "reason": r.reason, "environment": r.environment}
            for r in rows
        ]

    def for_category(self, category: str) -> list[dict]:
        with self.SessionFactory() as db:
            rows = db.query(Experience).filter(Experience.category == category).all()
        return [
            {
                "outcome": r.outcome, "reason": r.reason, "description": r.description,
                "technology": r.technology,
                "environment": r.environment, "explained_by_doc_id": r.explained_by_doc_id,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in rows
        ]
