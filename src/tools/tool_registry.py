"""Tool Registry — Vol II Ch13, Vol VII Ch5.

Planner discovers/selects tools through this registry, never by
hard-coding shell commands.
"""
from __future__ import annotations
import shlex
import yaml
from dataclasses import dataclass


@dataclass
class ToolSpec:
    name: str
    category: str
    version: str
    command_template: str
    input_schema: dict
    output_schema: dict
    risk_level: str
    timeout: int
    dependencies: list
    default_params: dict
    description: str = ""


class ToolRegistry:
    def __init__(self, registry_path: str):
        with open(registry_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        self._tools = {
            t["name"]: ToolSpec(
                name=t["name"], category=t["category"], version=t["version"],
                command_template=t["command_template"], input_schema=t["input_schema"],
                output_schema=t["output_schema"], risk_level=t["risk_level"],
                timeout=t["timeout"], dependencies=t.get("dependencies", []),
                default_params=t.get("default_params", {}),
                description=t.get("description", ""),
            )
            for t in data.get("tools", [])
        }

    def get(self, name: str) -> ToolSpec | None:
        return self._tools.get(name)

    def list_names(self) -> list[str]:
        return list(self._tools.keys())

    def by_category(self, category: str) -> list[ToolSpec]:
        return [t for t in self._tools.values() if t.category == category]

    def schema_summary(self) -> list[dict]:
        """Compact per-tool schema for the reasoning prompt — this is what
        stops the model from inventing param names that don't exist.

        `description` matters most for tools the model has no pretrained
        familiarity with (anything custom to this codebase, like
        diff_requests) — nuclei/httpx/nmap it can reason about from prior
        knowledge even with a thin schema, but a genuinely new tool with
        no explanation of purpose is invisible to it in practice, not
        just under-preferred."""
        return [
            {
                "name": t.name,
                "category": t.category,
                "description": t.description,
                "params": t.input_schema,
                "defaults": t.default_params,
                "risk_level": t.risk_level,
            }
            for t in self._tools.values()
        ]

    def build_command(self, name: str, params: dict) -> str:
        spec = self.get(name)
        if not spec:
            raise KeyError(f"Unknown tool: {name}")
        # Registry-level defaults fill in anything the planner didn't supply
        # (e.g. nuclei's severity) before checking for genuinely missing input.
        merged = {**spec.default_params, **params}
        missing = [k for k in spec.input_schema if k not in merged or merged[k] is None]
        if missing:
            raise ValueError(f"Missing params for {name}: {missing}")
        # Quote every value before interpolating into the template. Without
        # this, an unquoted target like "...?page=foo.php" hits the remote
        # shell (zsh on Kali, nomatch on by default) as an unmatched glob
        # and aborts with "no matches found" before the tool even runs.
        quoted = {k: shlex.quote(str(v)) for k, v in merged.items()}
        return spec.command_template.format(**quoted)