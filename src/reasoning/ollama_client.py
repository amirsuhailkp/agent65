"""Ollama abstraction layer — Vol VI Ch9.

Planner talks to this, never to `ollama` package directly. Wraps chat()
with exponential backoff (the fix for the LLM-backend 500 crash you hit
against scanme.nmap.org).
"""
from __future__ import annotations
import time
import ollama
from ..logging_setup import get_logger

log = get_logger("reasoning.ollama_client")


class OllamaUnavailableError(Exception):
    pass


class OllamaClient:
    def __init__(self, host: str, model: str, temperature: float = 0.2,
                 max_retries: int = 3, backoff_base_seconds: int = 2):
        self.client = ollama.Client(host=host)
        self.model = model
        self.temperature = temperature
        self.max_retries = max_retries
        self.backoff_base_seconds = backoff_base_seconds

    def chat(self, messages: list[dict], format: str | None = None) -> str:
        """messages: [{"role": "system"|"user"|"assistant", "content": str}, ...]"""
        last_err = None
        for attempt in range(1, self.max_retries + 1):
            try:
                log.info(f"LLM call -> model={self.model}")
                resp = self.client.chat(
                    model=self.model,
                    messages=messages,
                    options={"temperature": self.temperature},
                    format=format,
                )
                return resp["message"]["content"]
            except Exception as e:
                last_err = e
                wait = self.backoff_base_seconds ** attempt
                log.warning(
                    f"llm.chat() failed (attempt {attempt}/{self.max_retries}): {e}. "
                    f"Retrying in {wait}s."
                )
                time.sleep(wait)
        log.error(f"Ollama backend unavailable after {self.max_retries} attempts: {last_err}")
        raise OllamaUnavailableError(str(last_err))
