"""Kali Dispatcher — Vol VII Ch3-4, Ch7. SSH-based execution against the Kali VM
(bridged adapter, key-based auth — matches your existing infra fix).
"""
from __future__ import annotations
import time
import datetime as dt
import paramiko
from dataclasses import dataclass, field
from ..tools.tool_registry import ToolRegistry, ToolSpec
from ..logging_setup import get_logger

log = get_logger("dispatcher.kali")


@dataclass
class ExecutionResult:
    tool: str
    status: str  # completed|failed|timed_out
    stdout: str = ""
    stderr: str = ""
    exit_code: int | None = None
    started_at: str = field(default_factory=lambda: dt.datetime.utcnow().isoformat())
    finished_at: str | None = None
    runtime_seconds: float | None = None


class KaliDispatcher:
    def __init__(self, host: str, port: int, user: str, key_path: str,
                 connect_timeout: int, registry: ToolRegistry):
        self.host = host
        self.port = port
        self.user = user
        self.key_path = key_path
        self.connect_timeout = connect_timeout
        self.registry = registry
        self._client: paramiko.SSHClient | None = None

    def _connect(self) -> paramiko.SSHClient:
        if self._client is not None:
            transport = self._client.get_transport()
            if transport and transport.is_active():
                return self._client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname=self.host, port=self.port, username=self.user,
            key_filename=self.key_path, timeout=self.connect_timeout,
        )
        self._client = client
        log.info(f"SSH connected to Kali VM at {self.host}:{self.port}")
        return client

    def execute(self, tool_name: str, params: dict, approved: bool = False) -> ExecutionResult:
        spec: ToolSpec | None = self.registry.get(tool_name)
        if not spec:
            return ExecutionResult(tool=tool_name, status="failed", stderr="unknown tool")

        if spec.risk_level == "high" and not approved:
            log.warning(f"BLOCKED: {tool_name} is high-risk and not approved")
            return ExecutionResult(tool=tool_name, status="failed",
                                    stderr="high-risk tool requires human approval")

        command = self.registry.build_command(tool_name, params)
        log.info(f"Dispatching: {command} (timeout={spec.timeout}s)")

        started = time.monotonic()
        result = ExecutionResult(tool=tool_name, status="failed")
        try:
            client = self._connect()
            stdin, stdout, stderr = client.exec_command(command, timeout=spec.timeout)
            out = stdout.read().decode(errors="replace")
            err = stderr.read().decode(errors="replace")
            exit_code = stdout.channel.recv_exit_status()
            result.stdout, result.stderr, result.exit_code = out, err, exit_code
            result.status = "completed" if exit_code == 0 else "failed"
        except TimeoutError:
            result.status = "timed_out"
            log.error(f"{tool_name} timed out after {spec.timeout}s")
        except Exception as e:
            result.status = "failed"
            result.stderr = str(e)
            log.error(f"{tool_name} execution error: {e}")
        finally:
            result.finished_at = dt.datetime.utcnow().isoformat()
            result.runtime_seconds = round(time.monotonic() - started, 2)

        return result

    def close(self):
        if self._client:
            self._client.close()
            self._client = None
