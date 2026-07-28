"""Unit tests for safe raw and processed filesystem persistence."""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from storage.filesystem import FilesystemStorage, validate_filename


class FilesystemStorageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = TemporaryDirectory()
        self.base_directory = Path(self.temporary_directory.name)
        self.storage = FilesystemStorage(self.base_directory)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_creates_storage_directories_and_saves_content(self) -> None:
        path = self.storage.save_raw("<html>raw</html>", "article.html")

        self.assertTrue((self.base_directory / "raw").is_dir())
        self.assertTrue((self.base_directory / "processed").is_dir())
        self.assertEqual(path, self.base_directory / "raw" / "article.html")
        self.assertEqual(path.read_text(encoding="utf-8"), "<html>raw</html>")

    def test_versions_duplicate_names_without_overwriting(self) -> None:
        original = self.storage.save_processed("first", "article.md")
        versioned = self.storage.save_processed("second", "article.md")

        self.assertEqual(original.name, "article.md")
        self.assertEqual(versioned.name, "article (1).md")
        self.assertEqual(original.read_text(encoding="utf-8"), "first")
        self.assertEqual(versioned.read_text(encoding="utf-8"), "second")

    def test_rejects_paths_and_portability_unsafe_names(self) -> None:
        for filename in ("../escape.md", "nested/file.md", "CON.txt", "report?.md", ""):
            with self.subTest(filename=filename):
                with self.assertRaises(ValueError):
                    validate_filename(filename)

    def test_saves_binary_content(self) -> None:
        path = self.storage.save_raw(b"\x00\x01", "source.bin")

        self.assertEqual(path.read_bytes(), b"\x00\x01")
