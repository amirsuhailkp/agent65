"""Evidence Collector — Vol II Ch15, Vol IX.

Stores immutable originals (requests/responses/logs/screenshots), hashed
and timestamped, linked to a hypothesis. Never mutates stored evidence.
"""
from __future__ import annotations
import hashlib
import json
import datetime as dt
from pathlib import Path
from ..memory.db_models import Evidence


class EvidenceCollector:
    def __init__(self, evidence_dir: str, session_factory):
        self.evidence_dir = Path(evidence_dir)
        self.evidence_dir.mkdir(parents=True, exist_ok=True)
        self.SessionFactory = session_factory

    def _write_blob(self, content: bytes, suffix: str) -> tuple[Path, str]:
        content_hash = hashlib.sha256(content).hexdigest()
        ts = dt.datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
        path = self.evidence_dir / f"{ts}_{content_hash[:12]}{suffix}"
        path.write_bytes(content)
        return path, content_hash

    def record(
        self,
        task_id: int | None,
        hypothesis_id: int | None,
        endpoint: str | None,
        request: bytes | None,
        response: bytes | None,
        tool_output: str | None,
        planner_reasoning: str,
        confidence: float,
        screenshot: bytes | None = None,
    ) -> int:
        req_ref = resp_ref = shot_ref = out_ref = None
        content_hash = None

        if request:
            p, h = self._write_blob(request, ".req.txt")
            req_ref = str(p)
            content_hash = h
        if response:
            p, h = self._write_blob(response, ".resp.txt")
            resp_ref = str(p)
            content_hash = content_hash or h
        if screenshot:
            p, _ = self._write_blob(screenshot, ".png")
            shot_ref = str(p)
        if tool_output:
            p, h = self._write_blob(tool_output.encode(), ".tool.txt")
            out_ref = str(p)
            content_hash = content_hash or h

        with self.SessionFactory() as db:
            row = Evidence(
                task_id=task_id,
                hypothesis_id=hypothesis_id,
                endpoint=endpoint,
                request_ref=req_ref,
                response_ref=resp_ref,
                screenshot_ref=shot_ref,
                tool_output_ref=out_ref,
                planner_reasoning=planner_reasoning,
                confidence=confidence,
                content_hash=content_hash,
            )
            db.add(row)
            db.commit()
            db.refresh(row)
            return row.id
