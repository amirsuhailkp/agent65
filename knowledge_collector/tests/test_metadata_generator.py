"""Unit tests for generated YAML front matter."""

from datetime import UTC, datetime
import unittest

import yaml

from metadata.metadata_generator import MetadataGenerator, extract_title, generate_tags


class MetadataGeneratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.generator = MetadataGenerator(
            clock=lambda: datetime(2026, 7, 25, 12, 30, tzinfo=UTC)
        )

    def test_prepends_complete_yaml_front_matter(self) -> None:
        document = self.generator.generate(
            "# SQL Injection Prevention\n\nUse parameterized queries.",
            url="https://www.owasp.org/www-community/attacks/SQL_Injection",
            collector="owasp",
            category="web-security",
            language="en",
        )

        _, raw_metadata, body = document.split("---", maxsplit=2)
        metadata = yaml.safe_load(raw_metadata)
        self.assertEqual(metadata["title"], "SQL Injection Prevention")
        self.assertEqual(metadata["source"], "owasp.org")
        self.assertEqual(metadata["collector"], "owasp")
        self.assertEqual(metadata["date_collected"], "2026-07-25T12:30:00Z")
        self.assertIn("sql", metadata["tags"])
        self.assertEqual(body.strip(), "# SQL Injection Prevention\n\nUse parameterized queries.")

    def test_replaces_existing_front_matter(self) -> None:
        document = self.generator.generate(
            "---\ntitle: stale\n---\n\n# Fresh Title",
            url="https://example.test/article",
            collector="example",
        )

        self.assertEqual(document.count("---"), 2)
        self.assertIn("title: Fresh Title", document)
        self.assertNotIn("stale", document)

    def test_extract_title_and_tags_ignore_code_blocks(self) -> None:
        markdown = "# Secure Headers\n\n```python\npassword exploit exploit\n```\n\nHeaders reduce risk."

        self.assertEqual(extract_title(markdown), "Secure Headers")
        self.assertIn("headers", generate_tags(markdown))
        self.assertNotIn("exploit", generate_tags(markdown))
