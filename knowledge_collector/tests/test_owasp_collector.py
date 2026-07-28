"""Unit tests for single-page OWASP collection orchestration."""

from pathlib import Path
import unittest
from unittest.mock import MagicMock

from collectors.owasp import OWASPCollector
from models.document import DownloadedDocument


class OWASPCollectorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.downloader = MagicMock()
        self.extractor = MagicMock()
        self.converter = MagicMock()
        self.cleaner = MagicMock()
        self.metadata = MagicMock()
        self.storage = MagicMock()
        self.collector = OWASPCollector(
            downloader=self.downloader,
            extractor=self.extractor,
            markdown_converter=self.converter,
            cleaner=self.cleaner,
            metadata_generator=self.metadata,
            storage=self.storage,
        )

    def test_collects_one_page_through_all_pipeline_stages(self) -> None:
        url = "https://owasp.org/www-project-top-ten/"
        final_path = Path("processed/owasp-top-ten.md")
        self.downloader.download_document.return_value = DownloadedDocument(
            html="<html>raw</html>", requested_url=url, final_url=url, status_code=200, redirect_history=()
        )
        self.extractor.extract.return_value = "<article>article</article>"
        self.converter.convert.return_value = "# Article"
        self.cleaner.clean.return_value = "# Article\n"
        self.metadata.generate.return_value = "---\ntitle: Article\n---\n\n# Article\n"
        self.storage.save_processed.return_value = final_path

        result = self.collector.collect(url, language="en")

        self.assertEqual(result, final_path)
        self.downloader.download_document.assert_called_once_with(url)
        self.extractor.extract.assert_called_once_with("<html>raw</html>")
        self.converter.convert.assert_called_once_with("<article>article</article>")
        self.cleaner.clean.assert_called_once_with("# Article")
        self.metadata.generate.assert_called_once_with(
            "# Article\n",
            url=url,
            collector="owasp",
            category="web-security",
            language="en",
        )
        self.storage.save_raw.assert_called_once()
        self.storage.save_processed.assert_called_once()

    def test_rejects_non_owasp_urls_without_downloading(self) -> None:
        with self.assertRaises(ValueError):
            self.collector.collect("https://example.com/article")

        self.downloader.download.assert_not_called()

    def test_discovery_is_empty_to_prevent_crawling(self) -> None:
        self.assertEqual(tuple(self.collector.discover()), ())
