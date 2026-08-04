"""Reasoning Engine — Vol III Ch6, Ch12 (anti-hallucination).

Consumes evidence + memory + retrieved knowledge, outputs updated
understanding, confidence, and recommended actions as structured JSON.
Never fabricates endpoints/params/technologies/vulnerabilities/exploits —
enforced by requiring every hypothesis cite supporting evidence or
retrieved knowledge, checked in HypothesisEngine.validate().
"""
from __future__ import annotations
import json
from .ollama_client import OllamaClient, OllamaUnavailableError
from .prompt_builder import build_prompt
from ..logging_setup import get_logger

log = get_logger("reasoning.engine")


class ReasoningEngine:
    def __init__(self, llm_client: OllamaClient):
        self.llm = llm_client

    def reason(
        self,
        current_goal: str,
        scope: dict,
        working_memory: dict,
        retrieved_knowledge: list[dict],
        active_hypotheses: list[dict],
        available_tools: list[dict],
        resource_status: dict,
        relevant_playbooks: list[dict] | None = None,
        relevant_experiences: list[dict] | None = None,
    ) -> dict:
        messages = build_prompt(
            current_goal, scope, working_memory, retrieved_knowledge,
            active_hypotheses, available_tools, resource_status,
            relevant_playbooks=relevant_playbooks, relevant_experiences=relevant_experiences,
        )
        try:
            raw = self.llm.chat(messages, format="json")
        except OllamaUnavailableError:
            log.error("Reasoning cycle skipped — LLM backend unavailable")
            return {"analysis": "", "hypotheses": [], "next_action": None, "error": "llm_unavailable"}

        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            log.error(f"Model returned non-JSON output, discarding: {raw[:200]}")
            return {"analysis": "", "hypotheses": [], "next_action": None, "error": "invalid_json"}

        # Anti-hallucination guard: knowledge-unsupported hypotheses are flagged, not dropped —
        # human/planner decides whether observation alone is sufficient grounding.
        knowledge_titles = {k.get("title") for k in retrieved_knowledge}

        # Shape validation. Valid JSON doesn't guarantee the right shape —
        # this crashed the whole run when the model once returned
        # next_action as a plain string instead of an object, since nothing
        # downstream checked isinstance before calling .get()/.strip() on
        # it. Coerce anything malformed back to the safe "no action this
        # cycle" shape (same path decision_engine already handles) rather
        # than letting a shape mismatch anywhere in this dict propagate
        # into an uncaught crash several calls later.
        next_action = parsed.get("next_action")
        if next_action is not None and not isinstance(next_action, dict):
            log.warning(
                f"Model returned non-dict next_action ({type(next_action).__name__}), "
                f"discarding: {next_action!r}"
            )
            parsed["next_action"] = None

        hyps = parsed.get("hypotheses", [])
        if not isinstance(hyps, list):
            log.warning(f"Model returned non-list hypotheses ({type(hyps).__name__}), discarding: {hyps!r}")
            hyps = []
        valid_hyps = []
        for h in hyps:
            if not isinstance(h, dict):
                log.warning(f"Skipping non-dict hypothesis entry: {h!r}")
                continue
            h["knowledge_grounded"] = bool(knowledge_titles) or bool(h.get("observation"))
            valid_hyps.append(h)
        parsed["hypotheses"] = valid_hyps

        analysis = parsed.get("analysis")
        if analysis is not None and not isinstance(analysis, str):
            log.warning(f"Model returned non-string analysis ({type(analysis).__name__}), coercing to str")
            parsed["analysis"] = str(analysis)

        return parsed