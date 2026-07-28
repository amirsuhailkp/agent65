"""Unit tests for HTML-to-Markdown conversion."""

import unittest

from extractor.markdown_converter import MarkdownConverter, remove_empty_elements


class MarkdownConverterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.converter = MarkdownConverter()

    def test_converts_article_structures_to_markdown(self) -> None:
        html = """
        <h1>Threat model</h1><p>Read <a href="https://example.test">this guide</a>.</p>
        <ul><li>Identify assets</li><li>Review controls</li></ul>
        <table><tr><th>Risk</th><th>Score</th></tr><tr><td>SQLi</td><td>High</td></tr></table>
        <pre><code class="language-python">print('safe')</code></pre>
        """

        markdown = self.converter.convert(html)

        self.assertIn("# Threat model", markdown)
        self.assertIn("[this guide](https://example.test)", markdown)
        self.assertIn("- Identify assets", markdown)
        self.assertIn("| Risk | Score |", markdown)
        self.assertIn("```python", markdown)
        self.assertIn("print('safe')", markdown)

    def test_removes_empty_sections_before_conversion(self) -> None:
        html = "<section><h2> </h2><p></p><div><p>Useful content</p></div></section>"

        self.assertEqual(self.converter.convert(html), "Useful content\n")
        self.assertNotIn("<h2>", remove_empty_elements(html))

    def test_returns_empty_markdown_for_empty_html(self) -> None:
        self.assertEqual(self.converter.convert("<section><p> </p></section>"), "")
