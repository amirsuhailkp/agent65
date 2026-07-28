"""Generic, configuration-driven collectors with one common interface.

Every collector type below (``generic_html``, ``documentation_site``,
``blog_site``, ``api_docs``, ``rss_feed``, ``sitemap_site``) exposes the same
surface: ``crawl()``, ``download()``, ``extract_links()``, ``extract_content()``.
The downstream pipeline (page classification, extraction, Markdown
conversion, storage) never needs to know which website produced a document;
only a source's ``config/sources.yaml`` entry varies.

Adding a brand-new source therefore never requires a new Python class: pick
an existing ``collector_type`` (or ``generic_html`` as a safe default) and
declare the source in YAML.
"""

from __future__ import annotations

import logging
from xml.etree import ElementTree

from config.sources import SourceConfig
from crawler.url_discovery import URLDiscoveryEngine
from downloader.downloader import Downloader
from extractor.html_extractor import HTMLExtractor


logger = logging.getLogger("knowledge_collector.collectors.generic")


class SeedStrategy:
    """Return the initial crawl seed URLs for a collector type.

    The default strategy simply seeds from ``config.start_urls``, which is
    correct for ``generic_html``, ``documentation_site``, ``blog_site``, and
    ``api_docs`` -- these all discover further pages by following links from
    a normal HTML start page.
    """

    def seeds(self, config: SourceConfig, downloader: Downloader) -> list[str]:
        return list(config.start_urls)


class SitemapSeedStrategy(SeedStrategy):
    """Seed URLs by parsing one or more ``sitemap.xml`` documents."""

    def seeds(self, config: SourceConfig, downloader: Downloader) -> list[str]:
        urls: list[str] = []
        for start_url in config.start_urls:
            try:
                xml_text = downloader.download(start_url)
                urls.extend(_parse_sitemap_locations(xml_text))
            except Exception as exc:
                logger.warning("Failed to parse sitemap %s: %s", start_url, exc)
        return urls or list(config.start_urls)


class RssFeedSeedStrategy(SeedStrategy):
    """Seed URLs by parsing one or more RSS/Atom feed documents."""

    def seeds(self, config: SourceConfig, downloader: Downloader) -> list[str]:
        urls: list[str] = []
        for start_url in config.start_urls:
            try:
                xml_text = downloader.download(start_url)
                urls.extend(_parse_feed_links(xml_text))
            except Exception as exc:
                logger.warning("Failed to parse feed %s: %s", start_url, exc)
        return urls or list(config.start_urls)


_SEED_STRATEGIES: dict[str, SeedStrategy] = {
    "generic_html": SeedStrategy(),
    "documentation_site": SeedStrategy(),
    "blog_site": SeedStrategy(),
    "api_docs": SeedStrategy(),
    "sitemap_site": SitemapSeedStrategy(),
    "rss_feed": RssFeedSeedStrategy(),
}


def seed_strategy_for(collector_type: str) -> SeedStrategy:
    """Return the seeding strategy registered for ``collector_type``."""

    return _SEED_STRATEGIES.get(collector_type, SeedStrategy())


def _parse_sitemap_locations(xml_text: str) -> list[str]:
    try:
        root = ElementTree.fromstring(xml_text)
    except ElementTree.ParseError:
        return []
    return [
        element.text.strip()
        for element in root.iter()
        if element.tag.rsplit("}", 1)[-1] == "loc" and element.text and element.text.strip()
    ]


def _parse_feed_links(xml_text: str) -> list[str]:
    try:
        root = ElementTree.fromstring(xml_text)
    except ElementTree.ParseError:
        return []
    links: list[str] = []
    for element in root.iter():
        tag = element.tag.rsplit("}", 1)[-1]
        if tag == "link":
            href = element.get("href")
            if href and href.strip():
                links.append(href.strip())
            elif element.text and element.text.strip():
                links.append(element.text.strip())
    return links


class GenericCollector:
    """Common, source-agnostic collector interface driven by ``SourceConfig``.

    This is the ``crawl()``/``download()``/``extract_links()``/
    ``extract_content()`` interface required for every collector to look
    identical to the downstream pipeline (item 13 of the upgrade). The
    heavier lifting -- classification, quality scoring, deduplication,
    Markdown conversion, and persistence -- is composed from the existing
    framework modules in ``crawler/page_processor.py`` and
    ``workflow/collection_workflow.py``; this class exists to give collectors
    one stable, minimal surface plus source-specific seeding.
    """

    def __init__(
        self,
        config: SourceConfig,
        *,
        downloader: Downloader | None = None,
        url_discovery: URLDiscoveryEngine | None = None,
        extractor: HTMLExtractor | None = None,
    ) -> None:
        self.config = config
        self._downloader = downloader or Downloader()
        self._url_discovery = url_discovery or URLDiscoveryEngine()
        self._extractor = extractor or HTMLExtractor()
        self._seed_strategy = seed_strategy_for(config.collector_type)

    @property
    def source_name(self) -> str:
        return self.config.name

    def crawl(self) -> list[str]:
        """Return this source's initial crawl seed URLs.

        Full-site traversal beyond the seeds is performed by ``BFSCrawler``
        with a ``ClassifyingCrawlPageProcessor`` (see ``main.py``); this
        method only resolves collector-type-specific starting points (e.g.
        parsing a sitemap or feed into individual article URLs).
        """

        return self._seed_strategy.seeds(self.config, self._downloader)

    def download(self, url: str) -> str:
        """Download raw HTML/XML for one URL."""

        return self._downloader.download(url)

    def extract_links(self, html: str, *, base_url: str) -> list[str]:
        """Discover normalized links from one HTML document."""

        return self._url_discovery.discover_urls(html, base_url=base_url)

    def extract_content(self, html: str) -> str:
        """Extract the main-article HTML from one downloaded page."""

        return self._extractor.extract(html)

    def close(self) -> None:
        self._downloader.close()

    def __enter__(self) -> "GenericCollector":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
