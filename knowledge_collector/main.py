"""Command-line interface for knowledge collection.

Every enabled source declared in ``config/sources.yaml`` is available here
automatically -- adding a new source never requires touching this file.

Examples:
    python main.py collect --source owasp --url https://owasp.org/www-project-top-ten/
    python main.py site --source portswigger --url https://portswigger.net/research --max-pages 0
    python main.py
"""

import argparse
import json
import logging
import os
import sys
from collections.abc import Sequence
from dataclasses import asdict
from pathlib import Path
from typing import Literal
from urllib.parse import urlsplit

from collectors.owasp import OWASPCollector
from collectors.portswigger import PortSwiggerCollector
from config.settings import settings
from config.sources import SourceConfig, SourceConfigError, SourceRegistry
from crawler.bfs_crawler import BFSCrawler, CrawlStatistics
from crawler.dedup import ContentHashStore
from crawler.incremental import PageMetadataStore
from crawler.page_processor import ClassifyingCrawlPageProcessor
from crawler.report import CrawlReportGenerator
from crawler.visited import VisitedURLDatabase
from downloader.downloader import Downloader
from logger import configure_logging
from utils.artifact_names import build_artifact_filenames
from workflow.collection_workflow import create_default_collection_workflow


logger = logging.getLogger("knowledge_collector.cli")

# `OWASPCollector` / `PortSwiggerCollector` stay wired directly for these two
# historical sources (referenced by name, at call time, in run_collection) so
# existing integrations and tests keep working unchanged. Every other source
# -- including new ones added purely through sources.yaml -- goes through the
# generic, configuration-driven path.

# A large, effectively-unbounded depth used only when the caller asked for
# unlimited pages (max_pages=0) and did not pin an explicit max_depth. See
# item 6 of the architecture upgrade: "crawl depth should become optional".
_EFFECTIVELY_UNLIMITED_DEPTH = 1_000_000


def _load_registry() -> SourceRegistry:
    try:
        return SourceRegistry.load()
    except SourceConfigError as exc:
        print(f"Error: invalid source configuration: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc


_REGISTRY = _load_registry()
SOURCE_CHOICES: tuple[str, ...] = _REGISTRY.enabled_names()


def build_parser() -> argparse.ArgumentParser:
    """Build the non-interactive command-line parser."""

    parser = argparse.ArgumentParser(
        description="Collect and process cybersecurity knowledge from configured sources.",
    )
    subcommands = parser.add_subparsers(dest="command")

    collect = subcommands.add_parser("collect", help="Collect one source page.")
    collect.add_argument("--source", choices=SOURCE_CHOICES, required=True)
    collect.add_argument("--url", required=True, help="Absolute URL for the selected source.")
    collect.add_argument("--category", default=None, help="Metadata category (defaults to the source's configured category).")
    collect.add_argument("--language", default="unknown", help="Metadata language code.")

    site = subcommands.add_parser("site", help="Crawl an entire source site.")
    _add_crawl_arguments(site)

    resume = subcommands.add_parser("resume", help="Resume an interrupted site crawl.")
    _add_crawl_arguments(resume)

    return parser


def run_collection(
    source: str,
    url: str,
    *,
    category: str | None = None,
    language: str = "unknown",
) -> Path:
    """Run one source's collector for a single URL and display its saved path."""

    config = _resolve_source_config(source)
    resolved_category = category or config.category
    print(f"Progress: starting single-page {config.display_name} collection...")
    logger.info("CLI requested %s collection for %s", source, url)

    if source == "owasp":
        collector = OWASPCollector()
        saved_path = collector.collect(url, category=resolved_category, language=language)
    elif source == "portswigger":
        collector = PortSwiggerCollector()
        saved_path = collector.collect(url, category=resolved_category, language=language)
    else:
        _validate_source_url(config, url)
        raw_filename, processed_filename = build_artifact_filenames(source, url)
        with Downloader() as downloader:
            workflow = create_default_collection_workflow(downloader=downloader)
            result = workflow.run(
                url=url,
                collector=source,
                category=resolved_category,
                language=language,
                raw_filename=raw_filename,
                processed_filename=processed_filename,
                subdirectory=config.slug,
            )
        saved_path = result.processed_path

    print(f"Saved processed Markdown: {saved_path}")
    return saved_path


def run_site_crawl(
    source: str,
    start_url: str,
    *,
    max_pages: int,
    max_depth: int | None = None,
    resume: bool = False,
    output_directory: Path | None = None,
    category: str | None = None,
    language: str = "unknown",
) -> tuple[Path, Path, CrawlStatistics]:
    """Crawl a source site and save its discovered URLs, summary, and reports."""

    config = _resolve_source_config(source)
    _validate_source_url(config, start_url)
    if max_pages < 0:
        raise ValueError("max_pages cannot be negative (use 0 for unlimited)")

    if max_depth is None:
        max_depth = config.max_depth
        if max_pages == 0:
            # Unlimited pages implies depth should not be the limiting factor
            # either, unless the caller pins one explicitly.
            max_depth = _EFFECTIVELY_UNLIMITED_DEPTH
    if max_depth < 0:
        raise ValueError("max_depth cannot be negative")

    resolved_category = category or config.category
    crawl_directory = output_directory or settings.logs_directory / "crawls" / _crawl_id(source, start_url)
    crawl_directory.mkdir(parents=True, exist_ok=True)
    visited = VisitedURLDatabase(crawl_directory / "visited_urls.json")
    print(f"Progress: starting site crawl for {start_url}")
    logger.info(
        "CLI requested site crawl source=%s url=%s max_pages=%s max_depth=%s resume=%s",
        source,
        start_url,
        max_pages,
        max_depth,
        resume,
    )

    with Downloader() as downloader:
        workflow = create_default_collection_workflow(downloader=downloader)
        page_processor = ClassifyingCrawlPageProcessor(
            workflow,
            downloader=downloader,
            collector=source,
            category=resolved_category,
            language=language,
            hash_store=ContentHashStore(),
            subdirectory=config.slug,
        )
        crawler = BFSCrawler(
            downloader,
            page_processor=page_processor,
            visited=visited,
            max_pages=max_pages,
            max_depth=max_depth,
            checkpoint_path=crawl_directory / "crawl_checkpoint.json",
        )
        statistics = crawler.crawl(start_url, resume=resume)

    results_path = crawl_directory / "crawl_results.json"
    summary_path = crawl_directory / "crawl_summary.json"
    statistics_path = crawl_directory / "crawl_statistics.json"
    failed_urls_path = crawl_directory / "failed_urls.json"
    skipped_urls_path = crawl_directory / "skipped_urls.json"

    _save_json(
        results_path,
        {
            "source": source,
            "start_url": start_url,
            "visited_urls": visited.urls,
        },
    )
    _save_json(
        summary_path,
        {
            "source": source,
            "start_url": start_url,
            "max_pages": max_pages,
            "max_depth": max_depth,
            "statistics": asdict(statistics),
        },
    )
    _save_json(statistics_path, asdict(statistics))
    _save_json(
        failed_urls_path,
        {"count": len(statistics.errors), "errors": list(statistics.errors)},
    )
    _save_json(
        skipped_urls_path,
        {
            "count": len(page_processor.skipped_urls),
            "skipped": [
                {"url": url, "reason": reason} for url, reason in page_processor.skipped_urls
            ],
        },
    )
    report_json_path, report_markdown_path = CrawlReportGenerator().generate(
        output_directory=crawl_directory,
        start_url=start_url,
        statistics=statistics,
        visited_urls=visited.urls,
        configuration={
            "source": source,
            "collector_type": config.collector_type,
            "max_pages": max_pages,
            "max_depth": max_depth,
            "ignore_robots": settings.ignore_robots,
            "crawl_delay_seconds": settings.crawl_delay_seconds,
            "resume": resume,
        },
        categories={resolved_category: statistics.pages_visited},
    )
    print(f"Saved crawl results: {results_path}")
    print(f"Saved crawl summary: {summary_path}")
    print(f"Saved crawl statistics: {statistics_path}")
    print(f"Saved failed URLs: {failed_urls_path}")
    print(f"Saved skipped URLs: {skipped_urls_path}")
    print(f"Saved crawl report: {report_json_path} and {report_markdown_path}")
    return results_path, summary_path, statistics


def _resolve_source_config(source: str) -> SourceConfig:
    try:
        return _REGISTRY.get(source)
    except KeyError as exc:
        raise ValueError(str(exc)) from exc


def _validate_source_url(config: SourceConfig, url: str) -> None:
    """Reject a URL that does not belong to this source's configured domain(s)."""

    allowed_hostnames = config.allowed_hostnames()
    hostname = (urlsplit(url).hostname or "").casefold().removeprefix("www.")
    if not hostname or not any(
        hostname == root or hostname.endswith(f".{root}") for root in allowed_hostnames
    ):
        raise ValueError(
            f"{url} is not part of the configured domain(s) for {config.display_name}: "
            f"{sorted(allowed_hostnames)}"
        )


def _add_crawl_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--source", choices=SOURCE_CHOICES, required=True)
    parser.add_argument("--url", required=True, help="Starting URL for the crawl.")
    parser.add_argument(
        "--max-pages",
        type=int,
        default=100,
        help="Maximum pages to crawl (default: 100). Use 0 for unlimited.",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=None,
        help="Maximum crawl depth (defaults to the source's configured depth; "
        "ignored in favor of an effectively unlimited depth when --max-pages 0 is used).",
    )
    parser.add_argument("--category", default=None, help="Metadata category (defaults to the source's configured category).")
    parser.add_argument("--language", default="unknown", help="Metadata language code.")


def _crawl_id(source: str, start_url: str) -> str:
    host = urlsplit(start_url).hostname or "site"
    return f"{source}-{host.casefold().replace('.', '-')}"


def _save_json(path: Path, payload: object) -> None:
    """Atomically persist a crawl artifact without overwriting a partial file."""

    temporary_path = path.with_suffix(f"{path.suffix}.tmp")
    with temporary_path.open("w", encoding="utf-8", newline="\n") as output:
        json.dump(payload, output, ensure_ascii=False, indent=2)
        output.flush()
        os.fsync(output.fileno())
    temporary_path.replace(path)


def _interactive_arguments() -> argparse.Namespace | None:
    """Prompt for source and collection mode when no command is supplied."""

    print("Knowledge Collector")
    for index, name in enumerate(SOURCE_CHOICES, start=1):
        print(f"{index}. {_REGISTRY.get(name).display_name}")
    source_choice = input("Choose source: ").strip()
    source_map = {str(index): name for index, name in enumerate(SOURCE_CHOICES, start=1)}
    source = source_map.get(source_choice)
    if source is None:
        print(f"Error: choose a number between 1 and {len(SOURCE_CHOICES)}.", file=sys.stderr)
        return None

    print("1. Single URL")
    print("2. Entire Site")
    print("3. Resume Crawl")
    mode = input("Choose collection mode: ").strip()
    if mode == "1":
        url = input("Enter URL: ").strip()
        return argparse.Namespace(
            command="collect",
            source=source,
            url=url,
            category=None,
            language="unknown",
        )
    if mode == "2":
        return _interactive_crawl_arguments("site", source)
    if mode == "3":
        return _interactive_crawl_arguments("resume", source)

    print("Error: choose 1, 2, or 3.", file=sys.stderr)
    return None


def _interactive_crawl_arguments(command: Literal["site", "resume"], source: str) -> argparse.Namespace:
    url = input("Enter starting URL: ").strip()
    max_pages = int(input("Enter maximum pages (0 = unlimited) [100]: ").strip() or "100")
    max_depth_raw = input("Enter maximum crawl depth [source default]: ").strip()
    return argparse.Namespace(
        command=command,
        source=source,
        url=url,
        max_pages=max_pages,
        max_depth=int(max_depth_raw) if max_depth_raw else None,
        category=None,
        language="unknown",
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Execute the CLI and return a process-compatible status code."""

    configure_logging(settings.logs_directory, settings.log_level)
    parser = build_parser()
    try:
        arguments = parser.parse_args(argv)
        if arguments.command is None:
            arguments = _interactive_arguments()
            if arguments is None:
                return 2

        if arguments.command in {"site", "resume"}:
            run_site_crawl(
                arguments.source,
                arguments.url,
                max_pages=arguments.max_pages,
                max_depth=arguments.max_depth,
                resume=arguments.command == "resume",
                category=arguments.category,
                language=arguments.language,
            )
            return 0

        run_collection(
            arguments.source,
            arguments.url,
            category=arguments.category,
            language=arguments.language,
        )
    except KeyboardInterrupt:
        print("\nCollection cancelled.", file=sys.stderr)
        return 130
    except (EOFError, ValueError) as exc:
        logger.error("Invalid collection request: %s", exc)
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:
        logger.exception("Collection failed")
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
