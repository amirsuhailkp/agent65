from unittest.mock import MagicMock, patch

from src.dispatcher.kali_dispatcher import KaliDispatcher
from src.tools.tool_registry import ToolRegistry

REGISTRY_PATH = "config/tools_registry.yaml"


def _dispatcher():
    registry = ToolRegistry(REGISTRY_PATH)
    return KaliDispatcher(
        host="192.168.56.105", port=22, user="kali", key_path="/dev/null",
        connect_timeout=5, registry=registry,
    )


def test_execute_missing_required_params_returns_failed_not_raises():
    """Regression test for the actual crash (session 45 resumed, cycle 3):
    diff_requests was called with params={'url': ...} instead of the
    required 'url_a'/'url_b'. ToolRegistry.build_command() raised a bare
    ValueError that previously sat OUTSIDE any try/except in execute(),
    propagating all the way up through planner.run_cycle() and killing the
    whole process. It must now degrade to a single failed ExecutionResult."""
    d = _dispatcher()
    result = d.execute(tool_name="diff_requests", params={"url": "http://x/y"})
    assert result.status == "failed"
    assert "url_a" in result.stderr or "url_b" in result.stderr
    d.close()


def test_execute_missing_params_never_attempts_ssh_connect():
    """A bad-params failure should be caught before even trying to reach
    the Kali VM — no point paying an SSH connect timeout for a command
    that was never going to build."""
    d = _dispatcher()
    with patch.object(d, "_connect") as mock_connect:
        d.execute(tool_name="diff_requests", params={"url": "http://x/y"})
        mock_connect.assert_not_called()
    d.close()


def test_execute_unknown_tool_returns_failed_not_raises():
    d = _dispatcher()
    result = d.execute(tool_name="totally_invented_tool", params={})
    assert result.status == "failed"
    assert "unknown tool" in result.stderr
    d.close()


def test_execute_valid_params_reaches_ssh_layer():
    """Sanity check the fix didn't break the happy path — valid params
    for a real tool should still get as far as attempting to dispatch."""
    d = _dispatcher()
    with patch.object(d, "_connect") as mock_connect:
        client = MagicMock()
        stdin, stdout, stderr = MagicMock(), MagicMock(), MagicMock()
        stdout.read.return_value = b"ok"
        stderr.read.return_value = b""
        stdout.channel.recv_exit_status.return_value = 0
        client.exec_command.return_value = (stdin, stdout, stderr)
        mock_connect.return_value = client

        result = d.execute(
            tool_name="diff_requests",
            params={"url_a": "http://x/a", "url_b": "http://x/b"},
        )
        assert result.status == "completed"
        assert result.command  # a real command string was built
    d.close()
