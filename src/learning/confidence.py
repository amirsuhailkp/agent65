"""Confidence System — spec 'Confidence System' & 'Provenance'.

Hard rule from the spec: "Never increase confidence from one report
alone." Everything else scales with evidence, but that floor is absolute
and enforced structurally below, not just by tuning weights.

Factors considered (spec's example list):
  - independent reports        -> `distinct_sources`
  - personal successful findings -> `personal_successes`
  - repeated validation         -> folded into `supporting_observations`
  - contradictory evidence      -> `contradictions` (failed/false-positive
                                    experiences linked to this category)
  - freshness                   -> left as a future hook (`freshness`),
                                    defaults to neutral (1.0) so it never
                                    silently deflates confidence today
"""
from __future__ import annotations


def calculate_confidence(
    supporting_observations: int,
    distinct_sources: int,
    personal_successes: int = 0,
    personal_failures: int = 0,
    contradictions: int = 0,
    freshness: float = 1.0,
) -> float:
    """Returns a confidence score in [0.0, 0.99]. Never returns a value
    above 0.3 when only a single observation supports the tactic —
    this is a structural cap, not a tunable weight, per spec."""
    if supporting_observations <= 0:
        return 0.0
    if supporting_observations == 1:
        return round(min(0.3, 0.15 * supporting_observations), 3)

    # Diminishing-returns curves: each additional piece of evidence helps
    # less than the last, so confidence grows but never explodes off a
    # handful of reports.
    evidence_component = 1 - (1 / (1 + 0.15 * supporting_observations))
    diversity_component = 1 - (1 / (1 + 0.5 * max(distinct_sources, 0)))
    personal_component = 1 - (1 / (1 + 0.3 * max(personal_successes, 0)))

    contradiction_penalty = min(0.4, 0.1 * max(contradictions, 0)) \
        + min(0.3, 0.15 * max(personal_failures, 0))

    raw = 0.5 * evidence_component + 0.3 * diversity_component + 0.2 * personal_component
    raw *= max(0.0, min(freshness, 1.0)) if freshness else 1.0
    confidence = max(0.0, min(0.99, raw - contradiction_penalty))
    return round(confidence, 3)


def build_provenance(
    source_counts: dict[str, int],
    supporting_observations: int,
    personal_successes: int = 0,
    personal_failures: int = 0,
) -> dict:
    """Every tactic must explain WHY it exists (spec 'Provenance')."""
    return {
        "derived_from": dict(source_counts),
        "personal_successful_findings": personal_successes,
        "personal_failed_findings": personal_failures,
        "supporting_observations": supporting_observations,
    }
