"""Unit tests for single-page PortSwigger collection orchestration."""

from pathlib import Path
import unittest
from unittest.mock import MagicMock

from collectors.portswigger import PortSwiggerCollector
from models.document import DownloadedDocument


class PortSwiggerCollectorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.downloader = MagicMock()
        self.extractor = MagicMock()
        self.converter = MagicMock()
        self.cleaner = MagicMock()
        self.metadata = MagicMock()
        self.storage = MagicMock()
        self.collector = PortSwiggerCollector(
            downloader=self.downloader,
            extractor=self.extractor,
            markdown_converter=self.converter,
            cleaner=self.cleaner,
            metadata_generator=self.metadata,
            storage=self.storage,
        )

    def test_collects_one_portswigger_page_with_shared_pipeline(self) -> None:
        url = "https://portswigger.net/web-security/sql-injection"
        final_path = Path("processed/portswigger-sqli.md")
        self.downloader.download_document.return_value = DownloadedDocument(
            html="<html>raw</html>", requested_url=url, final_url=url, status_code=200, redirect_history=()
        )
        self.extractor.extract.return_value = "<article>article</article>"
        self.converter.convert.return_value = "# SQL injection"
        self.cleaner.clean.return_value = "# SQL injection\n"
        self.metadata.generate.return_value = "---\ntitle: SQL injection\n---\n"
        self.storage.save_processed.return_value = final_path

        result = self.collector.collect(url, language="en")

        self.assertEqual(result, final_path)
        self.downloader.download_document.assert_called_once_with(url)
        self.metadata.generate.assert_called_once_with(
            "# SQL injection\n",
            url=url,
            collector="portswigger",
            category="web-security",
            language="en",
        )
        self.storage.save_raw.assert_called_once()
        self.storage.save_processed.assert_called_once()

    def test_rejects_non_portswigger_urls_without_downloading(self) -> None:
        with self.assertRaises(ValueError):
            self.collector.collect("https://owasp.org/www-project-top-ten/")

        self.downloader.download.assert_not_called()

    def test_discovery_remains_empty_until_crawling_is_introduced(self) -> None:
        self.assertEqual(tuple(self.collector.discover()), ())
