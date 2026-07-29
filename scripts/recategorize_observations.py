"""Run this after CATEGORY_ALIASES gains new entries (src/learning/
observation_extractor.py) to consolidate already-extracted observations
into the corrected categories. Zero LLM cost — just re-derives each
observation's category from its stored vulnerability text and
re-synthesizes any playbook categories that changed.

Usage:
    python scripts/recategorize_observations.py
"""
import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import load_config, resolve_path
from src.memory.db_models import get_session_factory
from src.learning.recategorize import recategorize_all

if __name__ == "__main__":
    cfg = load_config()
    db_path = str(resolve_path(cfg["database"]["sqlite_path"]))
    session_factory = get_session_factory(db_path)

    summary = recategorize_all(session_factory)
    print(json.dumps(summary, indent=2))
