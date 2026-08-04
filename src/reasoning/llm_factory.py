"""Builds an LLM client from a config block, dispatching on `provider`.

Every client this returns is duck-typed identically: `.chat(messages,
format=None) -> str`. Callers (LearningEngine, ReasoningEngine,
ImpactAssessor, ...) never need to know or care which backend is behind it.

config block shape:

    provider: ollama            # or: cloud
    # --- ollama fields ---
    host: "http://127.0.0.1:11434"
    model: "qwen3:8b"
    # --- cloud fields (OpenAI-compatible endpoint, e.g. FreeLLMAPI) ---
    base_url: "http://localhost:3001/v1"
    model: "auto"
    api_key_env: "FREELLMAPI_API_KEY"   # optional, this is the default
    # --- shared fields ---
    temperature: 0.1
    max_retries: 3
    backoff_base_seconds: 2
"""
from __future__ import annotations
from .ollama_client import OllamaClient
from .cloud_llm_client import CloudLLMClient


def build_llm_client(cfg: dict):
    provider = (cfg.get("provider") or "ollama").lower()

    if provider == "ollama":
        return OllamaClient(
            host=cfg["host"],
            model=cfg["model"],
            temperature=cfg.get("temperature", 0.2),
            max_retries=cfg.get("max_retries", 3),
            backoff_base_seconds=cfg.get("backoff_base_seconds", 2),
        )

    if provider in ("cloud", "openai_compatible", "freellmapi"):
        return CloudLLMClient(
            base_url=cfg["base_url"],
            model=cfg.get("model", "auto"),
            api_key=cfg.get("api_key"),  # normally omitted — use api_key_env instead
            api_key_env=cfg.get("api_key_env", "FREELLMAPI_API_KEY"),
            temperature=cfg.get("temperature", 0.1),
            max_retries=cfg.get("max_retries", 3),
            backoff_base_seconds=cfg.get("backoff_base_seconds", 2),
        )

    raise ValueError(f"Unknown llm provider: {provider!r} (expected 'ollama' or 'cloud')")
