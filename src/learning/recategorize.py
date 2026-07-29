"""Retroactive recategorization — zero LLM/GPU cost.

Every Observation row keeps the raw `vulnerability` string exactly as
originally extracted (see db_models.py). That means improving
CATEGORY_ALIASES / normalize_category() after the fact does NOT require
re-running any extraction: just re-derive `category` from the text
already on disk, update in place, and re-synthesize whatever categories
were touched.

Use this whenever CATEGORY_ALIASES gains new entries — e.g. after
noticing real fragmentation like a dozen near-duplicate access-control /
deserialization / XSS categories each stuck at supporting_observations=1,
unable to ever build real playbook confidence. This consolidates
existing data immediately, at zero additional model cost, instead of
waiting for a full document reprocessing pass.
"""
from __future__ import annotations
from collections import Counter

from .db_models import Observation
from .observation_extractor import normalize_category
from .playbook_synthesizer import PlaybookSynthesizer
from ..logging_setup import get_logger

log = get_logger("learning.recategorize")


def recategorize_all(session_factory) -> dict:
    """Re-derives `category` for every Observation from its stored
    `vulnerability` text using the CURRENT normalize_category() logic and
    alias table. Returns a summary of what merged into what, and
    re-synthesizes every touched category afterward so playbooks reflect
    the consolidated evidence immediately."""
    changes: Counter = Counter()  # (old_category, new_category) -> count
    touched_categories: set[str] = set()

    with session_factory() as db:
        observations = db.query(Observation).all()
        for obs in observations:
            new_category = normalize_category(obs.vulnerability)
            if new_category != obs.category:
                changes[(obs.category, new_category)] += 1
                touched_categories.add(obs.category)
                touched_categories.add(new_category)
                obs.category = new_category
        db.commit()

    synthesizer = PlaybookSynthesizer(session_factory)
    synthesis_results = [
        synthesizer.synthesize_category(cat) for cat in sorted(touched_categories)
    ]

    summary = {
        "observations_recategorized": sum(changes.values()),
        "category_merges": [
            {"from": old, "to": new, "count": count}
            for (old, new), count in sorted(changes.items(), key=lambda kv: -kv[1])
        ],
        "categories_resynthesized": synthesis_results,
    }
    log.info(f"Recategorization complete: {summary['observations_recategorized']} observation(s) moved "
             f"across {len(changes)} category merge(s)")
    return summary
