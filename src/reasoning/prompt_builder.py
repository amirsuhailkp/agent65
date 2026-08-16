"""Prompt Architecture — Vol III Ch14.

Fixed section order keeps prompts consistent and modular so the 8B model
gets a compact, high-value context (Vol III Ch5, Ch15).
"""
from __future__ import annotations
import json

SYSTEM_IDENTITY = """You are the reasoning core of Agent Cyber, an authorized bug bounty \
research assistant. You reason like an experienced bug bounty hunter focused on IDOR/BOLA, \
business logic flaws, API security, and authentication/session management.

You NEVER claim a finding, vulnerability, or exploit exists without test evidence to back it. \
You NEVER fabricate scan results, assert a technology/CVE is present without verification, or \
invent an endpoint that isn't implied by the target, scope, or retrieved knowledge. If evidence \
does not support a claim, say so explicitly.

This does NOT mean refusing to act when you don't yet know a parameter name — not knowing one \
is the normal starting condition for IDOR testing, not a reason to stop. Proposing a candidate \
parameter to TEST (e.g. via diff_requests or httpx) is hypothesis generation, not invention, \
especially when it's grounded in evidence already surfaced this engagement (a hint in a prior \
tool's output, a known pattern for the target's technology) or in your own domain knowledge of \
how similar applications are typically built. A low-confidence hypothesis is exactly what you \
test next to gather more evidence — it is not a dead end. Only stop and report "insufficient \
evidence" if you've actually run out of untested, reasonably-motivated candidates, not merely \
because none has been confirmed yet.

Know what actually counts as IDOR evidence before claiming a finding: two requests returning \
IDENTICAL content (same length, same body) for two different parameter values is NOT evidence \
of IDOR — on its own it usually means the parameter had no effect at all (wrong name, ignored \
by the endpoint, or the app needs a session/cookie neither request sent, so both just got the \
same generic/default page). That is a negative result, not a vulnerability. A real IDOR finding \
requires the two responses to DIFFER in a way that reveals data specific to a different \
identity than the one making the request — e.g. a different user's actual post content, name, \
or record appearing when you had no authorization to see it. If two responses are identical, \
say so plainly and move to a different candidate; do not describe it as "no access control \
enforced" or a confirmed vulnerability.

The same caution applies in the other direction: identical responses for ONE specific pair of \
values (e.g. author=admin vs author=user1) is a negative result for THOSE TWO VALUES ONLY — it \
is NOT grounds to conclude "no IDOR vulnerability" for the endpoint or parameter as a whole. A \
guessed value can fail for reasons that have nothing to do with whether the parameter is \
exploitable — most commonly, the account you picked simply has no seeded data to leak (an empty \
account looks identical to a broken parameter from the outside). Before closing a hypothesis as \
"confirmed not vulnerable," check the # Scope section for a `known_credentials` list: if it's \
present and you haven't yet tested with those specific values, that is untested surface, not a \
dead end — retry with them before concluding anything. Only treat a hypothesis as genuinely \
exhausted after testing against known-good values (or, absent any, at least 2-3 distinct \
plausible values) and getting identical results across all of them. If deep_review on a prior \
attempt noted a secondary signal even when the response body was identical — e.g. the backend \
query itself changed shape based on the parameter — that is active evidence the parameter IS \
being processed by the application, which argues for testing further values, not for closing \
the hypothesis.

Do not assume a login/session is required just because `known_credentials` exist in scope — a \
username/password pair being documented does not mean authentication is the next step. Many \
vulnerable endpoints (Mutillidae's view-someones-blog.php is a concrete example already in this \
engagement's history) take the username directly as an unauthenticated parameter value with no \
session involved at all. Try the direct, unauthenticated request FIRST. Only pursue an actual \
login flow if a direct attempt is demonstrably rejected — a 401/403 status, or a redirect to a \
login page — not preemptively. And if you do need to log in, know the limits of your tools: a \
one-off HTTP tool with no cookie jar (like httpx here) proves credentials are valid but does NOT \
carry a session into any later, separate tool call — a successful login response alone is not \
enough to then treat a following unauthenticated request as if it were authenticated.

If `session_auth_ground_truth` is present in # Scope, it is established fact about THIS \
engagement, not something to independently verify from scratch — you may not have another way to \
learn it. A named cookie (e.g. under `session_cookie_name` or `secondary_auth_cookie`) is a real, \
concrete parameter you may test directly (e.g. manipulating its value to attempt privilege \
escalation or auth bypass) — this is using given ground truth, not inventing an endpoint. If \
`account_lockout_present` is explicitly `false`, treat "does repeated failed login trigger \
lockout" as already answered: either skip generating that hypothesis at all, or if it's already \
active, resolve it directly to a negative/rejected outcome without spending a live tool call to \
re-discover a fact already given to you."""

MISSION = "Observe evidence, retrieve knowledge, generate ranked hypotheses, select the " \
          "next best action. Optimize for coverage and reasoning quality, not raw request count. " \
          "A goal can name more than one distinct target (e.g. \"blog posts and credit card " \
          "records\" is two separate objectives, not one investigation with two names). Track " \
          "them separately. Exhausting your hypotheses for ONE named target and confirming it's " \
          "not vulnerable is progress on that target, not a reason to conclude the whole goal is " \
          "done — pivot to the next unaddressed target named in the goal before considering the " \
          "engagement finished."

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
fill them in.

next_action MUST always be a JSON object with exactly the four keys above —
never a bare string, never a sentence describing what to do. If you don't
have a next action this cycle, set next_action to null (JSON null, not the
word "none" or an empty string) — do NOT put the tool name or a description
of the action there instead.
WRONG:  "next_action": "diff_requests"
WRONG:  "next_action": "Use httpx to test user_id=1 on the target"
RIGHT:  "next_action": {"tool": "diff_requests", "params": {"url_a": "...", "url_b": "..."}, "reason": "...", "risk_level": "low"}
RIGHT (no action this cycle):  "next_action": null"""


def _split_goal_items(goal: str) -> list[str]:
    """Best-effort split of a comma-separated, "and"-joined goal string into
    individual sub-objectives, e.g. "X, Y, and Z" -> ["X", "Y", "Z"].

    Deliberately conservative: only splits on commas (the pattern every
    goal string used so far actually follows), and only strips a leading
    "and " off the final segment. Goals without commas are left as a
    single item — we'd rather show no checklist than a wrong one built
    from a shakier heuristic (e.g. splitting on " and " alone would wrongly
    break apart a phrase like "cookie manipulation or direct URL access").
    """
    parts = [p.strip() for p in goal.split(",") if p.strip()]
    if len(parts) > 1 and parts[-1].lower().startswith("and "):
        parts[-1] = parts[-1][4:].strip()
    return parts


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
    target: str | None = None,
    correction: str | None = None,
) -> list[dict]:
    relevant_playbooks = relevant_playbooks or []
    relevant_experiences = relevant_experiences or []
    goal_items = _split_goal_items(current_goal)
    target_section = (
        f"# Target\n{target}\n\n"
        "This is the EXACT, canonical target string for this engagement. "
        "Copy it verbatim into any target/url/host param you choose — do not "
        "retype it from memory, shorten it, drop segments, or invent a "
        "different host/path. If you're unsure which endpoint to hit, reuse "
        "this string exactly rather than guessing a variant."
        if target else
        "# Target\n(no explicit target provided — infer only from Scope below, "
        "and stay conservative)"
    )
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
        "repeating known failures or false positives. Any entry marked "
        "[CONFIRMED VULNERABILITY] was already verified and reported in a prior "
        "session — treat it as established ground truth, not a hypothesis to "
        "re-derive. Do NOT let a fresh inconclusive/negative result on a "
        "DIFFERENT parameter value talk you out of something already confirmed "
        "on a SPECIFIC value pair (e.g. a confirmed admin-vs-samurai result is "
        "not contradicted by an inconclusive samurai-vs-john result — they are "
        "different tests). If a confirmed finding is listed here, either build on "
        "it (deeper exploitation, related endpoints) or move to the goal's other "
        "targets — don't spend cycles re-proving it.\n" + (
            "\n---\n".join(
                f"[{'CONFIRMED VULNERABILITY' if e.get('outcome') == 'success' else e.get('outcome')}] "
                f"{e.get('description') or e.get('reason') or '(no detail recorded)'} "
                f"({e.get('technology') or 'generic'})"
                for e in relevant_experiences
            ) or "(no recorded experience for this category yet)"
        ),
        f"# Active Hypotheses\n{json.dumps(active_hypotheses, indent=2)}",
    ]
    if len(goal_items) > 1:
        sections.append(
            "# Goal Checklist\n"
            "This goal has multiple distinct sub-objectives, split out below. "
            "Testing one of these to a conclusion (positive OR negative) is "
            "progress on THAT item only — it is not grounds to set "
            "next_action to null. Before concluding there is nothing left to "
            "do this cycle, check this list against Active Hypotheses and "
            "Relevant Experience above: if any item here has no hypothesis "
            "or experience addressing it yet, that is your next action, not "
            "a reason to stop.\n"
            + "\n".join(f"- {item}" for item in goal_items)
        )
    sections += [
        "# Available Tools\n"
        "Each tool lists its exact accepted param keys under \"params\". "
        "Only use keys listed there — inventing a param name means it gets "
        "silently ignored at execution time. Anything in \"defaults\" is "
        "already filled in if you omit it.\n"
        f"{json.dumps(available_tools, indent=2)}",
        f"# Resource Status\n{json.dumps(resource_status, indent=2)}",
        # Target and (if present) Correction are placed LAST, immediately
        # before Required Output Format, rather than at the top. Two
        # independent reasons converge on the same fix: (1) Ollama's
        # num_ctx truncation drops from the FRONT of the prompt with no
        # warning when the accumulated Knowledge/Playbook/Hypotheses
        # sections above push the whole thing over the context window —
        # content placed early was the first casualty, silently, on
        # exactly the cycles where it mattered most (later cycles with
        # more accumulated context). (2) even well within the context
        # window, instruction-following in small models is generally most
        # reliable for content nearest the point of generation. Putting
        # the single most load-bearing fact (the literal target string)
        # and the single most urgent instruction (a same-cycle correction)
        # last protects them on both counts instead of neither.
        target_section,
    ]
    if correction:
        sections.append(f"# CORRECTION — READ THIS FIRST\n{correction}")
    sections.append(f"# Required Output Format\n{OUTPUT_FORMAT}")
    return [{"role": "system", "content": "\n\n".join(sections)}]