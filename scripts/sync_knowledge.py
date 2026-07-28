"""Run this after the Knowledge Collector Framework produces new processed
output. Never crawls anything itself — only chunks/embeds/indexes what
the collector already wrote to disk."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import load_config
from src.knowledge.knowledge_manager import KnowledgeManager

if __name__ == "__main__":
    cfg = load_config()
    km = KnowledgeManager(cfg)
    count = km.sync_from_collector()
    print(f"Indexed {count} knowledge chunks")
