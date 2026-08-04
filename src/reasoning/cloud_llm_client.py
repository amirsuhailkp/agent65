"""Cloud LLM abstraction layer — OpenAI-compatible endpoint (e.g. FreeLLMAPI).

Same duck-typed interface as OllamaClient: `.chat(messages, format=None) -> str`.
Used ONLY by the offline Playbook Learning Engine (src/learning/), which
extracts structured observations from already-collected, already-public
knowledge-base documents (OWASP/PortSwigger/HackTricks-style writeups).
It is deliberately NOT wired into the hot reasoning loop, the decision
engine, or ImpactAssessor's live-evidence judgment — those stay on the
local Ollama models (see config.yaml comments + README "Two-Model Hybrid"
section for why).

Requires: pip install openai --break-system-packages
"""
from __future__ import annotations
import os
import time
from openai import OpenAI, APIError, APIConnectionError, RateLimitError
from ..logging_setup import get_logger

log = get_logger("reasoning.cloud_llm_client")


class CloudLLMUnavailableError(Exception):
    pass


class CloudLLMClient:
    def __init__(
        self,
        base_url: str,
        model: str,
        api_key: str | None = None,
        api_key_env: str = "FREELLMAPI_API_KEY",
        temperature: float = 0.1,
        max_retries: int = 3,
        backoff_base_seconds: int = 2,
        request_timeout: int = 120,
    ):
        """
        base_url: e.g. "http://localhost:3001/v1" for a local FreeLLMAPI instance.
        model: e.g. "auto" (let FreeLLMAPI's router pick) or a pinned model id
               such as "gemini-2.5-flash" — see freellmapi.co/models.
        api_key: pass directly, OR leave None and set it via the env var named
                 by `api_key_env` (recommended — keeps the key out of config.yaml
                 and out of source control).
        """
        key = api_key or os.environ.get(api_key_env)
        if not key:
            raise ValueError(
                f"No API key provided and env var {api_key_env} is not set. "
                f"Set it to your FreeLLMAPI unified key (starts with 'freellmapi-')."
            )
        self.client = OpenAI(base_url=base_url, api_key=key, timeout=request_timeout)
        self.model = model
        self.temperature = temperature
        self.max_retries = max_retries
        self.backoff_base_seconds = backoff_base_seconds

    def chat(self, messages: list[dict], format: str | None = None) -> str:
        """messages: [{"role": "system"|"user"|"assistant", "content": str}, ...]
        format: pass "json" to request a JSON object response (maps to
        OpenAI-style response_format), same convention as OllamaClient."""
        kwargs = {}
        if format == "json":
            kwargs["response_format"] = {"type": "json_object"}

        last_err = None
        for attempt in range(1, self.max_retries + 1):
            try:
                log.info(f"Cloud LLM call -> model={self.model}")
                resp = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=self.temperature,
                    **kwargs,
                )
                routed_via = getattr(resp, "model", self.model)
                log.info(f"Cloud LLM response served by: {routed_via}")
                return resp.choices[0].message.content or ""
            except (APIConnectionError, RateLimitError, APIError) as e:
                last_err = e
                wait = self.backoff_base_seconds ** attempt
                log.warning(
                    f"cloud_llm.chat() failed (attempt {attempt}/{self.max_retries}): {e}. "
                    f"Retrying in {wait}s."
                )
                time.sleep(wait)
            except Exception as e:
                # Non-retryable (bad request, auth failure, etc.) — fail fast.
                log.error(f"Cloud LLM call failed non-retryably: {e}")
                raise CloudLLMUnavailableError(str(e)) from e
        log.error(f"Cloud LLM backend unavailable after {self.max_retries} attempts: {last_err}")
        raise CloudLLMUnavailableError(str(last_err))
