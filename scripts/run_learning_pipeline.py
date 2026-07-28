"""Run this to extract observations from whatever the Knowledge Collector
has newly produced, and (re)synthesize playbooks for any touched category.

Never reprocesses already-indexed, unmodified documents (SHA256-tracked
in the learning_document_index table) — safe and cheap to re-run often,
e.g. right after scripts/sync_knowledge.py in a cron job.

Usage:
    python scripts/run_learning_pipeline.py
"""
import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import load_config, resolve_path
from src.memory.db_models import get_session_factory
from src.knowledge.repository import KnowledgeRepository
from src.reasoning.ollama_client import OllamaClient
from src.learning.learning_engine import LearningEngine

if __name__ == "__main__":
    cfg = load_config()
    db_path = str(resolve_path(cfg["database"]["sqlite_path"]))
    session_factory = get_session_factory(db_path)

    repository = KnowledgeRepository(cfg["knowledge_collector"]["processed_output_path"])
    # Deep model — this pipeline runs offline/infrequently, so extraction
    # quality matters more than latency here (mirrors main.py's wiring).
    deep_cfg = cfg.get("llm_deep", cfg["llm"])
    llm_client = OllamaClient(
        host=deep_cfg["host"], model=deep_cfg["model"],
        temperature=deep_cfg["temperature"], max_retries=deep_cfg["max_retries"],
        backoff_base_seconds=deep_cfg["backoff_base_seconds"],
    )

    engine = LearningEngine(repository=repository, session_factory=session_factory, llm_client=llm_client,
                             config=cfg.get("learning", {}))
    summary = engine.import_knowledge()
    print(json.dumps(summary, indent=2))
