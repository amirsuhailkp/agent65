"""Vector Database wrapper (ChromaDB) — Vol IV Ch16, Vol II Ch22."""
from __future__ import annotations
import chromadb
from ..logging_setup import get_logger

log = get_logger("knowledge.vector_store")


class VectorStore:
    def __init__(self, persist_path: str, collection_name: str):
        self.client = chromadb.PersistentClient(path=persist_path)
        self.collection = self.client.get_or_create_collection(collection_name)

    def upsert_chunks(self, chunks, embeddings) -> int:
        ids, docs, metas, embs = [], [], [], []
        for chunk, emb in zip(chunks, embeddings):
            if not emb:
                continue
            ids.append(chunk.chunk_id)
            docs.append(chunk.text)
            metas.append({
                "doc_id": chunk.doc_id,
                "title": chunk.title,
                "source": chunk.source,
                "category": chunk.category,
                "tags": ",".join(chunk.tags) if chunk.tags else "",
                "trust_level": chunk.trust_level,
                "technology": chunk.technology,
            })
            embs.append(emb)
        if ids:
            self.collection.upsert(ids=ids, documents=docs, metadatas=metas, embeddings=embs)
            log.info(f"Upserted {len(ids)} chunks into vector store")
        return len(ids)

    def query(self, query_embedding: list[float], top_k: int = 6, where: dict | None = None):
        res = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where,
        )
        return res
