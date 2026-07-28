"""Central logging configuration."""

import logging
from pathlib import Path


def configure_logging(log_directory: Path, level: str = "INFO") -> None:
    """Configure framework logging without adding duplicate handlers."""

    log_directory.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("knowledge_collector")
    logger.setLevel(level)
    logger.propagate = False

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        file_handler = logging.FileHandler(log_directory / "knowledge_collector.log", encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    progress_logger = logging.getLogger("knowledge_collector.crawl_progress")
    progress_logger.setLevel(level)
    progress_logger.propagate = False
    crawl_log = log_directory / "crawl.log"
    if not any(
        isinstance(handler, logging.FileHandler)
        and Path(handler.baseFilename) == crawl_log.resolve()
        for handler in progress_logger.handlers
    ):
        crawl_handler = logging.FileHandler(crawl_log, encoding="utf-8")
        crawl_handler.setFormatter(formatter)
        progress_logger.addHandler(crawl_handler)
