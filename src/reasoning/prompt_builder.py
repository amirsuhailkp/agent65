"""Prompt Architecture — Vol III Ch14.

Fixed section order keeps prompts consistent and modular so the 8B model
gets a compact, high-value context (Vol III Ch5, Ch15).
"""
from __future__ import annotations
import json

SYSTEM_IDENTITY = """You are the reasoning core of Agent Cyber, an authorized bug bounty \
research assistant. You NEVER invent endpoints, parameters, technologies, vulnerabilities, \
or exploits. If evidence does not support a claim, say so explicitly. You reason like an \
experienced bug bounty hunter focused on IDOR/BOLA, business logic flaws, API security, \
and authentication/session management."""

MISSION = "Observe evidence, retrieve knowledge, generate ranked hypotheses, select the " \
          "next best action. Optimize for coverage and reasoning quality, not raw request count."

OUTPUT_FORMAT = """Respond ONLY with JSON matching:
{
  "analysis": "what the evidence implies and which assumptions are being made",
  "hypotheses": [
    {"observation": "...", "attack_strategy": "...", "confidence": 0.0, "rationale": "..."}
  ],
  "next_action": {
    "tool": "...",
    "params": {"...": "..."},
    "reason": "...",
    "risk_level": "low|medium|high"
  }
}
`params` should include any tool-specific inputs beyond the target (e.g. nuclei
needs "severity"). Omit params you're unsure about — registry defaults will
fill them in."""


def build_prompt(
    current_goal: str,
    scope: dict,
    working_memory: dict,
    retrieved_knowledge: list[dict],
    active_hypotheses: list[dict],
    available_tools: list[dict],
    resource_status: dict,
    relevant_playbooks: list[dict] | None = None,
    relevant_experiences: list[dict] | None = None,
) -> list[dict]:
    relevant_playbooks = relevant_playbooks or []
    relevant_experiences = relevant_experiences or []
    sections = [
        f"# System Identity\n{SYSTEM_IDENTITY}",
        f"# Mission\n{MISSION}",
        f"# Current Goal\n{current_goal}",
        f"# Scope\n{json.dumps(scope, indent=2)}",
        f"# Working Memory\n{json.dumps(working_memory, indent=2)}",
        "# Retrieved Knowledge\n" + (
            "\n---\n".join(
                f"[{k.get('source')}] ({k.get('trust_level')}) {k.get('title')}\n{k.get('text')}"
                for k in retrieved_knowledge
            ) or "(no relevant knowledge retrieved — reason conservatively)"
        ),
        "# Relevant Playbooks\n"
        "Synthesized methodologies from many prior reports, ranked by confidence. "
        "Prefer high-confidence playbooks but weigh alternatives — none of these are "
        "guarantees for this specific target.\n" + (
            "\n---\n".join(
                f"[{p.get('category')} v{p.get('version')}] {p.get('name')} "
                f"(confidence={p.get('confidence')})\n"
                f"Workflow: {' -> '.join(p.get('workflow', []))}\n"
                f"Common mistakes: {', '.join(p.get('common_mistakes', []))}\n"
                f"Best tools: {', '.join(p.get('best_tools', []))}"
                for p in relevant_playbooks
            ) or "(no synthesized playbook yet for this goal — reason from raw knowledge only)"
        ),
        "# Relevant Experience\n"
        "Real outcomes from past engagements on this category — use these to avoid "
        "repeating known failures or false positives.\n" + (
            "\n---\n".join(
                f"[{e.get('outcome')}] {e.get('reason') or '(no reason recorded)'} "
                f"({e.get('technology') or 'generic'})"
                for e in relevant_experiences
            ) or "(no recorded experience for this category yet)"
        ),
        f"# Active Hypotheses\n{json.dumps(active_hypotheses, indent=2)}",
        "# Available Tools\n"
        "Each tool lists its exact accepted param keys under \"params\". "
        "Only use keys listed there — inventing a param name means it gets "
        "silently ignored at execution time. Anything in \"defaults\" is "
        "already filled in if you omit it.\n"
        f"{json.dumps(available_tools, indent=2)}",
        f"# Resource Status\n{json.dumps(resource_status, indent=2)}",
        f"# Required Output Format\n{OUTPUT_FORMAT}",
    ]
    return [{"role": "system", "content": "\n\n".join(sections)}]
