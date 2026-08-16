import pytest
from pathlib import Path
from src.tools.tool_registry import ToolRegistry

REGISTRY_PATH = Path(__file__).parent.parent / "config" / "tools_registry.yaml"


def test_nuclei_severity_default_fills_missing_param():
    registry = ToolRegistry(str(REGISTRY_PATH))
    # Only target supplied — severity must come from default_params, not crash
    cmd = registry.build_command("nuclei", {"target": "example.com"})
    assert "example.com" in cmd
    assert "-severity" in cmd
    assert "medium" in cmd


def test_explicit_param_overrides_default():
    registry = ToolRegistry(str(REGISTRY_PATH))
    cmd = registry.build_command("nuclei", {"target": "example.com", "severity": "critical"})
    assert "critical" in cmd
    assert "medium,high,critical" not in cmd


def test_nuclei_tags_default_fills_missing_param():
    registry = ToolRegistry(str(REGISTRY_PATH))
    cmd = registry.build_command("nuclei", {"target": "example.com"})
    assert "-tags" in cmd
    assert "auth" in cmd


def test_schema_summary_exposes_real_param_keys():
    registry = ToolRegistry(str(REGISTRY_PATH))
    summary = registry.schema_summary()
    nuclei = next(t for t in summary if t["name"] == "nuclei")
    assert set(nuclei["params"].keys()) == {"target", "severity", "tags"}
    assert "severity" in nuclei["defaults"]


def test_missing_required_param_still_raises():
    registry = ToolRegistry(str(REGISTRY_PATH))
    with pytest.raises(ValueError):
        registry.build_command("httpx", {})  # no target, no default for it


def test_httpx_header_defaults_to_harmless_noop():
    registry = ToolRegistry(str(REGISTRY_PATH))
    cmd = registry.build_command("httpx", {"target": "example.com"})
    assert "-H" in cmd
    assert "X-Agent-Probe: 1" in cmd


def test_httpx_header_supports_cookie_manipulation():
    # This is the actual mechanism that was missing when a hypothesis
    # tried to test a named cookie (e.g. session_auth_ground_truth's
    # "uid") — previously there was no way to set a Cookie header at
    # all, so cookie values got wrongly sent as POST body data instead.
    registry = ToolRegistry(str(REGISTRY_PATH))
    cmd = registry.build_command(
        "httpx",
        {"target": "example.com", "header": "Cookie: uid=admin"},
    )
    assert "Cookie: uid=admin" in cmd
    assert "-H" in cmd