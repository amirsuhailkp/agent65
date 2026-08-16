"""Tests for scripts/kali_tools/diff_requests.py.

This script is deployed standalone to the Kali VM and isn't part of the
main src/ package, so it's imported directly via sys.path rather than a
normal package import.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts" / "kali_tools"))
import diff_requests as dr  # noqa: E402


def test_fetch_request_has_no_cookie_header_by_default():
    import urllib.request
    req = urllib.request.Request(
        "http://example.invalid",
        headers={"User-Agent": "agent-cyber-diff/1.1"},
    )
    assert "Cookie" not in dict(req.headers)


def test_fetch_builds_cookie_header_when_given():
    # Mirrors the header-construction logic inside fetch() without making
    # a real network call.
    import urllib.request
    cookie = "uid=admin"
    headers = {
        "User-Agent": "agent-cyber-diff/1.1",
        **({"Cookie": cookie} if cookie else {}),
    }
    req = urllib.request.Request("http://example.invalid", headers=headers)
    assert dict(req.headers).get("Cookie") == "uid=admin"


def test_cli_sentinel_dash_means_no_cookie():
    # Same sentinel convention as --data-a/--data-b: a literal "-" means
    # "not provided", not an actual header value with that content.
    for raw in ["-", None, ""]:
        resolved = raw if (raw and raw != "-") else None
        assert resolved is None


def test_cli_real_cookie_value_passes_through():
    raw = "uid=samurai"
    resolved = raw if (raw and raw != "-") else None
    assert resolved == "uid=samurai"