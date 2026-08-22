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
    command: str = ""
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

        started = time.monotonic()
        result = ExecutionResult(tool=tool_name, status="failed")
        try:
            # build_command() raises ValueError (missing required params) or
            # KeyError (template/param mismatch) — previously this call sat
            # OUTSIDE the try block entirely, so either exception propagated
            # all the way up through planner.run_cycle() and crashed the
            # whole process mid-cycle (observed: session 45 resumed, cycle 3,
            # diff_requests called with the wrong param names). A malformed
            # command from the model should degrade this ONE cycle to a
            # failed execution, exactly like an SSH failure does below —
            # never take down cycles that haven't run yet.
            try:
                command = self.registry.build_command(tool_name, params)
            except (ValueError, KeyError) as e:
                result.stderr = f"bad params for {tool_name}: {e}"
                log.error(f"BLOCKED: {tool_name} params rejected by registry: {e}")
                return result
            result.command = command
            log.info(f"Dispatching: {command} (timeout={spec.timeout}s)")

            try:
                client = self._connect()
            except (TimeoutError, OSError, paramiko.SSHException) as e:
                result.status = "connection_failed"
                result.stderr = str(e)
                log.error(
                    f"SSH connection to Kali VM ({self.host}:{self.port}) failed "
                    f"before dispatching {tool_name}: {e}"
                )
                return result

            stdin, stdout, stderr = client.exec_command(command, timeout=spec.timeout)
            # Some tools (httpx in particular) check whether stdin has
            # piped data and block reading it if so. Paramiko's exec_command
            # leaves the remote process's stdin open indefinitely unless we
            # explicitly close it — without this, non-interactive SSH looks
            # like "a pipe with data coming eventually" rather than "no
            # stdin input", so the tool hangs until spec.timeout instead of
            # running immediately. nuclei/nmap don't read stdin so they
            # never hit this; httpx does.
            stdin.close()
            out = stdout.read().decode(errors="replace")
            err = stderr.read().decode(errors="replace")
            exit_code = stdout.channel.recv_exit_status()
            result.stdout, result.stderr, result.exit_code = out, err, exit_code
            result.status = "completed" if exit_code == 0 else "failed"
            if exit_code != 0:
                # Previously silent: a nonzero exit skipped both except blocks
                # below, so "failed" cycles logged nothing explaining why.
                log.error(
                    f"{tool_name} exited with code {exit_code}: "
                    f"{(err or out).strip()[:500] or '(no stderr/stdout captured)'}"
                )
        except TimeoutError:
            result.status = "timed_out"
            log.error(f"{tool_name} timed out after {spec.timeout}s of no output")
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