"""Unit tests for crawler.content_quality.ContentQualityScorer."""

import unittest

from crawler.content_quality import ContentQualityScorer


class ContentQualityScorerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.scorer = ContentQualityScorer()

    def test_accepts_rich_article_content(self) -> None:
        html = """
        <article>
        <h1>Title</h1>
        <p>This is a full paragraph with plenty of meaningful text describing
        a real security concept in enough depth to be useful to a reader.</p>
        <p>Here is a second paragraph continuing the explanation with more
        detail and context about mitigations and best practices.</p>
        <pre><code>example code block</code></pre>
        </article>
        """
        result = self.scorer.score(html)
        self.assertTrue(result.is_acceptable)
        self.assertGreater(result.score, 0.3)

    def test_rejects_empty_page(self) -> None:
        result = self.scorer.score("<html><body></body></html>")
        self.assertFalse(result.is_acceptable)

    def test_rejects_pure_navigation_boilerplate(self) -> None:
        html = "<nav>" + "".join(f'<a href="/{i}">Link {i}</a>' for i in range(30)) + "</nav>"
        result = self.scorer.score(html)
        self.assertFalse(result.is_acceptable)

    def test_rejects_invalid_threshold(self) -> None:
        with self.assertRaises(ValueError):
            ContentQualityScorer(acceptance_threshold=1.5)

    def test_rejects_non_string_html(self) -> None:
        with self.assertRaises(TypeError):
            self.scorer.score(None)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
