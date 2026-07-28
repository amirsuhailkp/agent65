"""Unit tests for the persistent crawl queue."""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from crawler.queue import CrawlQueue


class CrawlQueueTests(unittest.TestCase):
    def test_enqueue_dequeue_keeps_fifo_order(self) -> None:
        queue = CrawlQueue()
        queue.enqueue("https://example.test/a")
        queue.enqueue("https://example.test/b")

        self.assertEqual(queue.peek(), "https://example.test/a")
        self.assertEqual(queue.dequeue(), "https://example.test/a")
        self.assertEqual(queue.dequeue(), "https://example.test/b")
        self.assertTrue(queue.is_empty())

    def test_never_enqueues_duplicates(self) -> None:
        queue = CrawlQueue()

        first = queue.enqueue("https://example.test/a")
        second = queue.enqueue("https://example.test/a")
        third = queue.enqueue("  https://example.test/a  ")

        self.assertTrue(first)
        self.assertFalse(second)
        self.assertFalse(third)
        self.assertEqual(queue.size(), 1)
        self.assertEqual(queue.to_list(), ["https://example.test/a"])

    def test_save_and_load_json_supports_resume(self) -> None:
        with TemporaryDirectory() as temp_dir:
            queue_path = Path(temp_dir) / "crawl_queue.json"
            queue = CrawlQueue()
            queue.enqueue("https://example.test/a")
            queue.enqueue("https://example.test/b")
            queue.save_to_json(queue_path)

            resumed = CrawlQueue.load_from_json(queue_path)
            self.assertEqual(resumed.to_list(), ["https://example.test/a", "https://example.test/b"])
            self.assertEqual(resumed.dequeue(), "https://example.test/a")
            resumed.enqueue("https://example.test/c")
            self.assertEqual(resumed.to_list(), ["https://example.test/b", "https://example.test/c"])

    def test_load_rejects_invalid_schema(self) -> None:
        with TemporaryDirectory() as temp_dir:
            queue_path = Path(temp_dir) / "crawl_queue.json"
            queue_path.write_text('{"version": 1, "items": [123]}', encoding="utf-8")

            with self.assertRaises(ValueError):
                CrawlQueue.load_from_json(queue_path)

    def test_logs_size_after_operations(self) -> None:
        queue = CrawlQueue()
        with self.assertLogs("knowledge_collector.crawler.queue", level="INFO") as logs:
            queue.enqueue("https://example.test/a")
            queue.peek()
            queue.size()
            queue.is_empty()
            queue.dequeue()

        self.assertGreaterEqual(len(logs.output), 5)
        self.assertTrue(any("operation=enqueue" in message for message in logs.output))
        self.assertTrue(any("operation=peek" in message for message in logs.output))
        self.assertTrue(any("operation=size" in message for message in logs.output))
        self.assertTrue(any("operation=is_empty" in message for message in logs.output))
        self.assertTrue(any("operation=dequeue" in message for message in logs.output))


if __name__ == "__main__":
    unittest.main()
