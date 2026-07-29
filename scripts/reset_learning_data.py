"""Resets the Playbook Learning Engine's DERIVED tables so the next run
of scripts/run_learning_pipeline.py reprocesses every document from
scratch — e.g. right after improving the extraction prompt, so documents
that returned 0 observations under the old prompt get a fair second pass.

Wipes (all re-derivable from your immutable source documents):
  - learning_document_index  (SHA256 tracking — this is WHY reprocessing
    was being skipped; clearing it makes every doc look "new" again)
  - learning_observations    (would otherwise duplicate once documents
    are reprocessed — old + new observations for the same doc_id)
  - learning_playbooks       (stale synthesis built from the old,
    incomplete observation set)

Preserved by default:
  - learning_experiences     (real engagement outcomes are NOT derived
    from documents — there's no source to regenerate them from, so this
    table is left alone unless you explicitly pass --all)

Usage:
    python scripts/reset_learning_data.py             # interactive confirm
    python scripts/reset_learning_data.py --dry-run    # show counts only
    python scripts/reset_learning_data.py --all --yes  # also wipe Experience, skip confirm
"""
import sys
import argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import load_config, resolve_path
from src.memory.db_models import get_session_factory
from src.learning.db_models import DocumentIndex, Observation, Playbook, Experience

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true",
                         help="Also wipe Experience (real engagement outcomes) — off by default")
    parser.add_argument("--dry-run", action="store_true",
                         help="Show what would be deleted without deleting anything")
    parser.add_argument("--yes", action="store_true",
                         help="Skip the interactive confirmation prompt")
    args = parser.parse_args()

    cfg = load_config()
    db_path = str(resolve_path(cfg["database"]["sqlite_path"]))
    SessionFactory = get_session_factory(db_path)

    with SessionFactory() as db:
        counts = {
            "learning_document_index (SHA256 tracking)": db.query(DocumentIndex).count(),
            "learning_observations": db.query(Observation).count(),
            "learning_playbooks": db.query(Playbook).count(),
            "learning_experiences (real engagement outcomes)": db.query(Experience).count(),
        }
        print("Current row counts:")
        for k, v in counts.items():
            print(f"  {k}: {v}")

        if args.dry_run:
            print("\n--dry-run: nothing deleted.")
            sys.exit(0)

        will_wipe_experience = args.all
        print(
            f"\nThis will DELETE all rows from: learning_document_index, "
            f"learning_observations, learning_playbooks"
            + (", learning_experiences." if will_wipe_experience else
               " — learning_experiences will be KEPT (pass --all to wipe it too).")
        )
        print("Your immutable source documents (knowledge_collector/processed/) are NOT touched.")

        if not args.yes:
            confirm = input("\nType 'yes' to proceed: ").strip().lower()
            if confirm != "yes":
                print("Aborted, nothing deleted.")
                sys.exit(0)

        db.query(DocumentIndex).delete()
        db.query(Observation).delete()
        db.query(Playbook).delete()
        if will_wipe_experience:
            db.query(Experience).delete()
        db.commit()

        print("\nDone. Every document is now untracked — the next run of "
              "scripts/run_learning_pipeline.py will reprocess everything from scratch.")
