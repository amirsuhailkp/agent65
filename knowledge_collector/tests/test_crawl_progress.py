"""Unit tests for terminal crawl progress reporting."""

from io import StringIO
import unittest

from crawler.progress import CrawlProgressTracker


class CrawlProgressTrackerTests(unittest.TestCase):
    def test_renders_required_statistics_and_estimated_time(self) -> None:
        clock_values = iter([0.0, 10.0])
        output = StringIO()
        tracker = CrawlProgressTracker(
            total_pages=10,
            stream=output,
            clock=lambda: next(clock_values),
            enabled=True,
        )

        with self.assertLogs("knowledge_collector.crawl_progress", level="INFO") as logs:
            tracker.update(
                current_page=3,
                pages_completed=2,
                pages_remaining=4,
                queue_size=4,
                visited_pages=2,
                current_depth=1,
                current_url="https://example.test/current",
            )
        tracker.finish()

        rendered = output.getvalue()
        self.assertIn("Current page: 3", rendered)
        self.assertIn("Pages completed: 2", rendered)
        self.assertIn("Pages remaining: 4", rendered)
        self.assertIn("Queue size: 4", rendered)
        self.assertIn("Visited pages: 2", rendered)
        self.assertIn("Current depth: 1", rendered)
        self.assertIn("Elapsed time: 00:10", rendered)
        self.assertIn("Estimated remaining time: 00:20", rendered)
        self.assertIn("Current URL: https://example.test/current", rendered)
        self.assertTrue(any("Current page: 3" in message for message in logs.output))


if __name__ == "__main__":
    unittest.main()
