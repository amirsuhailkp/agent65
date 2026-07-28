"""Dashboard-ready crawl report generation."""

from __future__ import annotations

import json
import os
from collections import Counter
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlsplit

from .bfs_crawler import CrawlStatistics


class CrawlReportGenerator:
    """Create machine-readable and human-readable reports for a completed crawl."""

    def generate(
        self,
        *,
        output_directory: Path,
        start_url: str,
        statistics: CrawlStatistics,
        visited_urls: tuple[str, ...],
        configuration: dict[str, object],
        categories: dict[str, int] | None = None,
    ) -> tuple[Path, Path]:
        """Write ``crawl_report.json`` and ``crawl_report.md`` atomically."""

        output_directory.mkdir(parents=True, exist_ok=True)
        domains = Counter(
            host for url in visited_urls if (host := urlsplit(url).hostname) is not None
        )
        report = {
            "schema_version": 1,
            "report_type": "crawl_report",
            "generated_at": datetime.now(UTC).isoformat(),
            "start_url": start_url,
            "run": {
                "status": _run_status(statistics),
                "stop_reason": statistics.stop_reason,
                "max_depth_reached": statistics.max_depth_reached,
                "queue_size_remaining": statistics.queue_size_remaining,
            },
            "metrics": {
                "total_pages": statistics.pages_visited,
                "failed_pages": statistics.pages_failed,
                "skipped_pages": statistics.skipped_visited_urls,
                "duplicate_urls": statistics.duplicate_urls,
                "external_urls": statistics.external_urls,
                "download_size_bytes": statistics.download_size_bytes,
                "processing_time_seconds": statistics.duration_seconds,
                "average_page_size_bytes": _average(
                    statistics.download_size_bytes, statistics.pages_visited
                ),
                "average_extraction_size_bytes": _average(
                    statistics.extraction_size_bytes, statistics.pages_visited
                ),
                "average_extraction_size_status": (
                    "collected" if statistics.extraction_collected else "not_collected"
                ),
            },
            "top_domains": _top_counts(domains),
            "top_categories": _top_counts(Counter(categories or {})),
            "crawler_configuration": configuration,
            "statistics": asdict(statistics),
            "errors": list(statistics.errors),
            "warnings": list(statistics.warnings),
        }
        json_path = output_directory / "crawl_report.json"
        markdown_path = output_directory / "crawl_report.md"
        _save_json(json_path, report)
        _save_text(markdown_path, _render_markdown(report))
        return json_path, markdown_path


def _average(total: int, count: int) -> float:
    return round(total / count, 2) if count else 0.0


def _top_counts(counts: Counter[str]) -> list[dict[str, int | str]]:
    return [{"name": name, "count": count} for name, count in counts.most_common(10)]


def _render_markdown(report: dict[str, object]) -> str:
    metrics = report["metrics"]
    assert isinstance(metrics, dict)
    lines = [
        "# Crawl Report",
        "",
        f"- **Generated:** {report['generated_at']}",
        f"- **Start URL:** {report['start_url']}",
        f"- **Status:** {_markdown_value(report['run'], 'status')}",
        f"- **Stop reason:** {_markdown_value(report['run'], 'stop_reason')}",
        "",
        "## Metrics",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
    ]
    labels = {
        "total_pages": "Total pages",
        "failed_pages": "Failed pages",
        "skipped_pages": "Skipped pages",
        "duplicate_urls": "Duplicate URLs",
        "external_urls": "External URLs",
        "download_size_bytes": "Download size (bytes)",
        "processing_time_seconds": "Processing time (seconds)",
        "average_page_size_bytes": "Average page size (bytes)",
        "average_extraction_size_bytes": "Average extraction size (bytes)",
    }
    lines.extend(
        f"| {label} | {_format_metric(key, metrics[key])} |"
        for key, label in labels.items()
    )
    lines.append(
        "| Average extraction size status | "
        f"{metrics['average_extraction_size_status']} |"
    )
    lines.extend(_render_counts("Top Domains", report["top_domains"]))
    lines.extend(_render_counts("Top Categories", report["top_categories"]))
    lines.extend(_render_configuration(report["crawler_configuration"]))
    lines.extend(_render_messages("Errors", report["errors"]))
    lines.extend(_render_messages("Warnings", report["warnings"]))
    return "\n".join(lines) + "\n"


def _render_counts(title: str, entries: object) -> list[str]:
    lines = ["", f"## {title}", ""]
    if not entries:
        return [*lines, "None recorded."]
    lines.extend(f"- {entry['name']}: {entry['count']}" for entry in entries if isinstance(entry, dict))
    return lines


def _render_messages(title: str, messages: object) -> list[str]:
    lines = ["", f"## {title}", ""]
    if not messages:
        return [*lines, "None recorded."]
    lines.extend(f"- {message}" for message in messages)
    return lines


def _render_configuration(configuration: object) -> list[str]:
    lines = ["", "## Crawler Configuration", ""]
    if not isinstance(configuration, dict) or not configuration:
        return [*lines, "None recorded."]
    lines.extend(f"- **{key}:** {value}" for key, value in configuration.items())
    return lines


def _run_status(statistics: CrawlStatistics) -> str:
    """Return a stable, dashboard-friendly outcome for this crawl invocation."""

    if statistics.stop_reason == "completed":
        return "completed"
    if statistics.stop_reason in {"max_pages", "max_runtime"}:
        return "partial"
    return "stopped"


def _markdown_value(value: object, key: str) -> object:
    return value.get(key, "unknown") if isinstance(value, dict) else "unknown"


def _format_metric(key: str, value: object) -> str:
    if key in {"download_size_bytes", "average_page_size_bytes", "average_extraction_size_bytes"}:
        return f"{value} ({_format_bytes(value)})"
    if key == "processing_time_seconds":
        return f"{value} ({_format_duration(value)})"
    return str(value)


def _format_bytes(value: object) -> str:
    if not isinstance(value, (int, float)):
        return "unknown"
    units = ("B", "KiB", "MiB", "GiB", "TiB")
    size = float(value)
    for unit in units:
        if abs(size) < 1024 or unit == units[-1]:
            return f"{size:.2f} {unit}" if unit != "B" else f"{int(size)} {unit}"
        size /= 1024
    return "unknown"


def _format_duration(value: object) -> str:
    if not isinstance(value, (int, float)):
        return "unknown"
    total_seconds = max(0, int(round(value)))
    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:d}:{minutes:02d}:{seconds:02d}" if hours else f"{minutes:d}:{seconds:02d}"


def _save_json(path: Path, payload: object) -> None:
    _save_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def _save_text(path: Path, content: str) -> None:
    temporary_path = path.with_suffix(f"{path.suffix}.tmp")
    with temporary_path.open("w", encoding="utf-8", newline="\n") as report_file:
        report_file.write(content)
        report_file.flush()
        os.fsync(report_file.fileno())
    temporary_path.replace(path)
