"""Unit tests for crawl report generation."""

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from crawler.bfs_crawler import CrawlStatistics
from crawler.report import CrawlReportGenerator


class CrawlReportGeneratorTests(unittest.TestCase):
    def test_generates_dashboard_json_and_professional_markdown(self) -> None:
        statistics = CrawlStatistics(
            pages_visited=2,
            pages_failed=1,
            skipped_visited_urls=3,
            links_discovered=8,
            links_enqueued=4,
            max_depth_reached=2,
            queue_size_remaining=0,
            duration_seconds=4.5,
            stop_reason="completed",
            duplicate_urls=2,
            external_urls=5,
            download_size_bytes=1_000,
            errors=("https://example.test/fail: timeout",),
            warnings=("robots.txt missing",),
        )
        with TemporaryDirectory() as temp_dir:
            json_path, markdown_path = CrawlReportGenerator().generate(
                output_directory=Path(temp_dir),
                start_url="https://example.test/start",
                statistics=statistics,
                visited_urls=("https://example.test/start", "https://docs.example.test/page"),
                configuration={"max_pages": 10, "max_depth": 2},
                categories={"web-security": 2},
            )

            report = json.loads(json_path.read_text(encoding="utf-8"))
            markdown = markdown_path.read_text(encoding="utf-8")

        self.assertEqual(report["metrics"]["total_pages"], 2)
        self.assertEqual(report["metrics"]["external_urls"], 5)
        self.assertEqual(report["metrics"]["average_page_size_bytes"], 500.0)
        self.assertEqual(report["report_type"], "crawl_report")
        self.assertEqual(report["run"]["status"], "completed")
        self.assertEqual(report["errors"], ["https://example.test/fail: timeout"])
        self.assertEqual(report["top_domains"][0]["name"], "example.test")
        self.assertIn("# Crawl Report", markdown)
        self.assertIn("## Crawler Configuration", markdown)
        self.assertIn("## Errors", markdown)
        self.assertIn("**Status:** completed", markdown)
        self.assertIn("1000 (1000 B)", markdown)
