"""LearningEngine — the single entry point for the Playbook Learning Engine.

Wires together:
  IncrementalIndexer   (never reprocess indexed documents)
  ObservationExtractor (raw document -> structured observations)
  PlaybookSynthesizer  (many observations -> versioned methodology)
  ExperienceStore      (every engagement -> future evidence)

Pipeline (spec 'Learning Pipeline'):
  New document -> extract observations -> normalize -> compare against
  existing playbooks -> increase evidence OR create new tactic -> never
  duplicate, never overwrite history.

This module does NOT touch raw documents, does NOT fine-tune anything,
and does NOT self-modify prompts — it only writes to its own four
tables (src/learning/db_models.py).
"""
from __future__ import annotations
import json
import dataclasses

from ..knowledge.repository import KnowledgeRepository
from .db_models import Observation
from .incremental_indexer import IncrementalIndexer
from .observation_extractor import ObservationExtractor, normalize_category, CATEGORY_ALIASES
from .playbook_synthesizer import PlaybookSynthesizer
from .experience_store import ExperienceStore
from ..logging_setup import get_logger

log = get_logger("learning.engine")


class LearningEngine:
    def __init__(self, repository: KnowledgeRepository, session_factory, llm_client, config: dict | None = None):
        self.repository = repository
        self.SessionFactory = session_factory
        cfg = config or {}
        self.indexer = IncrementalIndexer(repository, session_factory,
                                           priority_keywords=cfg.get("priority_keywords"))
        self.extractor = ObservationExtractor(llm_client)
        self.synthesizer = PlaybookSynthesizer(
            session_factory,
            confidence_delta_for_new_version=cfg.get("confidence_delta_for_new_version", 0.05),
        )
        self.experience_store = ExperienceStore(session_factory)

    # ---- Learning Pipeline (spec Section: Learning Pipeline) ----
    def import_knowledge(self) -> dict:
        """Runs the full pipeline over whatever the Knowledge Collector has
        newly produced or modified since the last run. Safe to call
        repeatedly — indexed, unmodified documents are always skipped."""
        pending = self.indexer.find_pending()
        touched_categories: set[str] = set()
        total_observations = 0
        docs_failed = 0

        for pending_doc in pending:
            doc, body, digest = pending_doc.doc, pending_doc.body, pending_doc.sha256
            filename = doc.file_path.name if doc.file_path else doc.doc_id

            try:
                extracted = self.extractor.extract(doc, body)
            except Exception as e:
                log.error(f"Observation extraction failed for {doc.doc_id}: {e}")
                self.indexer.mark_indexed(doc.doc_id, filename, digest, 0, status="failed")
                docs_failed += 1
                continue

            with self.SessionFactory() as db:
                for eo in extracted:
                    row = Observation(
                        doc_id=doc.doc_id,
                        source_title=doc.title,
                        source=doc.source,
                        trust_level=doc.trust_level,
                        category=eo.category,
                        vulnerability=eo.vulnerability,
                        target_technology=eo.target_technology,
                        preconditions=json.dumps(eo.preconditions),
                        discovery_sequence=json.dumps(eo.discovery_sequence),
                        payloads=json.dumps(eo.payloads),
                        tool_usage=json.dumps(eo.tool_usage),
                        decision_points=json.dumps(eo.decision_points),
                        false_positives=json.dumps(eo.false_positives),
                        failure_reasons=json.dumps(eo.failure_reasons),
                        successful_validation_steps=json.dumps(eo.successful_validation_steps),
                        severity=eo.severity,
                        references=json.dumps(eo.references),
                        raw_extraction=json.dumps(dataclasses.asdict(eo)),
                    )
                    db.add(row)
                    touched_categories.add(eo.category)
                db.commit()

            total_observations += len(extracted)
            self.indexer.mark_indexed(doc.doc_id, filename, digest, len(extracted))
            log.info(f"Indexed {doc.doc_id}: {len(extracted)} observation(s)")

        synthesis_results = [
            self.synthesizer.synthesize_category(cat) for cat in sorted(touched_categories)
        ]

        summary = {
            "documents_scanned": len(pending),
            "documents_failed": docs_failed,
            "observations_extracted": total_observations,
            "categories_touched": sorted(touched_categories),
            "playbook_synthesis": synthesis_results,
        }
        log.info(f"Learning pipeline complete: {summary}")
        return summary

    # ---- Experience Learning (spec Section: Experience Learning) ----
    def record_experience(self, outcome: str, category: str, **kwargs) -> dict:
        """Records an engagement outcome and immediately re-synthesizes
        that category's playbook so confidence reflects real-world
        results, not just document volume."""
        category = normalize_category(category) if category not in self._known_categories() else category
        exp_id = self.experience_store.record(outcome=outcome, category=category, **kwargs)
        synthesis = self.synthesizer.synthesize_category(category)
        return {"experience_id": exp_id, "playbook_synthesis": synthesis}

    def link_experience_explanation(self, experience_id: int, doc_id: str) -> bool:
        return self.experience_store.link_explanation(experience_id, doc_id)

    def unexplained_failures(self, category: str | None = None) -> list[dict]:
        return self.experience_store.find_unexplained_failures(category)

    # ---- Planner Integration (spec Section: Planner Integration) ----
    def retrieve_for_planning(self, goal_text: str, categories: list[str] | None = None) -> dict:
        """Retrieves relevant playbooks + experiences for the planner to
        weigh alongside raw retrieved knowledge, before generating a
        testing plan. Prefers high-confidence playbooks but always
        returns alternatives too, so the planner isn't blind to
        low-confidence-but-plausible tactics."""
        cats = categories or self._infer_categories(goal_text)
        playbooks = self.synthesizer.retrieve_relevant(cats) if cats else []
        experiences: list[dict] = []
        for cat in cats:
            experiences.extend(self.experience_store.for_category(cat))
        return {"categories_matched": cats, "playbooks": playbooks, "experiences": experiences}

    def _known_categories(self) -> set[str]:
        with self.SessionFactory() as db:
            rows = db.query(Observation.category).distinct().all()
        return {r[0] for r in rows}

    def _infer_categories(self, goal_text: str) -> list[str]:
        """Cheap keyword match against known category aliases + whatever
        categories already exist in the Observation table — deliberately
        simple (no extra LLM/embedding call) since this only narrows which
        playbooks to show the planner, it never filters out evidence."""
        text = (goal_text or "").lower()
        matched = set()
        for phrase, slug in CATEGORY_ALIASES.items():
            if phrase in text:
                matched.add(slug)
        for slug in self._known_categories():
            if slug and slug.replace("_", " ") in text:
                matched.add(slug)
        return sorted(matched)
