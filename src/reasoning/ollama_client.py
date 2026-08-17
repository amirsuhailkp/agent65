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
                 context_window: int | None = None,
                 num_gpu: int | None = None,
                 keep_alive: str | None = "30m"):
        """
        num_gpu: passed straight through as Ollama's `num_gpu` option —
        the number of model layers to offload to GPU. -1 means "as many
        as will fit" (Ollama's own default behavior when unset), but on
        constrained VRAM Ollama's auto-detection can be conservative;
        setting this explicitly to a high number (e.g. 99) tells it to
        try to fit as many layers as physically possible rather than
        leaving a cautious margin. Left as None by default (no override)
        since this needs empirical tuning per machine — see the note in
        config/config.yaml about the 4GB-VRAM setup this was built on.

        keep_alive: how long Ollama keeps the model loaded in
        memory/VRAM after a call before unloading it. Defaults to "30m"
        (Ollama's own factory default is 5m) since this agent's cognitive
        cycles routinely have multi-minute gaps between LLM calls (tool
        dispatch, verification, etc.) — with the 5m default, a slow cycle
        could cause the model to unload and need a full reload (itself
        costly) on the next call. Set to "0" to unload immediately after
        each call if VRAM needs to be freed for something else between
        cycles, or a plain number of seconds / duration string otherwise.
        """
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
        self.num_gpu = num_gpu
        self.keep_alive = keep_alive

    def chat(self, messages: list[dict], format: str | None = None) -> str:
        """messages: [{"role": "system"|"user"|"assistant", "content": str}, ...]"""
        last_err = None
        options = {"temperature": self.temperature}
        if self.context_window:
            options["num_ctx"] = self.context_window
        if self.num_gpu is not None:
            options["num_gpu"] = self.num_gpu
        for attempt in range(1, self.max_retries + 1):
            try:
                log.info(f"LLM call -> model={self.model}")
                resp = self.client.chat(
                    model=self.model,
                    messages=messages,
                    options=options,
                    format=format,
                    keep_alive=self.keep_alive,
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