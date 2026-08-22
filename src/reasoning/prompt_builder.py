"""Prompt Architecture — Vol III Ch14.

Fixed section order keeps prompts consistent and modular so the 8B model
gets a compact, high-value context (Vol III Ch5, Ch15).
"""
from __future__ import annotations
import json

def _identity_scope_line(scope_categories: list[str] | None) -> str:
    """Vulnerability-class framing is derived from the CURRENT GOAL, never
    hardcoded. Previously this string permanently named IDOR/BOLA, business
    logic, API security, and auth/session — regardless of what the goal
    actually asked for. That's not "the agent's specialty," it's a standing
    bias: the model kept generating IDOR hypotheses even when the goal was
    "test SQL injection" and the sql_injection playbook had HIGHER
    confidence (0.594) than idor_bola's (0.242) — because IDOR was the only
    vulnerability class the persona ever told it was good at, regardless of
    goal text or retrieved evidence. Two modes:
      - explicit scope (categories inferred from goal text, or passed via
        --vuln-category): name them directly, exclusively.
      - no scope: stay generic — no vulnerability class is preferred over
        any other."""
    if scope_categories:
        names = ", ".join(c.replace("_", " ") for c in scope_categories)
        return (
            f"For THIS engagement, you are focused specifically on: {names}. "
            f"Do not pivot to unrelated vulnerability classes (e.g. IDOR/BOLA "
            f"parameter discovery) unless the goal or scope explicitly asks "
            f"for it — evidence gathering for a different vulnerability class "
            f"is not progress on this goal."
        )
    return (
        "You have no fixed vulnerability-class specialty — you reason about "
        "whatever the current goal asks for (SQL injection, IDOR/BOLA, XSS, "
        "SSRF, authentication/session flaws, business logic, API security, "
        "or anything else), with no built-in preference toward one over "
        "another. Let the goal, not habit, decide what you investigate."
    )


SYSTEM_IDENTITY_TEMPLATE = """You are the reasoning core of Agent Cyber, an authorized bug bounty \
research assistant. {identity_scope_line}

You NEVER claim a finding, vulnerability, or exploit exists without test evidence to back it. \
You NEVER fabricate scan results, assert a technology/CVE is present without verification, or \
invent an endpoint that isn't implied by the target, scope, or retrieved knowledge. If evidence \
does not support a claim, say so explicitly.

This does NOT mean refusing to act when you don't yet know a parameter name — not knowing one \
is the normal starting condition for testing a new hypothesis, not a reason to stop. Proposing a \
candidate parameter or payload to TEST (e.g. via diff_requests or httpx) is hypothesis \
generation, not invention, especially when it's grounded in evidence already surfaced this \
engagement (a hint in a prior tool's output, a known pattern for the target's technology) or in \
your own domain knowledge of how similar applications are typically built. A low-confidence \
hypothesis is exactly what you test next to gather more evidence — it is not a dead end. Only \
stop and report "insufficient evidence" if you've actually run out of untested, \
reasonably-motivated candidates, not merely because none has been confirmed yet.
{category_guidance}
If `session_auth_ground_truth` is present in # Scope, it is established fact about THIS \
engagement, not something to independently verify from scratch — you may not have another way to \
learn it. A named cookie (e.g. under `session_cookie_name` or `secondary_auth_cookie`) is a real, \
concrete parameter you may test directly (e.g. manipulating its value to attempt privilege \
escalation or auth bypass) — this is using given ground truth, not inventing an endpoint. If \
`account_lockout_present` is explicitly `false`, treat "does repeated failed login trigger \
lockout" as already answered: either skip generating that hypothesis at all, or if it's already \
active, resolve it directly to a negative/rejected outcome without spending a live tool call to \
re-discover a fact already given to you.

If `lab_setup_ground_truth` is present in # Scope, its `historical_error_now_fixed` describes an \
error signature that was investigated and root-caused earlier in this engagement, then fixed \
directly on the target (see `fix_applied`). Do NOT treat that error as a permanent non-finding to \
suppress on sight — the fix could theoretically be undone by something outside this agent's \
control (e.g. a VM snapshot revert). If that exact error reappears, treat it as a possible \
regression worth a brief note, not as evidence of a SQL injection or IDOR finding on its own \
(a raw "table doesn't exist" error is infrastructure-level either way) — but also don't spend \
more than one cycle re-diagnosing it from scratch; flag it and move to the next hypothesis.

If `url_structure_ground_truth` is present in # Scope, apply its `correct_pattern` BEFORE \
constructing a URL for ANY page name, including ones not explicitly listed in its note. This is \
not optional guidance to weigh against other reasoning — it is a hard routing fact about this \
target: a direct path like `/mutillidae/<page-name>.php` (the `wrong_pattern_example`) will \
always be rejected as out-of-scope and cost a full wasted cycle. Before you write ANY url_a, \
url_b, or target parameter for this application, check it against `correct_pattern` first. This \
has already cost multiple full retry-cycles across past sessions on this exact mistake — do not \
repeat it."""

# Per-category worked-evidence guidance. Each block gives the model a
# CONCRETE worked example of what counts as evidence and how to shape a
# diff_requests/httpx call for that vulnerability class — not just an
# abstract instruction to "test it."
#
# Why this exists as separate, scope-gated blocks rather than one giant
# always-on paragraph (the previous shape of this file): the old version
# had a full page of detailed IDOR worked examples (author param,
# view-someones-blog.php, user_id) hardcoded permanently into every
# prompt, and NOTHING equally concrete for any other category. Even after
# _identity_scope_line() was fixed to say "focus on sql_injection, don't
# pivot to IDOR" (session ~40), the bulk of the surrounding instructional
# text was still entirely IDOR-shaped — the one sentence of scope framing
# lost to a full page of IDOR-specific worked pattern-matching material.
# Observed result (session 45, resumed 2026-08-22): even with an explicit
# sql_injection/authentication scope and a working category-mismatch
# override blocking every IDOR dispatch attempt, the model kept
# re-deriving IDOR/user_id hypotheses cycle after cycle and never once
# produced a valid, complete diff_requests call for the SQLi test it was
# actually asked to run — because it had no equivalent worked template to
# imitate for THIS goal's category.
#
# Fix: give each category its own compact worked block, and only splice
# in the blocks relevant to the current goal's scope (matching how
# _identity_scope_line already limits WHICH categories are named). This
# keeps prompt length bounded to what's actually relevant instead of
# growing unboundedly as more categories get worked examples added, and
# stops feeding the model a rich template for a category it was just
# told not to pursue.
_CATEGORY_GUIDANCE = {
    "idor_bola": """
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
""",
    "sql_injection": """
Know what actually counts as SQL injection evidence before claiming a finding. For an \
AUTHENTICATION-BYPASS test on a login form: an HTTP 200 on the login page proves NOTHING by \
itself — the login page returns 200 whether the credentials are valid, invalid, or the payload \
is nonsense, since it's just re-rendering the same form. Real evidence is either (a) the response \
actually reflects a LOGGED-IN state — a redirect away from the login page, or content only a \
successfully authenticated session sees (e.g. a username/welcome message, a logout link) — or \
(b) a database error message leaking into the response (a MySQL syntax error, a stack trace \
naming a table/column) that reveals the raw input reached a query unsanitized. Two requests with \
the SAME status code and SAME rendered login form are a negative result, not "worth another \
payload variant" — vary the PAYLOAD SHAPE (comment sequences, quote/parenthesis balancing, \
UNION-based vs boolean-based vs stacked queries), not just cosmetic details of the same shape.

For a SEARCH/EXTRACTION test (e.g. user-info.php's username parameter returning more than one \
record, or fields it shouldn't): the signal is the response containing data for records the \
baseline single-user query would not return — extra rows, extra fields, or a boolean-based \
divergence where a TRUE-condition payload and a FALSE-condition payload for the SAME target \
value produce reliably different response lengths/content while an always-true and a \
known-true-value produce the same content. A single ambiguous length difference is not enough — \
confirm it's condition-driven by testing a matched true/false pair, not just any two payloads.

Shape every SQLi diff_requests call as a clean two-request A/B, not a vague description: url_a \
is the BASELINE (a known-valid, unmodified value — e.g. `user-info.php&username=admin`), url_b \
is the SAME url with ONLY the payload substituted into the vulnerable parameter (e.g. \
`user-info.php&username=admin' OR '1'='1`). Both url_a and url_b are REQUIRED fields — never emit \
a next_action for diff_requests without both filled in with a real, complete URL string; if you \
don't yet know a good baseline value, use httpx first to establish one rather than skipping \
straight to a diff_requests call missing url_a or url_b.

This goal explicitly excludes automated SQLi tooling (no sqlmap) — every payload here is your \
own hand-crafted variation via diff_requests/httpx, not a tool you delegate the injection to.
""",
}


def _category_guidance_block(scope_categories: list[str] | None) -> str:
    """Splice in worked-evidence guidance only for categories actually in
    scope (or all of them, in unscoped/universal mode) — see
    _CATEGORY_GUIDANCE docstring above for why this is gated at all."""
    if scope_categories:
        cats = [c for c in scope_categories if c in _CATEGORY_GUIDANCE]
    else:
        cats = list(_CATEGORY_GUIDANCE)
    return "".join(_CATEGORY_GUIDANCE[c] for c in cats)

# Backward-compatible module-level constant: the universal-mode (no explicit
# scope) rendering of the identity, for any caller/test that still imports
# SYSTEM_IDENTITY directly rather than going through build_prompt(). This is
# always the "no fixed vulnerability-class specialty" text, never the old
# hardcoded IDOR/BOLA-only framing.
SYSTEM_IDENTITY = SYSTEM_IDENTITY_TEMPLATE.format(
    identity_scope_line=_identity_scope_line(None),
    category_guidance=_category_guidance_block(None),
)

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
    {"observation": "...", "attack_strategy": "...", "confidence": 0.0, "rationale": "...",
     "category": "sql_injection|idor_bola|xss|ssrf|authentication|session_management|business_logic|csrf|mfa_bypass|..."}
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

Every hypothesis MUST include a "category" naming the vulnerability class it
tests for (e.g. "sql_injection", "idor_bola", "xss") — use the specific
category, not a generic word like "vulnerability" or "security issue". This
is how the agent tracks which vulnerability class each hypothesis actually
belongs to; it is independent of any category label the goal was matched to,
since one goal can legitimately spawn hypotheses in more than one category.

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


def summarize_recon_facts(request_history: list[dict], recon_tools: tuple[str, ...] = ("katana", "arjun")) -> str:
    """Extract the most recent result per (tool, target) pair for the given
    recon-type tools from request_history, as a compact fact list.

    This exists because request_history is already correctly captured and
    checkpointed (survives --resume-session), but was only ever surfaced
    to the model as one raw JSON dump under "# Working Memory" — up to 50
    entries, no synthesis, competing for attention with everything else
    in the prompt. Observed result (session 43, 2026-08-16): the model
    re-ran an identical `arjun` scan on the same endpoint twice, three
    cycles apart, ignoring that its own prior output said a re-run
    "will not find anything new" — the fact was technically present in
    Working Memory both times, just not in a form a 4B model reliably
    extracts and acts on. This produces the same fact pre-extracted, in
    the protected prompt tail near Available Tools/Target, the same fix
    pattern already applied to those two sections for the same reason.

    Only the most recent entry per (tool, target) is kept — not a full
    history — because what the model needs here is "what do I currently
    know", not a timeline; a full timeline is still available in Working
    Memory for anyone who needs it.
    """
    latest: dict[tuple[str, str], dict] = {}
    for entry in request_history:
        tool = entry.get("tool")
        if tool not in recon_tools:
            continue
        target = (entry.get("params") or {}).get("target")
        if not target:
            continue
        key = (tool, target)
        # request_history is append-ordered, so a later match always
        # supersedes an earlier one for the same (tool, target) pair.
        latest[key] = entry
    if not latest:
        return "(no recon-tool results recorded yet for this session)"
    lines = []
    for (tool, target), entry in latest.items():
        summary = (entry.get("summary") or "").strip()
        cycle = entry.get("cycle")
        lines.append(f"- {tool} on {target} (cycle {cycle}): {summary}")
    return "\n".join(lines)


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
    scope_categories: list[str] | None = None,
) -> list[dict]:
    relevant_playbooks = relevant_playbooks or []
    relevant_experiences = relevant_experiences or []
    goal_items = _split_goal_items(current_goal)
    system_identity = SYSTEM_IDENTITY_TEMPLATE.format(
        identity_scope_line=_identity_scope_line(scope_categories),
        category_guidance=_category_guidance_block(scope_categories),
    )
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
        f"# System Identity\n{system_identity}",
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
        f"# Resource Status\n{json.dumps(resource_status, indent=2)}",
        "# Known Recon Facts\n"
        "Pre-extracted from this session's recon-tool history (arjun, katana) — "
        "the most recent result per (tool, target) pair, so you don't have to "
        "mine the full Working Memory dump for it. If an endpoint you're "
        "considering already has an entry here, that recon has already been "
        "done — use the fact directly instead of re-running the same scan. "
        "Re-running an identical recon call that's already listed here wastes "
        "a full cycle for no new information.\n"
        f"{summarize_recon_facts(working_memory.get('request_history', []))}",
        # Available Tools, Target, and (if present) Correction are placed
        # LAST, immediately before Required Output Format, rather than
        # scattered earlier in the prompt. Three independent reasons
        # converge on the same fix: (1) Ollama's num_ctx truncation drops
        # from the FRONT of the prompt with no warning when the
        # accumulated Knowledge/Playbook/Hypotheses sections above push
        # the whole thing over the context window — content placed early
        # was the first casualty, silently, on exactly the cycles where
        # it mattered most (later cycles with more accumulated context).
        # (2) even well within the context window, instruction-following
        # in small models is generally most reliable for content nearest
        # the point of generation. (3) — added 2026-08-16, discovered the
        # hard way: when context_window was lowered from 8192 to 3072 to
        # fix VRAM spillover latency, Available Tools (previously safely
        # inside the old, much larger budget) started getting truncated
        # out on cycles with heavier Scope/Knowledge/Experience content.
        # The model, unable to see its real tool list, hallucinated
        # plausible-sounding tool names ('recon', 'con') that don't
        # exist, and every one of those cycles failed outright. Moving
        # Available Tools into this same protected tail — instead of
        # leaving it earlier and just hoping the budget holds — fixes
        # this at the structural level rather than requiring the context
        # window to always be generous enough to reach it.
        "# Available Tools\n"
        "Each tool lists its exact accepted param keys under \"params\". "
        "Only use keys listed there — inventing a param name means it gets "
        "silently ignored at execution time. Anything in \"defaults\" is "
        "already filled in if you omit it. This list is authoritative: if "
        "a tool name isn't in this list, it does not exist — do not invent "
        "one, abbreviate one, or guess at a plausible-sounding name.\n"
        f"{json.dumps(available_tools, indent=2)}",
        target_section,
    ]
    if correction:
        sections.append(f"# CORRECTION — READ THIS FIRST\n{correction}")
    sections.append(f"# Required Output Format\n{OUTPUT_FORMAT}")
    return [{"role": "system", "content": "\n\n".join(sections)}]