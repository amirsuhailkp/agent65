"""Unit tests for crawler.incremental.PageMetadataStore."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from crawler.incremental import PageMetadataStore, PageRecord, utc_now_iso


class PageMetadataStoreTests(unittest.TestCase):
    def test_unknown_url_needs_collection(self) -> None:
        with TemporaryDirectory() as temp_dir:
            store = PageMetadataStore(Path(temp_dir) / "meta.json")
            self.assertTrue(store.has_changed("https://example.test/new"))

    def test_matching_etag_means_unchanged(self) -> None:
        with TemporaryDirectory() as temp_dir:
            store = PageMetadataStore(Path(temp_dir) / "meta.json")
            store.record(
                PageRecord(
                    url="https://example.test/a",
                    sha256="abc123",
                    last_modified=None,
                    etag='"v1"',
                    crawl_timestamp=utc_now_iso(),
                    http_status=200,
                )
            )
            self.assertFalse(store.has_changed("https://example.test/a", etag='"v1"'))

    def test_different_etag_means_changed(self) -> None:
        with TemporaryDirectory() as temp_dir:
            store = PageMetadataStore(Path(temp_dir) / "meta.json")
            store.record(
                PageRecord(
                    url="https://example.test/a",
                    sha256="abc123",
                    last_modified=None,
                    etag='"v1"',
                    crawl_timestamp=utc_now_iso(),
                    http_status=200,
                )
            )
            self.assertTrue(store.has_changed("https://example.test/a", etag='"v2"'))

    def test_matching_sha256_means_unchanged(self) -> None:
        with TemporaryDirectory() as temp_dir:
            store = PageMetadataStore(Path(temp_dir) / "meta.json")
            store.record(
                PageRecord(
                    url="https://example.test/a",
                    sha256="abc123",
                    last_modified=None,
                    etag=None,
                    crawl_timestamp=utc_now_iso(),
                    http_status=200,
                )
            )
            self.assertFalse(store.has_changed("https://example.test/a", sha256="abc123"))

    def test_persists_across_instances(self) -> None:
        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "meta.json"
            PageMetadataStore(path).record(
                PageRecord(
                    url="https://example.test/a",
                    sha256="abc123",
                    last_modified="Mon, 01 Jan 2024 00:00:00 GMT",
                    etag=None,
                    crawl_timestamp=utc_now_iso(),
                    http_status=200,
                )
            )
            second_store = PageMetadataStore(path)
            record = second_store.get("https://example.test/a")
            self.assertIsNotNone(record)
            self.assertEqual(record.sha256, "abc123")


if __name__ == "__main__":
    unittest.main()
