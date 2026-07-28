"""Central configuration loader. Vol VI Ch6 — config lives outside source code."""
from __future__ import annotations
import yaml
from pathlib import Path
from functools import lru_cache

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = ROOT / "config" / "config.yaml"
DEFAULT_SCOPE_PATH = ROOT / "config" / "scope.yaml"


@lru_cache(maxsize=1)
def load_config(path: Path = DEFAULT_CONFIG_PATH) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@lru_cache(maxsize=1)
def load_scope(path: Path = DEFAULT_SCOPE_PATH) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def resolve_path(relative: str) -> Path:
    p = Path(relative)
    return p if p.is_absolute() else ROOT / p
