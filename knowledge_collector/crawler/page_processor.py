"""Adapters that connect crawl traversal to the collection pipeline."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Protocol

from crawler.classifier import PageClassification, PageClassifier, PageType
from crawler.content_quality import ContentQualityScorer
from crawler.dedup import ContentHashStore, content_hash
from extractor.html_extractor import ExtractionError
from utils.artifact_names import build_artifact_filenames
from workflow.collection_workflow import CollectionWorkflow


logger = logging.getLogger("knowledge_collector.crawler.page_processor")


@dataclass(frozen=True, slots=True)
class ProcessedCrawlPage:
    """Page data needed by traversal after a successful collection."""

    discovery_html: str
    final_url: str
    download_size_bytes: int
    extraction_size_bytes: int
    extraction_collected: bool = False
    page_type: str = "unknown"
    saved: bool = False


class CrawlPageProcessor(Protocol):
    """Process one URL through the collection pipeline for a crawler."""

    def process(self, url: str) -> ProcessedCrawlPage:
        """Collect a page and return its post-processing crawl data."""


class WorkflowCrawlPageProcessor:
    """Use ``CollectionWorkflow`` once per queued URL without duplicate stages."""

    def __init__(
        self,
        workflow: CollectionWorkflow,
        *,
        collector: str,
        category: str = "uncategorized",
        language: str = "unknown",
    ) -> None:
        if not collector.strip():
            raise ValueError("collector cannot be empty")
        self._workflow = workflow
        self._collector = collector
        self._category = category
        self._language = language

    def process(self, url: str) -> ProcessedCrawlPage:
        raw_filename, processed_filename = build_artifact_filenames(self._collector, url)
        result = self._workflow.run(
            url=url,
            collector=self._collector,
            category=self._category,
            language=self._language,
            raw_filename=raw_filename,
            processed_filename=processed_filename,
        )
        return ProcessedCrawlPage(
            discovery_html=result.raw_html,
            final_url=result.final_url,
            download_size_bytes=len(result.raw_html.encode("utf-8")),
            extraction_size_bytes=result.extraction_size_bytes,
            extraction_collected=True,
        )


class ClassifyingCrawlPageProcessor:
    """Classify each page first, then route it through the right handling.

    This is the fix for crawlers that assumed every page was an article and
    therefore failed on hub/listing pages such as
    ``https://portswigger.net/research``:

    - LISTING / INDEX pages are never sent to extraction; their HTML is still
      returned so ``BFSCrawler`` discovers and queues their child links.
    - ARTICLE / DOCUMENTATION pages are deduplicated by content hash and, if
      new, run through the standard extraction/Markdown/metadata pipeline.
    - UNKNOWN pages are skipped safely: nothing is saved and no further links
      are discovered from them.
    """

    def __init__(
        self,
        workflow: CollectionWorkflow,
        *,
        downloader,
        collector: str,
        category: str = "uncategorized",
        language: str = "unknown",
        classifier: PageClassifier | None = None,
        quality_scorer: ContentQualityScorer | None = None,
        hash_store: ContentHashStore | None = None,
        subdirectory: str | None = None,
    ) -> None:
        if not collector.strip():
            raise ValueError("collector cannot be empty")
        self._workflow = workflow
        self._downloader = downloader
        self._collector = collector
        self._category = category
        self._language = language
        self._classifier = classifier or PageClassifier()
        self._quality_scorer = quality_scorer or ContentQualityScorer()
        self._hash_store = hash_store or ContentHashStore()
        self._subdirectory = subdirectory
        self.skipped_urls: list[tuple[str, str]] = []
        self.saved_urls: list[str] = []
        self.last_classification: PageClassification | None = None

    def process(self, url: str) -> ProcessedCrawlPage:
        raw_filename, processed_filename = build_artifact_filenames(self._collector, url)

        # The workflow downloads internally; here we need HTML first in order
        # to classify, so we fetch once and hand the same document to the
        # workflow via `downloaded_document` to avoid a second network call.
        downloaded_document = self._downloader.download_document(url)
        classification = self._classifier.classify(downloaded_document.html, downloaded_document.final_url)
        self.last_classification = classification
        html_bytes = len(downloaded_document.html.encode("utf-8"))

        if classification.page_type in (PageType.LISTING, PageType.INDEX):
            logger.info(
                "Classified %s as %s (confidence=%.2f); queuing links without saving",
                downloaded_document.final_url,
                classification.page_type.value,
                classification.confidence,
            )
            return ProcessedCrawlPage(
                discovery_html=downloaded_document.html,
                final_url=downloaded_document.final_url,
                download_size_bytes=html_bytes,
                extraction_size_bytes=0,
                extraction_collected=False,
                page_type=classification.page_type.value,
                saved=False,
            )

        if classification.page_type is PageType.UNKNOWN:
            logger.info(
                "Classified %s as unknown (confidence=%.2f); skipping safely",
                downloaded_document.final_url,
                classification.confidence,
            )
            self.skipped_urls.append((downloaded_document.final_url, "unknown_page_type"))
            return ProcessedCrawlPage(
                discovery_html="",
                final_url=downloaded_document.final_url,
                download_size_bytes=html_bytes,
                extraction_size_bytes=0,
                extraction_collected=False,
                page_type=classification.page_type.value,
                saved=False,
            )

        quality = self._quality_scorer.score(downloaded_document.html)
        if not quality.is_acceptable:
            logger.info(
                "Rejecting %s: content quality score %.2f below threshold",
                downloaded_document.final_url,
                quality.score,
            )
            self.skipped_urls.append((downloaded_document.final_url, "low_quality_content"))
            return ProcessedCrawlPage(
                discovery_html=downloaded_document.html,
                final_url=downloaded_document.final_url,
                download_size_bytes=html_bytes,
                extraction_size_bytes=0,
                extraction_collected=False,
                page_type=classification.page_type.value,
                saved=False,
            )

        digest = content_hash(downloaded_document.html)
        if not self._hash_store.record(digest, downloaded_document.final_url):
            self.skipped_urls.append((downloaded_document.final_url, "duplicate_content"))
            return ProcessedCrawlPage(
                discovery_html=downloaded_document.html,
                final_url=downloaded_document.final_url,
                download_size_bytes=html_bytes,
                extraction_size_bytes=0,
                extraction_collected=False,
                page_type=classification.page_type.value,
                saved=False,
            )

        try:
            result = self._workflow.run(
                url=url,
                collector=self._collector,
                category=self._category,
                language=self._language,
                raw_filename=raw_filename,
                processed_filename=processed_filename,
                downloaded_document=downloaded_document,
                subdirectory=self._subdirectory,
            )
        except ExtractionError as exc:
            logger.info(
                "Skipping %s after classification as %s: %s",
                downloaded_document.final_url,
                classification.page_type.value,
                exc,
            )
            self.skipped_urls.append((downloaded_document.final_url, "extraction_rejected"))
            return ProcessedCrawlPage(
                discovery_html=downloaded_document.html,
                final_url=downloaded_document.final_url,
                download_size_bytes=html_bytes,
                extraction_size_bytes=0,
                extraction_collected=False,
                page_type=classification.page_type.value,
                saved=False,
            )

        self.saved_urls.append(result.final_url)
        return ProcessedCrawlPage(
            discovery_html=downloaded_document.html,
            final_url=result.final_url,
            download_size_bytes=html_bytes,
            extraction_size_bytes=result.extraction_size_bytes,
            extraction_collected=True,
            page_type=classification.page_type.value,
            saved=True,
        )
