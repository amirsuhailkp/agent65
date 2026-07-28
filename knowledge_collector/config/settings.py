"""Application settings for the Knowledge Collector Framework."""

from dataclasses import dataclass
import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True, slots=True)
class Settings:
    """Immutable runtime paths shared by framework components."""

    project_root: Path = PROJECT_ROOT
    raw_directory: Path = PROJECT_ROOT / "raw"
    processed_directory: Path = PROJECT_ROOT / "processed"
    logs_directory: Path = PROJECT_ROOT / "logs"
    log_level: str = "INFO"
    debug: bool = False
    ignore_robots: bool = False
    crawl_delay_seconds: float = 1.0


def _env_flag(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().casefold() in {"1", "true", "yes", "on"}


def _env_nonnegative_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        parsed = float(value)
    except ValueError as exc:
        raise ValueError(f"{name} must be a non-negative number") from exc
    if parsed < 0:
        raise ValueError(f"{name} must be a non-negative number")
    return parsed


settings = Settings(
    debug=_env_flag("DEBUG", default=False),
    ignore_robots=_env_flag("IGNORE_ROBOTS", default=False),
    crawl_delay_seconds=_env_nonnegative_float("CRAWL_DELAY_SECONDS", default=1.0),
)
