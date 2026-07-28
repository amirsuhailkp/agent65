"""Idempotent DB init — Vol VI Ch10. Safe to re-run."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import load_config, resolve_path
from src.memory.db_models import get_engine
# Import registers Observation/Playbook/Experience/DocumentIndex on the
# SAME Base as the rest of the schema — must happen before get_engine()
# calls Base.metadata.create_all(), or these tables never get created.
import src.learning.db_models  # noqa: F401

if __name__ == "__main__":
    cfg = load_config()
    db_path = str(resolve_path(cfg["database"]["sqlite_path"]))
    get_engine(db_path)
    print(f"Database ready at {db_path}")
