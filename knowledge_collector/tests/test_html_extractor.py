"""Unit tests for main-article HTML extraction."""

from pathlib import Path
import tempfile
import unittest

from extractor.html_extractor import (
    CaptchaPageError,
    ErrorPageError,
    HTMLExtractor,
    LoginPageError,
    RedirectPageError,
    SuspiciousExtractionError,
)


RAW_PAGE = """
<html><body>
  <nav>Site navigation</nav><aside class="sidebar">Related links</aside>
  <article><h1>Article title</h1><p>Important paragraph.</p>
  <ul><li>One</li><li>Two</li></ul><table><tr><td>Data</td></tr></table>
  <pre><code>print('safe')</code></pre><footer>Article footer</footer></article>
  <div class="cookie-banner">Accept cookies</div>
</body></html>
"""


class HTMLExtractorTests(unittest.TestCase):
    def test_uses_primary_extractor_output_when_available(self) -> None:
        extractor = HTMLExtractor(
            extractor=lambda *_args, **_kwargs: "<p>Main content</p>",
            minimum_article_characters=1,
        )

        self.assertEqual(extractor.extract(RAW_PAGE), "<p>Main content</p>")

    def test_falls_back_and_removes_non_content_regions(self) -> None:
        extractor = HTMLExtractor(
            extractor=lambda *_args, **_kwargs: None,
            minimum_article_characters=1,
        )

        html = extractor.extract(RAW_PAGE)

        self.assertIn("<h1>Article title</h1>", html)
        self.assertIn("<table>", html)
        self.assertIn("<pre><code>print('safe')</code></pre>", html)
        self.assertNotIn("Site navigation", html)
        self.assertNotIn("Related links", html)
        self.assertNotIn("Accept cookies", html)

    def test_falls_back_when_primary_extractor_raises(self) -> None:
        def failing_extractor(*_args: object, **_kwargs: object) -> None:
            raise RuntimeError("invalid document")

        html = HTMLExtractor(
            extractor=failing_extractor,
            minimum_article_characters=1,
        ).extract(RAW_PAGE)

        self.assertIn("Important paragraph.", html)

    def test_rejects_redirect_page_before_extraction(self) -> None:
        redirect_html = """
        <html><body>
          <p>Redirecting to the canonical page...</p>
          <a href=\"/new-url\">Continue</a>
        </body></html>
        """
        extractor = HTMLExtractor(extractor=lambda *_args, **_kwargs: "<p>should not run</p>")

        with self.assertRaises(RedirectPageError) as context:
            extractor.extract(redirect_html)

        self.assertIn("redirect", context.exception.reason)

    def test_rejects_error_page_before_extraction(self) -> None:
        error_html = """
        <html><head><title>404 Not Found</title></head>
        <body><h1>404 Not Found</h1><p>The requested resource was not found.</p></body></html>
        """

        with self.assertRaises(ErrorPageError):
            HTMLExtractor(extractor=lambda *_args, **_kwargs: "<p>should not run</p>").extract(error_html)

    def test_rejects_login_page_before_extraction(self) -> None:
        login_html = """
        <html><body>
          <h1>Please Sign In</h1>
          <form action=\"/login\" method=\"post\">
            <input type=\"text\" name=\"username\" />
            <input type=\"password\" name=\"password\" />
          </form>
        </body></html>
        """

        with self.assertRaises(LoginPageError):
            HTMLExtractor(extractor=lambda *_args, **_kwargs: "<p>should not run</p>").extract(login_html)

    def test_rejects_captcha_page_before_extraction(self) -> None:
        captcha_html = """
        <html><body>
          <h1>Security Check</h1>
          <iframe src=\"https://www.google.com/recaptcha/api2/anchor\"></iframe>
        </body></html>
        """

        with self.assertRaises(CaptchaPageError):
            HTMLExtractor(extractor=lambda *_args, **_kwargs: "<p>should not run</p>").extract(captcha_html)

    def test_raises_when_extracted_article_is_suspiciously_small_and_saves_debug_html(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            debug_dir = Path(temp_dir)
            extractor = HTMLExtractor(
                extractor=lambda *_args, **_kwargs: "<p>tiny</p>",
                minimum_article_characters=500,
                debug_directory=debug_dir,
            )

            with self.assertRaises(SuspiciousExtractionError) as context:
                extractor.extract(RAW_PAGE)

            self.assertIn("suspiciously small", context.exception.reason)
            saved_files = list(debug_dir.glob("suspicious-extraction-*.html"))
            self.assertEqual(len(saved_files), 1)
