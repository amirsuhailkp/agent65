"""Unit tests for config.sources.SourceRegistry."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from config.sources import SourceConfigError, SourceRegistry


class SourceRegistryTests(unittest.TestCase):
    def test_loads_default_sources_yaml(self) -> None:
        registry = SourceRegistry.load()
        self.assertIn("owasp", registry.enabled_names())
        self.assertIn("portswigger", registry.enabled_names())

    def test_disabled_source_is_excluded_from_enabled_names(self) -> None:
        registry = SourceRegistry.load()
        all_names = {source.name for source in registry.all_sources()}
        self.assertIn("example-sitemap-source", all_names)
        self.assertNotIn("example-sitemap-source", registry.enabled_names())

    def test_get_unknown_source_raises_key_error(self) -> None:
        registry = SourceRegistry.load()
        with self.assertRaises(KeyError):
            registry.get("not-a-real-source")

    def test_allowed_hostnames_derived_from_start_urls(self) -> None:
        registry = SourceRegistry.load()
        config = registry.get("portswigger")
        self.assertIn("portswigger.net", config.allowed_hostnames())

    def test_unlimited_pages_flag(self) -> None:
        registry = SourceRegistry.load()
        self.assertTrue(registry.get("hacktricks").is_unlimited_pages)
        self.assertFalse(registry.get("owasp").is_unlimited_pages)

    def test_legacy_minimal_schema_still_loads(self) -> None:
        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "sources.yaml"
            path.write_text(
                """
sources:
  - name: LegacySource
    type: crawler
    url: https://legacy.test/start
    output: raw_documents/legacy/
""",
                encoding="utf-8",
            )
            registry = SourceRegistry.load(path)
            config = registry.get("legacysource")
            self.assertEqual(config.start_urls, ("https://legacy.test/start",))
            self.assertEqual(config.slug, "legacy")

    def test_missing_file_raises_source_config_error(self) -> None:
        with self.assertRaises(SourceConfigError):
            SourceRegistry.load(Path("/nonexistent/sources.yaml"))

    def test_empty_sources_list_raises_source_config_error(self) -> None:
        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "sources.yaml"
            path.write_text("sources: []\n", encoding="utf-8")
            with self.assertRaises(SourceConfigError):
                SourceRegistry.load(path)

    def test_duplicate_source_names_raise_error(self) -> None:
        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "sources.yaml"
            path.write_text(
                """
sources:
  - name: dupe
    start_urls: ["https://a.test/"]
  - name: dupe
    start_urls: ["https://b.test/"]
""",
                encoding="utf-8",
            )
            with self.assertRaises(SourceConfigError):
                SourceRegistry.load(path)

    def test_invalid_collector_type_raises_error(self) -> None:
        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "sources.yaml"
            path.write_text(
                """
sources:
  - name: bad
    collector_type: not_a_real_type
    start_urls: ["https://a.test/"]
""",
                encoding="utf-8",
            )
            with self.assertRaises(SourceConfigError):
                SourceRegistry.load(path)

    def test_negative_max_pages_raises_error(self) -> None:
        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "sources.yaml"
            path.write_text(
                """
sources:
  - name: bad
    start_urls: ["https://a.test/"]
    max_pages: -5
""",
                encoding="utf-8",
            )
            with self.assertRaises(SourceConfigError):
                SourceRegistry.load(path)


if __name__ == "__main__":
    unittest.main()
