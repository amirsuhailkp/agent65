"""Incremental Knowledge Import — spec 'Incremental Knowledge Import'.

The system must NEVER reprocess already indexed documents. If 100,000
reports exist and only 3 are added, process only those 3.

Algorithm, exactly as specified:
    1. Compute SHA256.
    2. Compare with index.
    3. Skip indexed files.
    4. Process only new or modified files.
    5. Update index.
"""
from __future__ import annotations
import hashlib
import datetime as dt
from dataclasses import dataclass

from ..knowledge.repository import KnowledgeRepository, RawKnowledgeDoc
from .db_models import DocumentIndex
from ..logging_setup import get_logger

log = get_logger("learning.incremental_indexer")

# Broad substring matches on title/category — catches "authentication",
# "authorization", "business logic", "IDOR", "session management", "JWT",
# etc. Deliberately coarse: false positives here just mean a doc gets
# processed slightly earlier than it needed to, which is harmless. This
# only reorders a queue — it never skips or excludes anything.
DEFAULT_PRIORITY_KEYWORDS = [
    "auth", "session", "logic", "idor", "bola", "privilege",
    "access control", "token", "jwt", "sso", "oauth",
]


@dataclass
class PendingDocument:
    doc: RawKnowledgeDoc
    body: str
    sha256: str


class IncrementalIndexer:
    def __init__(self, repository: KnowledgeRepository, session_factory,
                 priority_keywords: list[str] | None = None):
        self.repository = repository
        self.SessionFactory = session_factory
        self.priority_keywords = [k.lower() for k in (priority_keywords or DEFAULT_PRIORITY_KEYWORDS)]

    @staticmethod
    def _hash_bytes(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    def _existing_hash(self, db, doc_id: str) -> str | None:
        row = db.query(DocumentIndex).filter(DocumentIndex.doc_id == doc_id).first()
        return row.sha256 if row else None

    def _priority_rank(self, doc: RawKnowledgeDoc) -> int:
        """0 = process first (matches a priority keyword), 1 = process later.
        Used only to order an already-determined pending list — priority
        never causes a document to be skipped or included/excluded."""
        text = f"{doc.title or ''} {doc.category or ''}".lower()
        return 0 if any(k in text for k in self.priority_keywords) else 1

    def find_pending(self) -> list[PendingDocument]:
        """Returns only documents that are new or whose content changed
        since the last successful index run — never reprocesses unchanged
        documents. Within that set, priority-matching documents (see
        DEFAULT_PRIORITY_KEYWORDS) are ordered first so a large backlog
        doesn't delay playbooks for your actual focus area."""
        pending: list[PendingDocument] = []
        with self.SessionFactory() as db:
            for doc, body in self.repository.iter_documents():
                if doc.file_path is not None:
                    raw_bytes = doc.file_path.read_bytes()
                else:
                    raw_bytes = body.encode("utf-8")
                digest = self._hash_bytes(raw_bytes)

                existing = self._existing_hash(db, doc.doc_id)
                if existing == digest:
                    continue  # unchanged — never reprocess
                pending.append(PendingDocument(doc=doc, body=body, sha256=digest))

        # Stable sort: priority docs move to the front, relative order
        # otherwise preserved.
        pending.sort(key=lambda p: self._priority_rank(p.doc))
        priority_count = sum(1 for p in pending if self._priority_rank(p.doc) == 0)
        log.info(f"Incremental scan: {len(pending)} new/modified document(s) to process "
                 f"({priority_count} priority-matched, processed first)")
        return pending

    def mark_indexed(self, doc_id: str, filename: str, sha256: str, observation_count: int,
                      status: str = "indexed") -> None:
        with self.SessionFactory() as db:
            row = db.query(DocumentIndex).filter(DocumentIndex.doc_id == doc_id).first()
            now = dt.datetime.utcnow()
            if row:
                row.sha256 = sha256
                row.status = status
                row.observation_count = observation_count
                row.updated_at = now
            else:
                row = DocumentIndex(
                    doc_id=doc_id, filename=filename, sha256=sha256,
                    status=status, observation_count=observation_count,
                    indexed_at=now, updated_at=now,
                )
                db.add(row)
            db.commit()

    def stats(self) -> dict:
        with self.SessionFactory() as db:
            total = db.query(DocumentIndex).count()
            failed = db.query(DocumentIndex).filter(DocumentIndex.status == "failed").count()
            return {"total_indexed": total, "failed": failed}
