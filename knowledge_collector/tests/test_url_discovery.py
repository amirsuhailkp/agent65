"""Unit tests for HTML hyperlink discovery and normalization."""

import unittest

from crawler.url_discovery import URLDiscoveryEngine


class URLDiscoveryEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = URLDiscoveryEngine()

    def test_discovers_resolves_normalizes_and_deduplicates_urls(self) -> None:
        html = """
        <html><body>
          <a href="/guide">Guide</a>
          <a href="docs/intro#overview">Intro Fragment</a>
                    <a href="HTTPS://EXAMPLE.TEST:443/base/docs/intro#install">Absolute Duplicate</a>
                    <a href="https://example.test/base/docs/intro/">Trailing Slash Duplicate</a>
          <a href="https://example.test/reference?q=api#section">Reference</a>
          <a href="https://example.test/reference?q=api#other">Reference Duplicate via Fragment</a>
        </body></html>
        """

        urls = self.engine.discover_urls(html, base_url="https://example.test/base/page")

        self.assertEqual(
            urls,
            [
                "https://example.test/guide",
                "https://example.test/base/docs/intro",
                "https://example.test/reference?q=api",
            ],
        )

    def test_ignores_invalid_and_non_http_links(self) -> None:
        html = """
        <html><body>
          <a href="">Empty</a>
          <a href="   ">Whitespace</a>
          <a href="#section">Anchor only</a>
          <a href="javascript:void(0)">JS</a>
          <a href="mailto:test@example.test">Mailto</a>
          <a href="tel:+123456">Phone</a>
          <a href="data:text/plain;base64,SGVsbG8=">Data URL</a>
          <a href="ftp://example.test/file">FTP</a>
          <a href="/valid">Valid</a>
        </body></html>
        """

        urls = self.engine.discover_urls(html, base_url="https://example.test/start")

        self.assertEqual(urls, ["https://example.test/valid"])

    def test_logs_discovery_statistics(self) -> None:
        html = """
        <html><body>
          <a href="/a">A</a>
          <a href="/a#fragment">A Duplicate by Fragment</a>
          <a href="javascript:void(0)">Invalid</a>
        </body></html>
        """

        with self.assertLogs("knowledge_collector.crawler.url_discovery", level="INFO") as logs:
            urls = self.engine.discover_urls(html, base_url="https://example.test")

        self.assertEqual(urls, ["https://example.test/a"])
        joined_logs = "\n".join(logs.output)
        self.assertIn("total_links=3", joined_logs)
        self.assertIn("valid_links=1", joined_logs)
        self.assertIn("invalid_links=1", joined_logs)
        self.assertIn("duplicates_removed=1", joined_logs)

    def test_rejects_invalid_input_types(self) -> None:
        with self.assertRaises(TypeError):
            self.engine.discover_urls(123, base_url="https://example.test")  # type: ignore[arg-type]

        with self.assertRaises(ValueError):
            self.engine.discover_urls("<a href='/x'>x</a>", base_url="")


if __name__ == "__main__":
    unittest.main()
