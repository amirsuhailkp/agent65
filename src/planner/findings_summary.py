"""Compact, high-signal summaries of tool output for request_history.

Previously request_history only carried {tool, status, cycle} — the next
cycle's LLM call had no idea *what* a tool actually found, only that it
ran and passed/failed. That starved the model of the one thing it needs
to make a better decision next cycle: real findings, or a real reason a
scan came back empty.

Keyed off the registry's output_schema.format so this stays tool-agnostic
where possible, with light tool-specific parsing for the two formats
(nuclei jsonl, nmap xml) where the generic dump is too noisy to be useful
in a prompt.
"""
from __future__ import annotations
import json
import re

MAX_SUMMARY_CHARS = 600


def summarize(tool_name: str, output_format: str | None, exec_result) -> str:
    """exec_result needs .status, .stdout, .stderr — matches ExecResult."""
    if exec_result.status != "completed":
        # Failure path: the *reason* matters more than any partial output.
        # This is exactly what was missing when nuclei was silently hitting
        # "no matches found" from an unquoted glob — the next cycle just
        # saw status=failed and guessed blindly instead of adapting.
        err = (exec_result.stderr or exec_result.stdout or "").strip()
        err = re.sub(r"\s+", " ", err)[:MAX_SUMMARY_CHARS]
        return f"FAILED ({exec_result.status}): {err or 'no error output captured'}"

    stdout = exec_result.stdout or ""

    if tool_name == "nuclei" or output_format == "json_lines_nuclei":
        return _summarize_nuclei(stdout)
    if tool_name == "nmap" or output_format == "xml":
        return _summarize_nmap(stdout)
    if tool_name == "httpx":
        return _summarize_httpx(stdout)
    if output_format == "json_lines":
        return _summarize_json_lines(stdout)
    if output_format == "json":
        return _summarize_json(stdout)

    text = re.sub(r"\s+", " ", stdout.strip())
    return text[:MAX_SUMMARY_CHARS] if text else "(completed, no output captured)"


def _summarize_nuclei(stdout: str) -> str:
    matches = []
    for line in stdout.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except ValueError:
            continue
        tid = obj.get("template-id", "?")
        sev = (obj.get("info") or {}).get("severity", "?")
        at = obj.get("matched-at") or obj.get("host") or "?"
        matches.append(f"[{sev}] {tid} @ {at}")
    if not matches:
        return "0 matches found"
    shown = matches[:10]
    suffix = f" (+{len(matches) - 10} more)" if len(matches) > 10 else ""
    return f"{len(matches)} matches: " + "; ".join(shown) + suffix


def _strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _summarize_httpx(stdout: str) -> str:
    # -irr adds response headers+body to httpx's JSON output. Confirmed
    # against real httpx output: status_code, content_length, content_type
    # are top-level int/str fields. The response body's exact key under
    # -irr wasn't confirmed against real output (docs describe the flag's
    # effect, not the literal schema) — checking a few plausible names
    # rather than betting on one. If this cycle's summary looks wrong,
    # check the raw evidence blob for the actual key and this needs a
    # one-line fix.
    lines = [l for l in stdout.strip().splitlines() if l.strip()]
    if not lines:
        return "(no output captured)"
    parts = []
    for line in lines[:5]:
        try:
            obj = json.loads(line)
        except ValueError:
            continue
        status = obj.get("status_code", "?")
        clen = obj.get("content_length", "?")
        body_raw = (
            obj.get("response") or obj.get("body") or obj.get("raw_response")
            or obj.get("response_body") or ""
        )
        body_excerpt = _strip_html(str(body_raw))[:300] if body_raw else "(no body field found)"
        parts.append(f"[{status}] content_length={clen} body: {body_excerpt}")
    return " | ".join(parts) if parts else "(completed, output not valid JSON)"


def _summarize_nmap(stdout: str) -> str:
    # nmap -oX - output. Cheap regex scrape instead of full XML parsing —
    # good enough for "open ports + service/version" which is all the
    # planner needs to reason about next steps. Each <port> block is
    # extracted whole first, then name/product/version pulled out of it
    # independently (rather than one combined regex) so attribute order
    # inside <service .../> doesn't matter and none of them get swallowed
    # by an adjacent greedy match.
    blocks = re.findall(r'<port protocol="(\w+)" portid="(\d+)">(.*?)</port>', stdout, re.S)
    open_ports = []
    for proto, port, body in blocks:
        if 'state="open"' not in body:
            continue
        name = re.search(r'<service[^>]*\bname="([^"]*)"', body)
        product = re.search(r'<service[^>]*\bproduct="([^"]*)"', body)
        version = re.search(r'<service[^>]*\bversion="([^"]*)"', body)
        svc = name.group(1) if name else "unknown"
        if product:
            svc += f" ({product.group(1)}{' ' + version.group(1) if version else ''})"
        open_ports.append(f"{port}/{proto} {svc}")
    if not open_ports:
        return "0 open ports found (or output unparseable)"
    shown = open_ports[:20]
    suffix = f" (+{len(open_ports) - 20} more)" if len(open_ports) > 20 else ""
    return f"{len(open_ports)} open ports: " + "; ".join(shown) + suffix


def _summarize_json_lines(stdout: str) -> str:
    count = sum(1 for line in stdout.strip().splitlines() if line.strip())
    text = re.sub(r"\s+", " ", stdout.strip())[:MAX_SUMMARY_CHARS]
    return f"{count} lines: {text}"


def _summarize_json(stdout: str) -> str:
    try:
        obj = json.loads(stdout)
    except ValueError:
        text = re.sub(r"\s+", " ", stdout.strip())
        return text[:MAX_SUMMARY_CHARS] if text else "(completed, no output captured)"
    if isinstance(obj, list):
        return f"{len(obj)} results: " + json.dumps(obj[:5])[:MAX_SUMMARY_CHARS]
    return json.dumps(obj)[:MAX_SUMMARY_CHARS]