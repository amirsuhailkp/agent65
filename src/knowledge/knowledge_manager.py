"""Knowledge Manager — Vol II Ch11, Vol IV Ch4 (RAG pipeline) & Ch12 (retrieval).

Ingestion:  Collector output (already processed) -> Chunk -> Embed -> Vector DB
Retrieval:  Planner query -> search -> rank -> dedup -> concise context

The LLM is the CONSUMER of knowledge, never the source of truth (Vol IV Ch2).
"""
from __future__ import annotations
import datetime as dt
from .repository import KnowledgeRepository
from .chunking import chunk_document
from .embedding import get_embedding_backend
from .vector_store import VectorStore
from ..logging_setup import get_logger

log = get_logger("knowledge.manager")


class KnowledgeManager:
    def __init__(self, config: dict):
        kc_cfg = config["knowledge_collector"]
        db_cfg = config["database"]
        llm_cfg = config["llm"]

        self.repository = KnowledgeRepository(kc_cfg["processed_output_path"])
        self.embedder = get_embedding_backend(host=llm_cfg["host"])
        self.vector_store = VectorStore(
            persist_path=db_cfg["vector_db_path"],
            collection_name=db_cfg["vector_collection"],
        )

    # ---- Ingestion (run periodically / on-demand, never during collection itself) ----
    def sync_from_collector(self) -> int:
        """Pull whatever new processed docs the collector has produced and index them.
        Idempotent: upsert by chunk_id, safe to re-run."""
        total = 0
        for doc, body in self.repository.iter_documents():
            chunks = chunk_document(doc, body)
            if not chunks:
                continue
            embeddings = self.embedder.embed([c.text for c in chunks])
            total += self.vector_store.upsert_chunks(chunks, embeddings)
        log.info(f"Knowledge sync complete: {total} chunks indexed")
        return total

    def add_verified_item(self, item: dict):
        """Entry point for MemoryManager.promote_to_long_term — only ever called
        with user-approved / verified content (Vol IV Ch14 learning rules)."""
        from .chunking import KnowledgeChunk
        chunk = KnowledgeChunk(
            chunk_id=f"verified::{item.get('title', dt.datetime.utcnow().isoformat())}",
            doc_id="verified_notes",
            text=item.get("content", ""),
            title=item.get("title", "Verified note"),
            source="internal_verified",
            category=item.get("category", "methodology"),
            tags=item.get("tags", []),
            trust_level="verified",
            technology=item.get("technology", ""),
        )
        embedding = self.embedder.embed([chunk.text])
        self.vector_store.upsert_chunks([chunk], embedding)

    # ---- Retrieval (Vol IV Ch12) ----
    def retrieve(self, query: str, top_k: int = 6, category: str | None = None) -> list[dict]:
        query_emb = self.embedder.embed([query])[0]
        if not query_emb:
            log.error("Query embedding failed — returning no knowledge (never hallucinate)")
            return []
        where = {"category": category} if category else None
        res = self.vector_store.query(query_emb, top_k=top_k, where=where)

        results = []
        docs = res.get("documents", [[]])[0]
        metas = res.get("metadatas", [[]])[0]
        dists = res.get("distances", [[]])[0]
        seen_doc_ids = set()
        for text, meta, dist in zip(docs, metas, dists):
            if meta.get("doc_id") in seen_doc_ids:
                continue  # dedup near-identical chunks from same source
            seen_doc_ids.add(meta.get("doc_id"))
            results.append({
                "text": text,
                "title": meta.get("title"),
                "source": meta.get("source"),
                "trust_level": meta.get("trust_level"),
                "relevance": 1 - dist if dist is not None else None,
            })
        return results
