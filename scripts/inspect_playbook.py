"""Inspect a synthesized playbook — prints the workflow, tools, mistakes,
confidence, and provenance for one category. Handy for sanity-checking
what the Learning Engine has actually built, without fighting shell
quoting on inline one-liners.

Usage:
    python scripts/inspect_playbook.py authentication
    python scripts/inspect_playbook.py idor_bola --all-versions
"""
import sys
import json
import argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import load_config, resolve_path
from src.memory.db_models import get_session_factory
from src.learning.db_models import Playbook


def _print_playbook(row: Playbook):
    print(f"\n{'=' * 60}")
    print(f"{row.name}  (category={row.category}, v{row.version}, latest={row.is_latest})")
    print(f"Confidence: {row.confidence}")
    print(f"{'=' * 60}")
    print("\nWorkflow:")
    for i, step in enumerate(json.loads(row.workflow or "[]"), 1):
        print(f"  {i}. {step}")
    print("\nBest tools:")
    for t in json.loads(row.best_tools or "[]"):
        print(f"  - {t}")
    print("\nCommon mistakes / decision points:")
    for m in json.loads(row.common_mistakes or "[]"):
        print(f"  - {m}")
    print("\nFalse positives to watch for:")
    for fp in json.loads(row.false_positives or "[]"):
        print(f"  - {fp}")
    decision_tree = json.loads(row.decision_tree or "{}")
    if decision_tree.get("preconditions"):
        print("\nPreconditions:")
        for p in decision_tree["preconditions"]:
            print(f"  - {p}")
    if decision_tree.get("validation_steps"):
        print("\nValidation steps:")
        for v in decision_tree["validation_steps"]:
            print(f"  - {v}")
    print("\nProvenance:")
    print(json.dumps(json.loads(row.provenance or "{}"), indent=2))
    if row.change_summary:
        print(f"\nChange summary: {row.change_summary}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("category", help="Playbook category slug, e.g. 'authentication', 'idor_bola'")
    parser.add_argument("--all-versions", action="store_true",
                         help="Show every version's history, not just the latest")
    args = parser.parse_args()

    cfg = load_config()
    db_path = str(resolve_path(cfg["database"]["sqlite_path"]))
    session_factory = get_session_factory(db_path)

    with session_factory() as db:
        if args.all_versions:
            rows = (
                db.query(Playbook)
                .filter(Playbook.category == args.category)
                .order_by(Playbook.version)
                .all()
            )
        else:
            rows = (
                db.query(Playbook)
                .filter(Playbook.category == args.category, Playbook.is_latest.is_(True))
                .all()
            )

    if not rows:
        print(f"No playbook found for category '{args.category}'. "
              f"Check the exact slug with the category-breakdown query, or run "
              f"scripts/run_learning_pipeline.py / scripts/recategorize_observations.py first.")
        sys.exit(1)

    for row in rows:
        _print_playbook(row)
