"""Reusable orchestration for collectors that process one source page at a time."""

from abc import ABC, abstractmethod
import logging
from collections.abc import Iterable
from pathlib import Path
from urllib.parse import urlsplit

from cleaner.markdown_cleaner import MarkdownCleaner
from downloader.downloader import Downloader
from extractor.html_extractor import HTMLExtractor
from extractor.markdown_converter import MarkdownConverter
from metadata.metadata_generator import MetadataGenerator
from storage.filesystem import FilesystemStorage
from workflow.collection_workflow import CollectionWorkflow, create_default_collection_workflow
from utils.artifact_names import build_artifact_filenames

from .base import BaseCollector


logger = logging.getLogger("knowledge_collector.collectors.single_page")


class SinglePageCollector(BaseCollector, ABC):
    """Coordinate the framework pipeline for a single validated source URL.

    Subclasses provide source identity, URL validation, and a default category.
    Future crawling can be introduced by overriding :meth:`discover` without
    changing the single-page processing pipeline.
    """

    default_category = "uncategorized"

    def __init__(
        self,
        *,
        downloader: Downloader | None = None,
        extractor: HTMLExtractor | None = None,
        markdown_converter: MarkdownConverter | None = None,
        cleaner: MarkdownCleaner | None = None,
        metadata_generator: MetadataGenerator | None = None,
        storage: FilesystemStorage | None = None,
        workflow: CollectionWorkflow | None = None,
    ) -> None:
        if workflow is not None and any(
            component is not None
            for component in (
                downloader,
                extractor,
                markdown_converter,
                cleaner,
                metadata_generator,
                storage,
            )
        ):
            raise ValueError("workflow cannot be combined with individual pipeline components")
        self._workflow = workflow or create_default_collection_workflow(
            downloader=downloader,
            extractor=extractor,
            markdown_renderer=markdown_converter,
            markdown_cleaner=cleaner,
            metadata_generator=metadata_generator,
            storage=storage,
        )

    def discover(self) -> Iterable[dict[str, str]]:
        """Return no URLs until a source-specific crawling policy is added."""

        return ()

    def collect(
        self,
        url: str,
        *,
        category: str | None = None,
        language: str = "unknown",
    ) -> Path:
        """Collect one page and return the saved processed Markdown path."""

        self._validate_source_url(url)
        raw_filename, processed_filename = build_artifact_filenames(self.source_name, url)
        resolved_category = category or self.default_category
        logger.info("Collecting %s page: %s", self.source_name, url)

        try:
            result = self._workflow.run(
                url=url,
                collector=self.source_name,
                category=resolved_category,
                language=language,
                raw_filename=raw_filename,
                processed_filename=processed_filename,
            )
        except Exception:
            logger.exception("Failed to collect %s page: %s", self.source_name, url)
            raise

        logger.info("Collected %s page to %s", self.source_name, result.processed_path)
        return result.processed_path

    @abstractmethod
    def _validate_source_url(self, url: str) -> None:
        """Raise ValueError unless ``url`` belongs to this collector's source."""



def validate_source_url(url: str, *, root_domain: str, collector_name: str) -> None:
    """Validate an absolute HTTP(S) URL constrained to a source root domain."""

    parsed = urlsplit(url)
    hostname = parsed.hostname.casefold() if parsed.hostname else ""
    if parsed.scheme not in {"http", "https"} or not hostname:
        raise ValueError(f"url must be an absolute HTTP(S) {collector_name} URL")
    if hostname != root_domain and not hostname.endswith(f".{root_domain}"):
        raise ValueError(f"{collector_name} only accepts {root_domain} URLs")
