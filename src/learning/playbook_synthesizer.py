"""Playbook Synthesizer — spec 'Playbook Database' & 'Learning Pipeline'.

A playbook is NOT copied from one report. It is synthesized from many
observations that share a normalized category (e.g. "subdomain_takeover").

Merge strategy (deliberately simple arithmetic, not another LLM call —
"Keep all learning auditable and explainable"):
  - Workflow steps are merged by *average relative position* across every
    supporting observation's discovery_sequence, so steps that
    consistently show up early stay early (this is how the Subdomain
    Takeover example in the spec — Asset Discovery -> DNS Enumeration ->
    Cloud Detection -> Dangling Records -> Verification -> Evidence
    Collection — would fall out of many reports).
  - Tools / mistakes / false positives are merged by frequency (most
    commonly mentioned first), deduplicated on normalized text.

Versioning: a version bump happens only when the *substance* of the
playbook changes (workflow, tools, or mistakes). Pure evidence-count /
confidence updates patch the current latest row in place — the
methodology text itself is never silently rewritten without a new,
auditable version (spec 'Versioning Rules': never delete or overwrite
history).
"""
from __future__ import annotations
import json
import re
import math
from collections import Counter, defaultdict

from .db_models import Observation, Playbook, Experience
from .confidence import calculate_confidence, build_provenance
from ..logging_setup import get_logger

log = get_logger("learning.playbook_synthesizer")

# Structural-change thresholds — see module docstring on why version bumps
# are gated rather than automatic on every synthesis run.
_CONFIDENCE_DELTA_FOR_NEW_VERSION = 0.05


def _normalize_step(step: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", (step or "").lower()).strip()


def _merge_workflow(sequences: list[list[str]]) -> list[str]:
    """Average-relative-position merge. Steps mentioned by too few
    sources are dropped as noise once enough independent sequences exist."""
    if not sequences:
        return []
    if len(sequences) == 1:
        return [s for s in sequences[0] if s]

    positions: dict[str, list[float]] = defaultdict(list)
    display: dict[str, str] = {}
    for seq in sequences:
        seq = [s for s in seq if s]
        if not seq:
            continue
        denom = max(len(seq) - 1, 1)
        for idx, step in enumerate(seq):
            key = _normalize_step(step)
            if not key:
                continue
            positions[key].append(idx / denom)
            display.setdefault(key, step)

    min_support = max(1, math.ceil(0.3 * len(sequences)))
    kept = [(key, sum(v) / len(v)) for key, v in positions.items() if len(v) >= min_support]
    kept.sort(key=lambda kv: kv[1])
    return [display[k] for k, _ in kept]


def _merge_frequency_list(lists: list[list[str]], cap: int = 12) -> list[str]:
    """Frequency-ranked, deduplicated union. Preserves first-seen casing."""
    counts: Counter = Counter()
    display: dict[str, str] = {}
    for lst in lists:
        for item in lst or []:
            if not item:
                continue
            key = _normalize_step(item)
            if not key:
                continue
            counts[key] += 1
            display.setdefault(key, item)
    ranked = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
    return [display[k] for k, _ in ranked[:cap]]


class PlaybookSynthesizer:
    def __init__(self, session_factory, confidence_delta_for_new_version: float = _CONFIDENCE_DELTA_FOR_NEW_VERSION):
        self.SessionFactory = session_factory
        self.confidence_delta_for_new_version = confidence_delta_for_new_version

    def synthesize_category(self, category: str) -> dict:
        """Re-synthesizes the playbook for one category from ALL
        observations ever recorded for it (append-only), plus linked
        Experience outcomes. Safe/idempotent to re-run."""
        with self.SessionFactory() as db:
            observations = (
                db.query(Observation).filter(Observation.category == category).all()
            )
            if not observations:
                log.warning(f"No observations found for category={category}, skipping synthesis")
                return {"category": category, "changed": False, "reason": "no_observations"}

            experiences = (
                db.query(Experience).filter(Experience.category == category).all()
            )
            personal_successes = sum(1 for e in experiences if e.outcome == "success")
            personal_failures = sum(1 for e in experiences if e.outcome in ("failure", "false_positive"))
            contradictions = sum(
                1 for e in experiences if e.outcome in ("invalid", "duplicate", "tool_failure")
            )

            source_counts = Counter(o.source or "unknown" for o in observations)
            distinct_sources = len(source_counts)
            supporting_observation_ids = [o.id for o in observations]
            supporting_document_ids = sorted({o.doc_id for o in observations})

            workflow = _merge_workflow(
                [json.loads(o.discovery_sequence or "[]") for o in observations]
            )
            best_tools = _merge_frequency_list(
                [json.loads(o.tool_usage or "[]") for o in observations]
            )
            common_mistakes = _merge_frequency_list(
                [json.loads(o.failure_reasons or "[]") for o in observations]
                + [json.loads(o.decision_points or "[]") for o in observations]
            )
            false_positives = _merge_frequency_list(
                [json.loads(o.false_positives or "[]") for o in observations]
            )
            decision_tree = {
                "preconditions": _merge_frequency_list(
                    [json.loads(o.preconditions or "[]") for o in observations]
                ),
                "validation_steps": _merge_frequency_list(
                    [json.loads(o.successful_validation_steps or "[]") for o in observations]
                ),
            }

            confidence = calculate_confidence(
                supporting_observations=len(observations),
                distinct_sources=distinct_sources,
                personal_successes=personal_successes,
                personal_failures=personal_failures,
                contradictions=contradictions,
            )
            provenance = build_provenance(
                source_counts=dict(source_counts),
                supporting_observations=len(observations),
                personal_successes=personal_successes,
                personal_failures=personal_failures,
            )

            latest = (
                db.query(Playbook)
                .filter(Playbook.playbook_key == category, Playbook.is_latest.is_(True))
                .first()
            )

            display_name = observations[-1].vulnerability or category.replace("_", " ").title()

            if latest is None:
                # Genuinely new methodology — create the playbook lineage.
                row = Playbook(
                    playbook_key=category,
                    name=display_name,
                    category=category,
                    version=1,
                    is_latest=True,
                    workflow=json.dumps(workflow),
                    decision_tree=json.dumps(decision_tree),
                    common_mistakes=json.dumps(common_mistakes),
                    false_positives=json.dumps(false_positives),
                    best_tools=json.dumps(best_tools),
                    confidence=confidence,
                    supporting_observation_ids=json.dumps(supporting_observation_ids),
                    supporting_document_ids=json.dumps(supporting_document_ids),
                    provenance=json.dumps(provenance),
                    change_summary=f"Initial synthesis from {len(observations)} observation(s).",
                )
                db.add(row)
                db.commit()
                log.info(f"Created NEW playbook '{category}' v1 (confidence={confidence})")
                return {"category": category, "changed": True, "action": "created", "version": 1,
                        "confidence": confidence}

            prev_workflow = json.loads(latest.workflow or "[]")
            prev_tools = json.loads(latest.best_tools or "[]")
            prev_mistakes = json.loads(latest.common_mistakes or "[]")
            structural_change = (
                workflow != prev_workflow or best_tools != prev_tools or common_mistakes != prev_mistakes
            )
            confidence_jump = abs(confidence - (latest.confidence or 0.0)) >= self.confidence_delta_for_new_version

            if structural_change or confidence_jump:
                latest.is_latest = False
                new_row = Playbook(
                    playbook_key=category,
                    name=display_name,
                    category=category,
                    version=latest.version + 1,
                    is_latest=True,
                    workflow=json.dumps(workflow),
                    decision_tree=json.dumps(decision_tree),
                    common_mistakes=json.dumps(common_mistakes),
                    false_positives=json.dumps(false_positives),
                    best_tools=json.dumps(best_tools),
                    confidence=confidence,
                    supporting_observation_ids=json.dumps(supporting_observation_ids),
                    supporting_document_ids=json.dumps(supporting_document_ids),
                    provenance=json.dumps(provenance),
                    change_summary=(
                        f"Re-synthesized from {len(observations)} observation(s) "
                        f"({distinct_sources} distinct source(s)); "
                        f"{'workflow/tooling changed' if structural_change else 'confidence shifted materially'}."
                    ),
                )
                db.add(new_row)
                db.commit()
                log.info(f"New version of playbook '{category}': v{latest.version} -> v{new_row.version}")
                return {"category": category, "changed": True, "action": "new_version",
                        "version": new_row.version, "confidence": confidence}

            # No structural change and no material confidence shift —
            # update evidence bookkeeping on the existing latest row only.
            latest.supporting_observation_ids = json.dumps(supporting_observation_ids)
            latest.supporting_document_ids = json.dumps(supporting_document_ids)
            latest.provenance = json.dumps(provenance)
            latest.confidence = confidence
            db.commit()
            log.info(f"Playbook '{category}' evidence updated in place (v{latest.version}, "
                      f"confidence={confidence})")
            return {"category": category, "changed": True, "action": "evidence_updated",
                    "version": latest.version, "confidence": confidence}

    def get_latest(self, category: str) -> Playbook | None:
        with self.SessionFactory() as db:
            return (
                db.query(Playbook)
                .filter(Playbook.playbook_key == category, Playbook.is_latest.is_(True))
                .first()
            )

    def retrieve_relevant(self, categories: list[str], min_confidence: float = 0.0) -> list[dict]:
        """Planner-facing read. Prefers high-confidence playbooks but
        still returns lower-confidence alternatives so the planner can
        weigh them (spec 'Planner Integration')."""
        with self.SessionFactory() as db:
            rows = (
                db.query(Playbook)
                .filter(Playbook.playbook_key.in_(categories), Playbook.is_latest.is_(True))
                .all()
            )
        out = [
            {
                "name": r.name,
                "category": r.category,
                "version": r.version,
                "confidence": r.confidence,
                "workflow": json.loads(r.workflow or "[]"),
                "decision_tree": json.loads(r.decision_tree or "{}"),
                "common_mistakes": json.loads(r.common_mistakes or "[]"),
                "false_positives": json.loads(r.false_positives or "[]"),
                "best_tools": json.loads(r.best_tools or "[]"),
                "provenance": json.loads(r.provenance or "{}"),
            }
            for r in rows
            if r.confidence >= min_confidence
        ]
        out.sort(key=lambda p: p["confidence"], reverse=True)
        return out
