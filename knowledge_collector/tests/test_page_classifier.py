"""Unit tests for crawler.classifier.PageClassifier."""

import unittest

from crawler.classifier import PageClassifier, PageType


_LISTING_HTML = """
<html><body>
<nav><a href="/">Home</a><a href="/research">Research</a></nav>
<div class="card-grid">
""" + "".join(
    f'<div class="card"><a href="/research/post-{i}">Short teaser text about post {i}.</a></div>'
    for i in range(12)
) + """
</div>
</body></html>
"""

_ARTICLE_HTML = """
<html><body>
<article>
<h1>Understanding SQL Injection</h1>
<p>SQL injection is a code injection technique that exploits a security
vulnerability in an application's software. It occurs when user input is
incorrectly filtered.</p>
<p>Attackers can use SQL injection to view, modify, or delete data that they
are not normally able to retrieve, and in some cases issue commands to the
operating system.</p>
<p>Mitigations include parameterized queries, input validation, and least
privilege database accounts to reduce the impact of a successful attack.</p>
<h2>Prevention</h2>
<p>Always use prepared statements with parameterized queries rather than
concatenating strings directly into SQL commands.</p>
</article>
</body></html>
"""

_DOC_HTML = """
<html><body>
<nav aria-label="breadcrumb"><a href="/">Docs</a> / <a href="/guide">Guide</a></nav>
<aside class="sidebar">
""" + "".join(f'<a href="/guide/section-{i}">Section {i}</a>' for i in range(10)) + """
</aside>
<main>
<h1>Installation Guide</h1>
<p>This guide walks through installing the tool from source.</p>
<pre><code>pip install the-tool</code></pre>
<h2>Configuration</h2>
<p>Set the API key using an environment variable before running any commands.</p>
</main>
</body></html>
"""

_UNKNOWN_HTML = "<html><body></body></html>"


class PageClassifierTests(unittest.TestCase):
    def setUp(self) -> None:
        self.classifier = PageClassifier()

    def test_classifies_card_grid_as_listing(self) -> None:
        result = self.classifier.classify(_LISTING_HTML, "https://portswigger.net/research")
        self.assertEqual(result.page_type, PageType.LISTING)

    def test_classifies_prose_page_as_article(self) -> None:
        result = self.classifier.classify(_ARTICLE_HTML, "https://example.test/blog/sql-injection")
        self.assertEqual(result.page_type, PageType.ARTICLE)

    def test_classifies_sidebar_guide_as_documentation(self) -> None:
        result = self.classifier.classify(_DOC_HTML, "https://docs.example.test/guide/install")
        self.assertEqual(result.page_type, PageType.DOCUMENTATION)

    def test_classifies_empty_page_as_unknown(self) -> None:
        result = self.classifier.classify(_UNKNOWN_HTML, "https://example.test/empty")
        self.assertEqual(result.page_type, PageType.UNKNOWN)

    def test_rejects_non_string_html(self) -> None:
        with self.assertRaises(TypeError):
            self.classifier.classify(None, "https://example.test/")  # type: ignore[arg-type]

    def test_rejects_empty_url(self) -> None:
        with self.assertRaises(ValueError):
            self.classifier.classify("<html></html>", "")

    def test_scores_sum_to_dict_of_all_types(self) -> None:
        result = self.classifier.classify(_ARTICLE_HTML, "https://example.test/a")
        self.assertEqual(set(result.scores), {member.value for member in PageType})


if __name__ == "__main__":
    unittest.main()
