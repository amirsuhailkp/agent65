"""Unit-test examples for the downloader, with no live network calls."""

import unittest
from unittest.mock import MagicMock

import requests

from downloader.downloader import Downloader, DownloaderError, RedirectResolutionError


class DownloaderTests(unittest.TestCase):
    """Verify the downloader boundary using an injected mock session."""

    def setUp(self) -> None:
        self.session = MagicMock(spec=requests.Session)
        self.session.headers = {}
        self.downloader = Downloader(session=self.session, timeout=5.0)

    def test_download_returns_html_and_follows_redirects(self) -> None:
        response = MagicMock()
        response.text = "<html><body>ok</body></html>"
        response.url = "https://example.test/final"
        response.status_code = 200
        response.content = response.text.encode()
        response.history = []
        self.session.get.return_value = response

        html = self.downloader.download("https://example.test/original")

        self.assertEqual(html, response.text)
        self.session.get.assert_called_once_with(
            "https://example.test/original",
            timeout=5.0,
            allow_redirects=True,
        )
        response.raise_for_status.assert_called_once_with()

    def test_download_document_records_http_redirect_history(self) -> None:
        redirect = MagicMock(url="https://example.test/original", status_code=301)
        response = MagicMock(
            text="<html><body>article</body></html>",
            url="https://example.test/final",
            status_code=200,
            content=b"article",
            history=[redirect],
        )
        self.session.get.return_value = response

        result = self.downloader.download_document("https://example.test/original")

        self.assertEqual(result.final_url, "https://example.test/final")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.redirect_history[0].source_url, "https://example.test/original")
        self.assertEqual(result.redirect_history[0].destination_url, "https://example.test/final")

    def test_resolves_meta_refresh_to_final_article(self) -> None:
        redirect_page = MagicMock(
            text='<meta http-equiv="refresh" content="0; url=/article">',
            url="https://example.test/start",
            status_code=200,
            content=b"redirect",
            history=[],
        )
        final_page = MagicMock(
            text="<article>Final article</article>",
            url="https://example.test/article",
            status_code=200,
            content=b"article",
            history=[],
        )
        self.session.get.side_effect = [redirect_page, final_page]

        result = self.downloader.download_document("https://example.test/start")

        self.assertEqual(result.html, "<article>Final article</article>")
        self.assertEqual(result.final_url, "https://example.test/article")
        self.assertEqual(result.redirect_history[-1].mechanism, "meta refresh")
        self.assertEqual(self.session.get.call_count, 2)

    def test_raises_for_redirect_only_page_without_destination(self) -> None:
        response = MagicMock(
            text="<html><body>Redirecting...</body></html>",
            url="https://example.test/start",
            status_code=200,
            content=b"redirect",
            history=[],
        )
        self.session.get.return_value = response

        with self.assertRaises(RedirectResolutionError):
            self.downloader.download_document("https://example.test/start")

    def test_resolves_javascript_location_redirect(self) -> None:
        redirect_page = MagicMock(
            text='<script>window.location.href = "/article";</script>',
            url="https://example.test/start",
            status_code=200,
            content=b"redirect",
            history=[],
        )
        final_page = MagicMock(
            text="<article>Final article</article>",
            url="https://example.test/article",
            status_code=200,
            content=b"article",
            history=[],
        )
        self.session.get.side_effect = [redirect_page, final_page]

        result = self.downloader.download_document("https://example.test/start")

        self.assertEqual(result.final_url, "https://example.test/article")
        self.assertEqual(result.redirect_history[-1].mechanism, "JavaScript location")

    def test_resolves_redirecting_page_link(self) -> None:
        redirect_page = MagicMock(
            text='<a href="/article">Redirecting...</a>',
            url="https://example.test/start",
            status_code=200,
            content=b"redirect",
            history=[],
        )
        final_page = MagicMock(
            text="<article>Final article</article>",
            url="https://example.test/article",
            status_code=200,
            content=b"article",
            history=[],
        )
        self.session.get.side_effect = [redirect_page, final_page]

        result = self.downloader.download_document("https://example.test/start")

        self.assertEqual(result.final_url, "https://example.test/article")
        self.assertEqual(result.redirect_history[-1].mechanism, "redirecting page")

    def test_download_wraps_http_errors(self) -> None:
        response = MagicMock(status_code=404)
        response.raise_for_status.side_effect = requests.HTTPError(
            "not found", response=response
        )
        response.url = "https://example.test/missing"
        self.session.get.return_value = response

        with self.assertRaises(DownloaderError) as context:
            self.downloader.download("https://example.test/missing")

        self.assertIsInstance(context.exception.__cause__, requests.HTTPError)

    def test_download_wraps_network_errors(self) -> None:
        self.session.get.side_effect = requests.ConnectionError("connection refused")

        with self.assertRaises(DownloaderError) as context:
            self.downloader.download("https://example.test")

        self.assertIsInstance(context.exception.__cause__, requests.ConnectionError)
