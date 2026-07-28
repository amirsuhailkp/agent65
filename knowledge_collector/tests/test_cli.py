"""Unit tests for command-line collection dispatch."""

from contextlib import redirect_stdout
import json
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import main
from crawler.bfs_crawler import CrawlStatistics


class CliTests(unittest.TestCase):
    @patch("main.OWASPCollector")
    def test_runs_single_page_collection_and_displays_path(self, collector_type: object) -> None:
        collector = collector_type.return_value
        collector.collect.return_value = Path("processed/article.md")
        output = StringIO()

        with redirect_stdout(output):
            saved_path = main.run_collection(
                "owasp",
                "https://owasp.org/www-project-top-ten/",
                language="en",
            )

        self.assertEqual(saved_path, Path("processed/article.md"))
        collector.collect.assert_called_once_with(
            "https://owasp.org/www-project-top-ten/",
            category="web-security",
            language="en",
        )
        self.assertIn("Progress:", output.getvalue())
        self.assertIn("Saved processed Markdown: processed\\article.md", output.getvalue())

    def test_parser_accepts_entire_site_command(self) -> None:
        arguments = main.build_parser().parse_args(
            [
                "site",
                "--source", "portswigger",
                "--url", "https://portswigger.net/web-security",
                "--max-pages", "25",
                "--max-depth", "3",
            ]
        )

        self.assertEqual(arguments.command, "site")
        self.assertEqual(arguments.max_pages, 25)
        self.assertEqual(arguments.max_depth, 3)

    @patch("main.Downloader")
    @patch("main.BFSCrawler")
    def test_site_crawl_saves_results_and_summary(self, crawler_type: object, downloader_type: object) -> None:
        crawler = crawler_type.return_value
        crawler.crawl.return_value = CrawlStatistics(
            pages_visited=2,
            pages_failed=0,
            skipped_visited_urls=0,
            links_discovered=1,
            links_enqueued=1,
            max_depth_reached=1,
            queue_size_remaining=0,
            duration_seconds=1.5,
            stop_reason="completed",
        )
        downloader_type.return_value.__enter__.return_value = object()

        with TemporaryDirectory() as temp_dir:
            results_path, summary_path, statistics = main.run_site_crawl(
                "portswigger",
                "https://portswigger.net/web-security",
                max_pages=10,
                max_depth=2,
                output_directory=Path(temp_dir),
            )

            self.assertTrue(results_path.is_file())
            self.assertTrue(summary_path.is_file())
            self.assertEqual(statistics.pages_visited, 2)
            self.assertEqual(json.loads(summary_path.read_text(encoding="utf-8"))["statistics"]["pages_visited"], 2)
            crawler.crawl.assert_called_once_with("https://portswigger.net/web-security", resume=False)

    def test_parser_accepts_single_page_command(self) -> None:
        arguments = main.build_parser().parse_args(
            ["collect", "--source", "portswigger", "--url", "https://portswigger.net/web-security"]
        )

        self.assertEqual(arguments.command, "collect")
        self.assertEqual(arguments.source, "portswigger")
