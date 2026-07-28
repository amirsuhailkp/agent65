"""Unit tests for source-independent collection workflow composition."""

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import MagicMock

from models.document import DownloadedDocument
from extractor.html_extractor import SuspiciousExtractionError
from workflow.collection_workflow import CollectionWorkflow


class CollectionWorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.downloader = MagicMock()
        self.extractor = MagicMock()
        self.renderer = MagicMock()
        self.cleaner = MagicMock()
        self.metadata = MagicMock()
        self.storage = MagicMock()
        self.workflow = CollectionWorkflow(
            downloader=self.downloader,
            extractor=self.extractor,
            markdown_renderer=self.renderer,
            markdown_cleaner=self.cleaner,
            metadata_generator=self.metadata,
            storage=self.storage,
        )

    def test_runs_all_stages_and_returns_both_saved_paths(self) -> None:
        self.downloader.download_document.return_value = DownloadedDocument(
            html="<html>raw</html>",
            requested_url="https://example.test/content",
            final_url="https://example.test/final-content",
            status_code=200,
            redirect_history=(),
        )
        self.extractor.extract.return_value = "<article>content</article>"
        self.renderer.convert.return_value = "# Content"
        self.cleaner.clean.return_value = "# Content\n"
        self.metadata.generate.return_value = "---\ntitle: Content\n---\n\n# Content\n"
        self.storage.save_raw.return_value = Path("raw/content.html")
        self.storage.save_processed.return_value = Path("processed/content.md")

        result = self.workflow.run(
            url="https://example.test/content",
            collector="example",
            category="web-security",
            language="en",
            raw_filename="content.html",
            processed_filename="content.md",
        )

        self.assertEqual(result.raw_path, Path("raw/content.html"))
        self.assertEqual(result.processed_path, Path("processed/content.md"))
        self.assertEqual(result.final_url, "https://example.test/final-content")
        self.assertEqual(result.raw_html, "<html>raw</html>")
        self.assertEqual(result.extraction_size_bytes, len("<article>content</article>".encode("utf-8")))
        self.downloader.download_document.assert_called_once_with("https://example.test/content")
        self.extractor.extract.assert_called_once_with("<html>raw</html>")
        self.renderer.convert.assert_called_once_with("<article>content</article>")
        self.cleaner.clean.assert_called_once_with("# Content")
        self.metadata.generate.assert_called_once_with(
            "# Content\n",
            url="https://example.test/final-content",
            collector="example",
            category="web-security",
            language="en",
        )
        self.storage.save_raw.assert_called_once_with("<html>raw</html>", "content.html")
        self.storage.save_processed.assert_called_once_with(
            "---\ntitle: Content\n---\n\n# Content\n", "content.md"
        )

    def test_debug_mode_saves_diagnostics_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            logs_dir = Path(temp_dir)
            workflow = CollectionWorkflow(
                downloader=self.downloader,
                extractor=self.extractor,
                markdown_renderer=self.renderer,
                markdown_cleaner=self.cleaner,
                metadata_generator=self.metadata,
                storage=self.storage,
                debug=True,
                logs_directory=logs_dir,
            )

            self.downloader.download_document.return_value = DownloadedDocument(
                html="<html>raw</html>",
                requested_url="https://example.test/content",
                final_url="https://example.test/final-content",
                status_code=200,
                redirect_history=(),
                headers={"Content-Type": "text/html; charset=utf-8"},
                content_type="text/html; charset=utf-8",
                encoding="utf-8",
            )
            self.extractor.extract.return_value = "<article>content</article>"
            self.renderer.convert.return_value = "# Content"
            self.cleaner.clean.return_value = "# Content\n"
            self.metadata.generate.return_value = (
                "---\n"
                "title: Content\n"
                "source: example.test\n"
                "url: https://example.test/final-content\n"
                "collector: example\n"
                "category: web-security\n"
                "tags:\n"
                "- content\n"
                "date_collected: 2026-01-01T00:00:00Z\n"
                "language: en\n"
                "---\n\n"
                "# Content\n"
            )
            self.storage.save_raw.return_value = Path("raw/content.html")
            self.storage.save_processed.return_value = Path("processed/content.md")

            workflow.run(
                url="https://example.test/content",
                collector="example",
                category="web-security",
                language="en",
                raw_filename="content.html",
                processed_filename="content.md",
            )

            self.assertTrue((logs_dir / "raw_response.html").exists())
            self.assertTrue((logs_dir / "cleaned_article.html").exists())
            self.assertTrue((logs_dir / "extracted_markdown.md").exists())
            self.assertTrue((logs_dir / "metadata.json").exists())
            self.assertTrue((logs_dir / "redirect_history.json").exists())
            self.assertTrue((logs_dir / "download_headers.json").exists())

            metadata = json.loads((logs_dir / "metadata.json").read_text(encoding="utf-8"))
            self.assertEqual(metadata.get("title"), "Content")

    def test_debug_mode_false_does_not_save_diagnostics_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            logs_dir = Path(temp_dir)
            workflow = CollectionWorkflow(
                downloader=self.downloader,
                extractor=self.extractor,
                markdown_renderer=self.renderer,
                markdown_cleaner=self.cleaner,
                metadata_generator=self.metadata,
                storage=self.storage,
                debug=False,
                logs_directory=logs_dir,
            )

            self.downloader.download_document.return_value = DownloadedDocument(
                html="<html>raw</html>",
                requested_url="https://example.test/content",
                final_url="https://example.test/final-content",
                status_code=200,
                redirect_history=(),
            )
            self.extractor.extract.return_value = "<article>content</article>"
            self.renderer.convert.return_value = "# Content"
            self.cleaner.clean.return_value = "# Content\n"
            self.metadata.generate.return_value = "---\ntitle: Content\n---\n\n# Content\n"
            self.storage.save_raw.return_value = Path("raw/content.html")
            self.storage.save_processed.return_value = Path("processed/content.md")

            workflow.run(
                url="https://example.test/content",
                collector="example",
                category="web-security",
                language="en",
                raw_filename="content.html",
                processed_filename="content.md",
            )

            self.assertFalse((logs_dir / "raw_response.html").exists())
            self.assertFalse((logs_dir / "cleaned_article.html").exists())
            self.assertFalse((logs_dir / "extracted_markdown.md").exists())
            self.assertFalse((logs_dir / "metadata.json").exists())
            self.assertFalse((logs_dir / "redirect_history.json").exists())
            self.assertFalse((logs_dir / "download_headers.json").exists())

    def test_uses_playwright_fallback_when_initial_extraction_is_suspicious(self) -> None:
        browser_renderer = MagicMock()
        workflow = CollectionWorkflow(
            downloader=self.downloader,
            extractor=self.extractor,
            browser_renderer=browser_renderer,
            markdown_renderer=self.renderer,
            markdown_cleaner=self.cleaner,
            metadata_generator=self.metadata,
            storage=self.storage,
        )

        self.downloader.download_document.return_value = DownloadedDocument(
            html="<html>placeholder</html>",
            requested_url="https://example.test/content",
            final_url="https://example.test/final-content",
            status_code=200,
            redirect_history=(),
        )
        self.extractor.extract.side_effect = [
            SuspiciousExtractionError("too small"),
            "<article>rendered content</article>",
        ]
        browser_renderer.render.return_value = "<html><article>rendered</article></html>"
        self.renderer.convert.return_value = "# Rendered"
        self.cleaner.clean.return_value = "# Rendered\n"
        self.metadata.generate.return_value = "---\ntitle: Rendered\n---\n\n# Rendered\n"
        self.storage.save_raw.return_value = Path("raw/content.html")
        self.storage.save_processed.return_value = Path("processed/content.md")

        result = workflow.run(
            url="https://example.test/content",
            collector="example",
            category="web-security",
            language="en",
            raw_filename="content.html",
            processed_filename="content.md",
        )

        self.assertEqual(result.processed_path, Path("processed/content.md"))
        browser_renderer.render.assert_called_once_with("https://example.test/final-content")
        self.assertEqual(self.extractor.extract.call_count, 2)
        self.extractor.extract.assert_any_call("<html>placeholder</html>")
        self.extractor.extract.assert_any_call("<html><article>rendered</article></html>")

    def test_does_not_use_playwright_when_initial_extraction_succeeds(self) -> None:
        browser_renderer = MagicMock()
        workflow = CollectionWorkflow(
            downloader=self.downloader,
            extractor=self.extractor,
            browser_renderer=browser_renderer,
            markdown_renderer=self.renderer,
            markdown_cleaner=self.cleaner,
            metadata_generator=self.metadata,
            storage=self.storage,
        )

        self.downloader.download_document.return_value = DownloadedDocument(
            html="<html>raw</html>",
            requested_url="https://example.test/content",
            final_url="https://example.test/final-content",
            status_code=200,
            redirect_history=(),
        )
        self.extractor.extract.return_value = "<article>content</article>"
        self.renderer.convert.return_value = "# Content"
        self.cleaner.clean.return_value = "# Content\n"
        self.metadata.generate.return_value = "---\ntitle: Content\n---\n\n# Content\n"
        self.storage.save_raw.return_value = Path("raw/content.html")
        self.storage.save_processed.return_value = Path("processed/content.md")

        workflow.run(
            url="https://example.test/content",
            collector="example",
            category="web-security",
            language="en",
            raw_filename="content.html",
            processed_filename="content.md",
        )

        browser_renderer.render.assert_not_called()

    def test_raises_original_error_when_playwright_fallback_is_disabled(self) -> None:
        workflow = CollectionWorkflow(
            downloader=self.downloader,
            extractor=self.extractor,
            browser_renderer=None,
            markdown_renderer=self.renderer,
            markdown_cleaner=self.cleaner,
            metadata_generator=self.metadata,
            storage=self.storage,
        )

        self.downloader.download_document.return_value = DownloadedDocument(
            html="<html>placeholder</html>",
            requested_url="https://example.test/content",
            final_url="https://example.test/final-content",
            status_code=200,
            redirect_history=(),
        )
        self.extractor.extract.side_effect = SuspiciousExtractionError("too small")

        with self.assertRaises(SuspiciousExtractionError):
            workflow.run(
                url="https://example.test/content",
                collector="example",
                category="web-security",
                language="en",
                raw_filename="content.html",
                processed_filename="content.md",
            )
