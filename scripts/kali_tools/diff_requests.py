#!/usr/bin/env python3
"""diff_requests — fetch two requests and diff the result.

Deploy this to the Kali VM at /home/kali/agent_tools/diff_requests.py
(overwrite the existing file), then it's invoked by the agent as a
registered tool: two requests, one comparison, one structured JSON
result — the actual thing a pentester does by hand when checking for
IDOR (request as user A's ID, request as user B's ID, compare), instead
of leaving that comparison to be reconstructed from two separate
tool-call summaries several cycles apart.

Supports both GET (query-string identifiers) and POST (form-body
identifiers, e.g. Mutillidae's view-someones-blog.php `author` field).
Which one to use depends on the target endpoint — check recon output
before assuming GET.

Also supports diffing the SAME url_a/url_b under two different Cookie
header values (--cookie-a/--cookie-b) — the correct way to test whether
a cookie value (e.g. a `uid` cookie) controls access/identity, as opposed
to putting the cookie value in --data-a/--data-b, which sends it as a
POST form field instead of an actual Cookie header and tests something
different.

Usage:
    python3 diff_requests.py <url_a> <url_b> [--method GET|POST]
                              [--data-a FORM_BODY] [--data-b FORM_BODY]
                              [--cookie-a COOKIE] [--cookie-b COOKIE]
                              [--timeout SECONDS]

Examples:
    # GET-based IDOR (identifier in the query string)
    python3 diff_requests.py \\
        'http://target/item.php?id=1' 'http://target/item.php?id=2'

    # POST-based IDOR (identifier in a form field)
    python3 diff_requests.py \\
        'http://target/view-someones-blog.php' 'http://target/view-someones-blog.php' \\
        --method POST \\
        --data-a 'author=admin&view-someones-blog-php-submit-button=View+Blog+Entries' \\
        --data-b 'author=john&view-someones-blog-php-submit-button=View+Blog+Entries'

    # Cookie-based auth bypass (same protected URL, different uid cookie)
    python3 diff_requests.py \\
        'http://target/index.php?page=admin' 'http://target/index.php?page=admin' \\
        --cookie-a 'uid=admin' --cookie-b 'uid=samurai'

Exit codes:
    0 — both requests completed (regardless of what the diff shows)
    1 — one or both requests failed (connection error, timeout, etc.)

Uses only the standard library (urllib) — no extra pip installs needed
on the Kali VM.
"""
import sys
import json
import argparse
import urllib.request
import urllib.error
import difflib
import re


def strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def fetch(url: str, timeout: float, method: str = "GET", data: str | None = None,
          cookie: str | None = None) -> dict:
    """Fetch a single URL. For POST, `data` is a raw
    application/x-www-form-urlencoded body string, e.g.
    'author=admin&submit=View'. `cookie`, if given, is the raw Cookie
    header value, e.g. 'uid=admin' or 'PHPSESSID=deadbeef1234' — sent
    for either GET or POST, unlike `data` which only applies to POST."""
    body_bytes = data.encode() if (method == "POST" and data) else None
    headers = {
        "User-Agent": "agent-cyber-diff/1.1",
        **({"Content-Type": "application/x-www-form-urlencoded"} if body_bytes else {}),
        **({"Cookie": cookie} if cookie else {}),
    }
    req = urllib.request.Request(url, data=body_bytes, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode(errors="replace")
            return {
                "url": url,
                "ok": True,
                "status_code": resp.status,
                "content_length": len(body),
                "body": body,
                "body_excerpt": strip_html(body)[:500],
            }
    except urllib.error.HTTPError as e:
        # An HTTP error status (403, 404, 500...) is still a completed
        # request with a real, comparable response — not a failure.
        body = e.read().decode(errors="replace") if e.fp else ""
        return {
            "url": url,
            "ok": True,
            "status_code": e.code,
            "content_length": len(body),
            "body": body,
            "body_excerpt": strip_html(body)[:500],
        }
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        return {"url": url, "ok": False, "error": str(e)}


def diff_result(a: dict, b: dict) -> dict:
    if not a["ok"] or not b["ok"]:
        return {
            "comparable": False,
            "reason": f"request_a_ok={a['ok']} request_b_ok={b['ok']}",
        }

    status_match = a["status_code"] == b["status_code"]
    length_delta = a["content_length"] - b["content_length"]

    body_a_lines = a["body"].splitlines()
    body_b_lines = b["body"].splitlines()
    ratio = difflib.SequenceMatcher(None, a["body"], b["body"]).quick_ratio()

    # A short unified diff excerpt — enough for the model to see WHAT
    # differs (e.g. a username or record ID embedded in the page) without
    # dumping two full HTML bodies into the prompt.
    diff_lines = list(difflib.unified_diff(
        body_a_lines, body_b_lines, lineterm="", n=1,
    ))[:20]

    return {
        "comparable": True,
        "status_match": status_match,
        "status_a": a["status_code"],
        "status_b": b["status_code"],
        "content_length_delta": length_delta,
        "body_similarity_ratio": round(ratio, 3),
        # Heuristic, not a verdict: same status + ANY body difference is
        # the IDOR-suggestive pattern. A similarity-ratio cutoff was tried
        # first but gets skewed by shared template boilerplate (nav bars,
        # footers) common to real pages — two genuinely different users'
        # content can still score >0.9 similar if 90% of the page is
        # identical chrome around a small content block. Presence of any
        # diff at matching status is the actual signal; this still isn't
        # proof by itself and needs human/impact-assessor judgment.
        "idor_suggestive": status_match and bool(diff_lines),
        "diff_excerpt": diff_lines or ["(bodies identical)"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url_a")
    parser.add_argument("url_b")
    parser.add_argument("--method", choices=["GET", "POST"], default="GET",
                         help="HTTP method for BOTH requests (default: GET)")
    parser.add_argument("--data-a", default=None,
                         help="POST body for url_a, e.g. 'author=admin&submit=View' (ignored for GET)")
    parser.add_argument("--data-b", default=None,
                         help="POST body for url_b, e.g. 'author=john&submit=View' (ignored for GET)")
    parser.add_argument("--cookie-a", default=None,
                         help="Cookie header value for request A, e.g. 'uid=admin' (applies to GET or POST; '-' means none)")
    parser.add_argument("--cookie-b", default=None,
                         help="Cookie header value for request B, e.g. 'uid=samurai' (applies to GET or POST; '-' means none)")
    parser.add_argument("--timeout", type=float, default=15.0)
    args = parser.parse_args()

    data_a = args.data_a if args.method == "POST" else None
    data_b = args.data_b if args.method == "POST" else None
    # '-' is the registered tool's no-op sentinel (same convention as
    # data_a/data_b) — treat it as "no cookie", not a literal header value.
    cookie_a = args.cookie_a if (args.cookie_a and args.cookie_a != "-") else None
    cookie_b = args.cookie_b if (args.cookie_b and args.cookie_b != "-") else None

    a = fetch(args.url_a, args.timeout, args.method, data_a, cookie_a)
    b = fetch(args.url_b, args.timeout, args.method, data_b, cookie_b)
    result = {
        "request_a": {k: v for k, v in a.items() if k != "body"},
        "request_b": {k: v for k, v in b.items() if k != "body"},
        "diff": diff_result(a, b),
    }
    print(json.dumps(result))
    sys.exit(0 if (a["ok"] and b["ok"]) else 1)


if __name__ == "__main__":
    main()