"""Unit tests for crawler.dedup."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from crawler.dedup import ContentHashStore, canonicalize_url, content_hash


class CanonicalizeUrlTests(unittest.TestCase):
    def test_strips_tracking_parameters(self) -> None:
        result = canonicalize_url("https://example.test/page?utm_source=x&id=5")
        self.assertEqual(result, "https://example.test/page?id=5")

    def test_strips_www_and_default_port(self) -> None:
        result = canonicalize_url("https://www.example.test:443/page/")
        self.assertEqual(result, "https://example.test/page")

    def test_rejects_non_http_scheme(self) -> None:
        self.assertIsNone(canonicalize_url("ftp://example.test/file"))

    def test_rejects_empty_string(self) -> None:
        self.assertIsNone(canonicalize_url(""))

    def test_equivalent_urls_canonicalize_identically(self) -> None:
        first = canonicalize_url("https://Example.test/Page/?ref=newsletter")
        second = canonicalize_url("https://www.example.test/Page")
        # Hostname casing is normalized, but path case is preserved
        # (paths can be case-sensitive on the server), so only query/host
        # normalization is asserted here.
        self.assertEqual(first, "https://example.test/Page")
        self.assertEqual(second, "https://example.test/Page")


class ContentHashStoreTests(unittest.TestCase):
    def test_records_new_hash_as_not_duplicate(self) -> None:
        with TemporaryDirectory() as temp_dir:
            store = ContentHashStore(Path(temp_dir) / "hashes.json")
            digest = content_hash("<html>hello</html>")
            self.assertTrue(store.record(digest, "https://example.test/a"))

    def test_second_url_with_same_content_is_duplicate(self) -> None:
        with TemporaryDirectory() as temp_dir:
            store = ContentHashStore(Path(temp_dir) / "hashes.json")
            digest = content_hash("<html>hello</html>")
            store.record(digest, "https://example.test/a")
            self.assertFalse(store.record(digest, "https://example.test/mirror-of-a"))

    def test_persists_across_instances(self) -> None:
        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "hashes.json"
            digest = content_hash("<html>hello</html>")
            ContentHashStore(path).record(digest, "https://example.test/a")

            second_store = ContentHashStore(path)
            self.assertTrue(second_store.seen(digest))


if __name__ == "__main__":
    unittest.main()
