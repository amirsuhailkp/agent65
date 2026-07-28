"""Tests for the adapter that joins crawl traversal to page collection."""

from pathlib import Path
import unittest
from unittest.mock import MagicMock

from crawler.page_processor import WorkflowCrawlPageProcessor
from workflow.collection_workflow import CollectionResult


class WorkflowCrawlPageProcessorTests(unittest.TestCase):
    def test_runs_the_collection_workflow_and_exposes_discovery_data(self) -> None:
        workflow = MagicMock()
        workflow.run.return_value = CollectionResult(
            raw_path=Path("raw/page.html"),
            processed_path=Path("processed/page.md"),
            final_url="https://example.test/final",
            raw_html='<a href="/next">Next</a>',
            extraction_size_bytes=42,
        )
        processor = WorkflowCrawlPageProcessor(
            workflow,
            collector="example",
            category="web-security",
            language="en",
        )

        page = processor.process("https://example.test/page")

        workflow.run.assert_called_once()
        self.assertEqual(page.final_url, "https://example.test/final")
        self.assertEqual(page.discovery_html, '<a href="/next">Next</a>')
        self.assertEqual(page.extraction_size_bytes, 42)
