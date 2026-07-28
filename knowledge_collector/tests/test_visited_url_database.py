"""Unit tests for the persistent visited URL database."""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from crawler.visited import VisitedURLDatabase


class VisitedURLDatabaseTests(unittest.TestCase):
    def test_marks_and_checks_visited_urls(self) -> None:
        with TemporaryDirectory() as temp_directory:
            file_path = Path(temp_directory) / "visited.json"
            database = VisitedURLDatabase(file_path)

            self.assertFalse(database.is_visited("https://example.test/a"))
            self.assertTrue(database.mark_visited("https://example.test/a"))
            self.assertTrue(database.is_visited("https://example.test/a"))
            self.assertFalse(database.mark_visited("https://example.test/a"))
            self.assertEqual(database.visited_count, 1)

    def test_persists_and_loads_json(self) -> None:
        with TemporaryDirectory() as temp_directory:
            file_path = Path(temp_directory) / "visited.json"
            original = VisitedURLDatabase(file_path)
            original.mark_visited("https://example.test/a")
            original.mark_visited("https://example.test/b")

            restored = VisitedURLDatabase(file_path)
            self.assertTrue(restored.is_visited("https://example.test/a"))
            self.assertTrue(restored.is_visited("https://example.test/b"))
            self.assertEqual(restored.visited_count, 2)

    def test_logs_visited_statistics(self) -> None:
        with TemporaryDirectory() as temp_directory:
            file_path = Path(temp_directory) / "visited.json"
            database = VisitedURLDatabase(file_path)

            with self.assertLogs("knowledge_collector.crawler.visited", level="INFO") as logs:
                database.mark_visited("https://example.test/a")
                database.mark_visited("https://example.test/a")

            joined_logs = "\n".join(logs.output)
            self.assertIn("visited_count=1", joined_logs)
            self.assertIn("skipped_duplicates=1", joined_logs)
            self.assertIn("new_pages=1", joined_logs)

    def test_rejects_invalid_file_schema(self) -> None:
        with TemporaryDirectory() as temp_directory:
            file_path = Path(temp_directory) / "visited.json"
            file_path.write_text('{"version": 1, "urls": [123]}', encoding="utf-8")

            with self.assertRaises(ValueError):
                VisitedURLDatabase(file_path)


if __name__ == "__main__":
    unittest.main()