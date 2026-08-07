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
                 max_retries: int = 3, backoff_base_seconds: int = 2,
                 context_window: int | None = None):
        self.client = ollama.Client(host=host)
        self.model = model
        self.temperature = temperature
        self.max_retries = max_retries
        self.backoff_base_seconds = backoff_base_seconds
        # Was previously declared in config.yaml (llm.context_window: 8192)
        # but never actually read anywhere — this class silently ignored it
        # and every call fell back to Ollama's own default, which is 2048-4096
        # tokens depending on version/available VRAM, NOT 8192. Ollama does
        # not error or warn when this is exceeded — it silently drops the
        # OLDEST tokens to make room. Since build_prompt() puts the most
        # constraint-critical content (target, correction) at the END of a
        # single flattened message specifically so it survives this, an
        # unset num_ctx meant every cycle past a certain accumulated
        # hypotheses/knowledge size was silently reasoning over a truncated
        # prompt with no indication anything was missing.
        self.context_window = context_window

    def chat(self, messages: list[dict], format: str | None = None) -> str:
        """messages: [{"role": "system"|"user"|"assistant", "content": str}, ...]"""
        last_err = None
        options = {"temperature": self.temperature}
        if self.context_window:
            options["num_ctx"] = self.context_window
        for attempt in range(1, self.max_retries + 1):
            try:
                log.info(f"LLM call -> model={self.model}")
                resp = self.client.chat(
                    model=self.model,
                    messages=messages,
                    options=options,
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