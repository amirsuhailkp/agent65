"""Unit tests for collectors.generic."""

import unittest
from unittest.mock import MagicMock

from collectors.generic import (
    GenericCollector,
    RssFeedSeedStrategy,
    SeedStrategy,
    SitemapSeedStrategy,
    seed_strategy_for,
)
from config.sources import SourceConfig


def _make_config(**overrides: object) -> SourceConfig:
    defaults = dict(
        name="example",
        display_name="Example",
        collector_type="generic_html",
        start_urls=("https://example.test/",),
    )
    defaults.update(overrides)
    return SourceConfig(**defaults)  # type: ignore[arg-type]


class SeedStrategyTests(unittest.TestCase):
    def test_default_strategy_returns_start_urls(self) -> None:
        config = _make_config()
        strategy = SeedStrategy()
        self.assertEqual(strategy.seeds(config, MagicMock()), ["https://example.test/"])

    def test_sitemap_strategy_parses_locations(self) -> None:
        config = _make_config(start_urls=("https://example.test/sitemap.xml",))
        downloader = MagicMock()
        downloader.download.return_value = (
            "<urlset><url><loc>https://example.test/a</loc></url>"
            "<url><loc>https://example.test/b</loc></url></urlset>"
        )
        strategy = SitemapSeedStrategy()
        self.assertEqual(
            strategy.seeds(config, downloader),
            ["https://example.test/a", "https://example.test/b"],
        )

    def test_sitemap_strategy_falls_back_on_parse_error(self) -> None:
        config = _make_config(start_urls=("https://example.test/sitemap.xml",))
        downloader = MagicMock()
        downloader.download.return_value = "not xml"
        strategy = SitemapSeedStrategy()
        self.assertEqual(strategy.seeds(config, downloader), ["https://example.test/sitemap.xml"])

    def test_rss_strategy_parses_links(self) -> None:
        config = _make_config(start_urls=("https://example.test/feed.xml",))
        downloader = MagicMock()
        downloader.download.return_value = (
            "<rss><channel><item><link>https://example.test/post-1</link></item></channel></rss>"
        )
        strategy = RssFeedSeedStrategy()
        self.assertEqual(strategy.seeds(config, downloader), ["https://example.test/post-1"])

    def test_seed_strategy_for_unknown_type_defaults_to_generic(self) -> None:
        self.assertIsInstance(seed_strategy_for("something_undeclared"), SeedStrategy)

    def test_seed_strategy_for_sitemap(self) -> None:
        self.assertIsInstance(seed_strategy_for("sitemap_site"), SitemapSeedStrategy)


class GenericCollectorTests(unittest.TestCase):
    def test_crawl_delegates_to_seed_strategy(self) -> None:
        config = _make_config(collector_type="documentation_site")
        downloader = MagicMock()
        collector = GenericCollector(config, downloader=downloader)
        self.assertEqual(collector.crawl(), ["https://example.test/"])

    def test_download_delegates_to_downloader(self) -> None:
        config = _make_config()
        downloader = MagicMock()
        downloader.download.return_value = "<html></html>"
        collector = GenericCollector(config, downloader=downloader)
        self.assertEqual(collector.download("https://example.test/x"), "<html></html>")
        downloader.download.assert_called_once_with("https://example.test/x")

    def test_extract_links_delegates_to_url_discovery(self) -> None:
        config = _make_config()
        url_discovery = MagicMock()
        url_discovery.discover_urls.return_value = ["https://example.test/child"]
        collector = GenericCollector(config, downloader=MagicMock(), url_discovery=url_discovery)
        links = collector.extract_links("<html></html>", base_url="https://example.test/")
        self.assertEqual(links, ["https://example.test/child"])

    def test_extract_content_delegates_to_extractor(self) -> None:
        config = _make_config()
        extractor = MagicMock()
        extractor.extract.return_value = "<article>content</article>"
        collector = GenericCollector(config, downloader=MagicMock(), extractor=extractor)
        self.assertEqual(collector.extract_content("<html></html>"), "<article>content</article>")

    def test_context_manager_closes_downloader(self) -> None:
        config = _make_config()
        downloader = MagicMock()
        with GenericCollector(config, downloader=downloader):
            pass
        downloader.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
