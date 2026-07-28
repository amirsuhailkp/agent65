"""Unit tests for fence-aware Markdown cleanup."""

import unittest

from cleaner.markdown_cleaner import MarkdownCleaner


class MarkdownCleanerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cleaner = MarkdownCleaner()

    def test_removes_common_web_boilerplate(self) -> None:
        source = """
<!-- page metadata -->
#   Threat Guide ##

![tracking](data:image/png;base64,aGVsbG8=)
[Home](/) | [Next](/next)
[Donate](https://example.test/donate)
[Edit this page](https://example.test/edit)
We use cookies to improve this website.
<script>window.tracker()</script>
[unsafe](javascript:alert(1))


Useful [reference](https://example.test/reference).
"""

        cleaned = self.cleaner.clean(source)

        self.assertEqual(cleaned, "# Threat Guide\n\nUseful [reference](https://example.test/reference).\n")

    def test_preserves_fenced_code_and_its_contents(self) -> None:
        source = """Before\n\n```javascript
// [Donate](https://example.test/donate)
window.alert('cookie notice')
```
\n\nAfter\n"""

        cleaned = self.cleaner.clean(source)

        self.assertIn("```javascript\n// [Donate](https://example.test/donate)\nwindow.alert('cookie notice')\n```", cleaned)
        self.assertIn("Before", cleaned)
        self.assertIn("After", cleaned)

    def test_preserves_lists_and_tables_while_trimming_whitespace(self) -> None:
        source = "  - First item   \n  - Second item\n\n| Risk | Level |   \n| --- | --- |\n| XSS | High |\n"

        cleaned = self.cleaner.clean(source)

        self.assertIn("  - First item\n  - Second item", cleaned)
        self.assertIn("| Risk | Level |", cleaned)
