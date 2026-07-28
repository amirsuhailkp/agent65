"""Tool Registry — Vol II Ch13, Vol VII Ch5.

Planner discovers/selects tools through this registry, never by
hard-coding shell commands.
"""
from __future__ import annotations
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
        stops the model from inventing param names that don't exist."""
        return [
            {
                "name": t.name,
                "category": t.category,
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
        missing = [k for k in spec.input_schema if k not in merged or merged[k] in (None, "")]
        if missing:
            raise ValueError(f"Missing params for {name}: {missing}")
        return spec.command_template.format(**merged)
