"""Wipe learning data for ONE category only — use this instead of
reset_learning_data.py --all when only a specific category got polluted
(e.g. by a dispatcher bug that produced fake tool_failure experiences).

Deletes:
  - learning_experiences  where category == <category>
  - learning_playbooks    where key/category == <category>  (forces
    resynthesis from whatever real experiences remain, next time the
    agent records a new outcome in this category)

Leaves every other category's experiences and playbooks untouched.

Usage:
    python scripts/reset_category.py idor_bola             # interactive confirm
    python scripts/reset_category.py idor_bola --dry-run
    python scripts/reset_category.py idor_bola --yes
"""
import sys
import argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import load_config, resolve_path
from src.memory.db_models import get_session_factory
from src.learning.db_models import Playbook, Experience

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("category", help="e.g. idor_bola, authentication")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--yes", action="store_true")
    args = parser.parse_args()

    cfg = load_config()
    db_path = str(resolve_path(cfg["database"]["sqlite_path"]))
    SessionFactory = get_session_factory(db_path)

    with SessionFactory() as db:
        exp_q = db.query(Experience).filter(Experience.category == args.category)
        pb_q = db.query(Playbook).filter(Playbook.playbook_key == args.category)

        exp_count = exp_q.count()
        pb_count = pb_q.count()
        print(f"category={args.category!r}")
        print(f"  learning_experiences matching: {exp_count}")
        print(f"  learning_playbooks matching:    {pb_count}")

        if exp_count == 0 and pb_count == 0:
            print("Nothing to delete for this category.")
            sys.exit(0)

        if args.dry_run:
            print("\n--dry-run: nothing deleted.")
            sys.exit(0)

        if not args.yes:
            confirm = input(f"\nType 'yes' to delete these {exp_count + pb_count} rows: ").strip().lower()
            if confirm != "yes":
                print("Aborted, nothing deleted.")
                sys.exit(0)

        exp_q.delete()
        pb_q.delete()
        db.commit()
        print(f"\nDone. '{args.category}' experiences and playbook cleared. "
              "Other categories untouched.")