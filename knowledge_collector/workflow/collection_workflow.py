"""Composable URL-to-Markdown collection workflow."""

import json
import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import yaml

from config.settings import settings
from cleaner.markdown_cleaner import MarkdownCleaner as DefaultMarkdownCleaner
from downloader.downloader import Downloader
from extractor.html_extractor import SuspiciousExtractionError
from extractor.html_extractor import HTMLExtractor
from extractor.markdown_converter import MarkdownConverter
from extractor.playwright_renderer import BrowserRenderError
from extractor.playwright_renderer import PlaywrightRenderer
from extractor.playwright_renderer import is_playwright_available
from metadata.metadata_generator import MetadataGenerator as DefaultMetadataGenerator
from storage.filesystem import FilesystemStorage as DefaultFilesystemStorage
from models.document import DownloadedDocument


logger = logging.getLogger("knowledge_collector.workflow")


class HtmlDownloader(Protocol):
    """HTTP retrieval boundary."""

    def download_document(self, url: str) -> DownloadedDocument:
        """Return raw HTML and the final URL after redirects."""


class HtmlExtractor(Protocol):
    """Main-content HTML extraction boundary."""

    def extract(self, raw_html: str) -> str:
        """Return article HTML from raw HTML."""


class BrowserRenderer(Protocol):
    """Optional JavaScript-rendered HTML fallback boundary."""

    def render(self, url: str) -> str:
        """Return browser-rendered HTML for the given URL."""


class MarkdownRenderer(Protocol):
    """HTML-to-Markdown conversion boundary."""

    def convert(self, cleaned_html: str) -> str:
        """Return Markdown from article HTML."""


class MarkdownCleaner(Protocol):
    """Markdown normalization boundary."""

    def clean(self, markdown: str) -> str:
        """Return cleaned Markdown."""


class MetadataGenerator(Protocol):
    """YAML front-matter generation boundary."""

    def generate(
        self,
        markdown: str,
        *,
        url: str,
        collector: str,
        category: str,
        language: str,
    ) -> str:
        """Return Markdown prefixed with source metadata."""


class ArtifactStorage(Protocol):
    """Raw and processed artifact persistence boundary."""

    def save_raw(self, content: str, filename: str) -> Path:
        """Persist raw content and return its path."""

    def save_processed(self, content: str, filename: str) -> Path:
        """Persist processed content and return its path."""


@dataclass(frozen=True, slots=True)
class CollectionResult:
    """Artifacts and crawl-relevant facts produced by one page collection."""

    raw_path: Path
    processed_path: Path
    final_url: str
    raw_html: str
    extraction_size_bytes: int


class CollectionWorkflow:
    """Execute the source-agnostic URL-to-Markdown processing pipeline.

    The workflow depends only on narrow behavioral contracts, allowing any stage
    to be substituted without changing collectors or adjacent stages.
    """

    def __init__(
        self,
        *,
        downloader: HtmlDownloader,
        extractor: HtmlExtractor,
        markdown_renderer: MarkdownRenderer,
        markdown_cleaner: MarkdownCleaner,
        metadata_generator: MetadataGenerator,
        storage: ArtifactStorage,
        browser_renderer: BrowserRenderer | None = None,
        debug: bool | None = None,
        logs_directory: Path | None = None,
    ) -> None:
        self._downloader = downloader
        self._extractor = extractor
        self._markdown_renderer = markdown_renderer
        self._markdown_cleaner = markdown_cleaner
        self._metadata_generator = metadata_generator
        self._storage = storage
        self._browser_renderer = browser_renderer
        self._debug = settings.debug if debug is None else debug
        self._logs_directory = logs_directory or settings.logs_directory

    def run(
        self,
        *,
        url: str,
        collector: str,
        category: str,
        language: str,
        raw_filename: str,
        processed_filename: str,
        downloaded_document: DownloadedDocument | None = None,
        subdirectory: str | None = None,
    ) -> CollectionResult:
        """Process one URL and persist both raw HTML and final Markdown.

        Args:
            downloaded_document: Optional pre-fetched document. Callers that
                must inspect raw HTML before deciding how to process it (see
                ``crawler.page_processor.ClassifyingCrawlPageProcessor``) pass
                this to avoid a redundant second download.
            subdirectory: Optional per-source folder (e.g. a source slug)
                under ``raw/`` and ``processed/``. Omitted by default to
                preserve the historical flat layout.
        """

        logger.info("Workflow started (collector=%s, url=%s)", collector, url)
        download_result = downloaded_document or self._downloader.download_document(url)
        raw_html = download_result.html
        article_html, extraction_method = self._extract_with_optional_browser_fallback(download_result, raw_html)
        logger.info("Extraction succeeded using %s", extraction_method)
        markdown = self._markdown_renderer.convert(article_html)
        clean_markdown = self._markdown_cleaner.clean(markdown)
        document = self._metadata_generator.generate(
            clean_markdown,
            url=download_result.final_url,
            collector=collector,
            category=category,
            language=language,
        )
        if self._debug:
            self._log_debug_diagnostics(download_result, raw_html, article_html, markdown, clean_markdown)
            self._save_debug_artifacts(download_result, raw_html, article_html, markdown, document)
        if subdirectory:
            raw_path = self._storage.save_raw(raw_html, raw_filename, subdirectory=subdirectory)
            processed_path = self._storage.save_processed(document, processed_filename, subdirectory=subdirectory)
        else:
            raw_path = self._storage.save_raw(raw_html, raw_filename)
            processed_path = self._storage.save_processed(document, processed_filename)
        logger.info(
            "Workflow completed (raw=%s, processed=%s)", raw_path, processed_path
        )
        return CollectionResult(
            raw_path=raw_path,
            processed_path=processed_path,
            final_url=download_result.final_url,
            raw_html=raw_html,
            extraction_size_bytes=len(article_html.encode("utf-8")),
        )
    def _extract_with_optional_browser_fallback(
        self,
        download_result: DownloadedDocument,
        raw_html: str,
    ) -> tuple[str, str]:
        try:
            article_html = self._extractor.extract(raw_html)
            return article_html, "requests HTML"
        except SuspiciousExtractionError as initial_error:
            logger.warning(
                "Initial extraction from requests HTML was suspiciously small; "
                "attempting Playwright fallback: %s",
                initial_error.reason,
            )
            if self._browser_renderer is None:
                logger.info("Playwright fallback is disabled; raising original extraction error")
                raise

            render_url = getattr(download_result, "final_url", None) or getattr(download_result, "requested_url", None)
            if not render_url:
                logger.info("No URL available for Playwright fallback; raising original extraction error")
                raise

            try:
                rendered_html = self._browser_renderer.render(render_url)
            except BrowserRenderError as exc:
                logger.warning("Playwright fallback failed for %s: %s", render_url, exc)
                raise initial_error from exc

            article_html = self._extractor.extract(rendered_html)
            return article_html, "Playwright-rendered HTML fallback"

    def _log_debug_diagnostics(
        self,
        download_result: DownloadedDocument,
        raw_html: str,
        article_html: str,
        markdown: str,
        clean_markdown: str,
    ) -> None:
        html_size = len(raw_html)
        article_size = len(article_html)
        markdown_size = len(markdown)
        cleaned_size = len(clean_markdown)
        extraction_ratio = article_size / html_size if html_size else 0.0
        cleaning_ratio = cleaned_size / markdown_size if markdown_size else 0.0

        headers = download_result.headers or {}
        content_type = download_result.content_type or headers.get("Content-Type")
        encoding = download_result.encoding or "unknown"
        redirect_history = download_result.redirect_history

        logger.info("DEBUG response headers: %s", headers)
        logger.info("DEBUG content type: %s", content_type or "unknown")
        logger.info("DEBUG encoding: %s", encoding)
        logger.info(
            "DEBUG redirect chain: %s",
            [f"{hop.mechanism}:{hop.source_url}->{hop.destination_url}" for hop in redirect_history],
        )
        logger.info(
            "DEBUG extraction statistics: html_chars=%s article_chars=%s extraction_ratio=%.4f",
            html_size,
            article_size,
            extraction_ratio,
        )
        logger.info("DEBUG markdown size: markdown_chars=%s", markdown_size)
        logger.info(
            "DEBUG cleaning statistics: markdown_chars=%s cleaned_chars=%s cleaning_ratio=%.4f",
            markdown_size,
            cleaned_size,
            cleaning_ratio,
        )

    def _save_debug_artifacts(
        self,
        download_result: DownloadedDocument,
        raw_html: str,
        article_html: str,
        markdown: str,
        document: str,
    ) -> None:
        self._logs_directory.mkdir(parents=True, exist_ok=True)
        (self._logs_directory / "raw_response.html").write_text(raw_html, encoding="utf-8", newline="\n")
        (self._logs_directory / "cleaned_article.html").write_text(article_html, encoding="utf-8", newline="\n")
        (self._logs_directory / "extracted_markdown.md").write_text(markdown, encoding="utf-8", newline="\n")

        headers = download_result.headers or {}
        content_type = download_result.content_type or headers.get("Content-Type")
        encoding = download_result.encoding
        header_payload = {
            "requested_url": download_result.requested_url,
            "final_url": download_result.final_url,
            "status_code": download_result.status_code,
            "content_type": content_type,
            "encoding": encoding,
            "headers": headers,
        }
        (self._logs_directory / "download_headers.json").write_text(
            json.dumps(header_payload, indent=2, ensure_ascii=True),
            encoding="utf-8",
            newline="\n",
        )

        redirect_payload = [hop._asdict() for hop in download_result.redirect_history]
        (self._logs_directory / "redirect_history.json").write_text(
            json.dumps(redirect_payload, indent=2, ensure_ascii=True),
            encoding="utf-8",
            newline="\n",
        )

        metadata = _metadata_from_document(document)
        (self._logs_directory / "metadata.json").write_text(
            json.dumps(metadata, indent=2, ensure_ascii=True, default=str),
            encoding="utf-8",
            newline="\n",
        )
        logger.info("DEBUG artifacts saved to %s", self._logs_directory)


_FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)


def _metadata_from_document(document: str) -> dict[str, object]:
    """Extract YAML front matter into a JSON-serializable object."""

    match = _FRONT_MATTER.match(document)
    if not match:
        return {}
    parsed = yaml.safe_load(match.group(1))
    if isinstance(parsed, dict):
        return parsed
    return {}


def create_default_collection_workflow(
    *,
    downloader: HtmlDownloader | None = None,
    extractor: HtmlExtractor | None = None,
    markdown_renderer: MarkdownRenderer | None = None,
    markdown_cleaner: MarkdownCleaner | None = None,
    metadata_generator: MetadataGenerator | None = None,
    storage: ArtifactStorage | None = None,
) -> CollectionWorkflow:
    """Build the standard page pipeline used by single-page and site crawls.

    Callers may replace any dependency, while the default composition stays in
    one location rather than being duplicated by each entry point.
    """

    if not is_playwright_available():
        logger.warning(
            "Playwright is not installed; JavaScript-heavy pages will be collected "
            "using requests HTML only, and the crawl will continue without it."
        )
    return CollectionWorkflow(
        downloader=downloader or Downloader(),
        extractor=extractor or HTMLExtractor(),
        browser_renderer=PlaywrightRenderer(),
        markdown_renderer=markdown_renderer or MarkdownConverter(),
        markdown_cleaner=markdown_cleaner or DefaultMarkdownCleaner(),
        metadata_generator=metadata_generator or DefaultMetadataGenerator(),
        storage=storage or DefaultFilesystemStorage(),
    )
