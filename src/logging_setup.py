"""Logging — Vol VI Ch13. Planner decisions, tool execution, resource usage, errors, verification."""
from __future__ import annotations
import logging
import logging.handlers
from pathlib import Path
from .config import load_config, resolve_path

_CONFIGURED = False


def setup_logging() -> logging.Logger:
    global _CONFIGURED
    cfg = load_config()["logging"]
    log_dir = resolve_path(cfg["log_dir"])
    log_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("agent_cyber")
    if _CONFIGURED:
        return logger

    logger.setLevel(cfg.get("level", "INFO"))
    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )

    file_handler = logging.handlers.RotatingFileHandler(
        log_dir / "agent_cyber.log",
        maxBytes=cfg.get("rotate_mb", 20) * 1024 * 1024,
        backupCount=cfg.get("retain_files", 10),
    )
    file_handler.setFormatter(fmt)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(fmt)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    _CONFIGURED = True
    return logger


def get_logger(name: str) -> logging.Logger:
    setup_logging()
    return logging.getLogger(f"agent_cyber.{name}")
