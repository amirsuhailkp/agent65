"""Runs the retroactive recategorization pass (session 38, revised).

Re-derives `category` for every existing Observation from its stored
`vulnerability` text using the current CATEGORY_ALIASES table, merges
fragmented near-duplicate categories, and re-synthesizes only the
playbooks that were touched. Zero LLM/GPU cost -- no re-extraction.

SAFETY: defaults to --dry-run. Nothing is written to the database, and
no playbooks are re-synthesized, unless you pass --commit. Always
review the printed merge list first -- a bad alias can silently
reclassify well-supported observations (this happened once already:
sql_injection/xss/mfa_bypass observations were briefly merged into
unrelated categories due to a substring-matching bug in
normalize_category(), since fixed).

Usage (from the project root, venv active):
    python scripts/recategorize_run.py              # preview only
    python scripts/recategorize_run.py --commit      # actually apply
"""
from __future__ import annotations
import argparse
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import load_config, resolve_path
from src.memory.db_models import get_session_factory
from src.learning.db_models import Observation
from src.learning.observation_extractor import normalize_category
from src.learning.recategorize import recategorize_all


def preview(session_factory) -> Counter:
    """Read-only: computes what recategorize_all() WOULD change, without
    writing anything, so it can be reviewed before committing."""
    changes: Counter = Counter()
    with session_factory() as db:
        for obs in db.query(Observation).all():
            new_category = normalize_category(obs.vulnerability)
            if new_category != obs.category:
                changes[(obs.category, new_category)] += 1
    return changes


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--commit", action="store_true",
        help="Actually write the recategorization and re-synthesize playbooks. "
             "Without this flag, only a preview is printed.",
    )
    args = parser.parse_args()

    cfg = load_config()
    db_path = str(resolve_path(cfg["database"]["sqlite_path"]))
    print(f"Using database: {db_path}")

    session_factory = get_session_factory(db_path)
    changes = preview(session_factory)

    if not changes:
        print("\nNo category changes to make -- nothing to do.")
        return

    total = sum(changes.values())
    print(f"\n{total} observation(s) would move across {len(changes)} category merge(s):\n")
    for (old, new), count in sorted(changes.items(), key=lambda kv: -kv[1]):
        print(f"  {old!r:55} -> {new!r:30} ({count})")

    if not args.commit:
        print(
            f"\nDRY RUN -- nothing was written. Review the merges above.\n"
            f"If they look correct, back up your DB and re-run with --commit:\n"
            f"  Copy-Item {db_path} {db_path}.bak-before-recategorize\n"
            f"  python scripts/recategorize_run.py --commit"
        )
        return

    print("\n--commit passed -- applying and re-synthesizing playbooks...")
    summary = recategorize_all(session_factory)
    print(f"\nObservations recategorized: {summary['observations_recategorized']}")
    print(f"Categories resynthesized: {len(summary['categories_resynthesized'])}")


if __name__ == "__main__":
    main()