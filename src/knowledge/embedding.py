"""Embedding Strategy — Vol IV Ch6.

Abstraction layer so the embedding model can be swapped without touching
callers. Default backend uses Ollama's embedding endpoint (local, matches
the fully-local design constraint).
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Sequence
import ollama
from ..logging_setup import get_logger

log = get_logger("knowledge.embedding")


class EmbeddingBackend(ABC):
    @abstractmethod
    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        ...


class OllamaEmbeddingBackend(EmbeddingBackend):
    # Conservative char cap as a last-resort safety net. nomic-embed-text's
    # context window is token-based, not char-based, but ~4 chars/token is a
    # safe rule of thumb — this only kicks in if chunking.py's own bound
    # (MAX_CHUNK_CHARS) was bypassed, e.g. by a single oversized atomic code
    # block that can't be split without breaking Vol IV Ch7's rule.
    HARD_CHAR_CAP = 6000

    def __init__(self, host: str, model: str = "nomic-embed-text"):
        self.client = ollama.Client(host=host)
        self.model = model

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        vectors = []
        for t in texts:
            vectors.append(self._embed_one(t))
        return vectors

    def _embed_one(self, text: str) -> list[float]:
        try:
            resp = self.client.embeddings(model=self.model, prompt=text)
            return resp["embedding"]
        except Exception as e:
            if len(text) > self.HARD_CHAR_CAP:
                log.warning(
                    f"Chunk too long for embedding context ({len(text)} chars), "
                    f"retrying truncated to {self.HARD_CHAR_CAP} chars rather than dropping it"
                )
                try:
                    resp = self.client.embeddings(
                        model=self.model, prompt=text[: self.HARD_CHAR_CAP]
                    )
                    return resp["embedding"]
                except Exception as e2:
                    log.error(f"Embedding still failed after truncation, skipping chunk: {e2}")
                    return []
            log.error(f"Embedding failed, skipping chunk: {e}")
            return []


def get_embedding_backend(host: str, model: str = "nomic-embed-text") -> EmbeddingBackend:
    return OllamaEmbeddingBackend(host=host, model=model)
