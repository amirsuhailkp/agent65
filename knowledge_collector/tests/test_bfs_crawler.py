"""Unit tests for breadth-first crawler behavior."""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from crawler.bfs_crawler import BFSCrawler
from crawler.page_processor import ProcessedCrawlPage
from crawler.rate_limiter import RateLimiter
from crawler.visited import VisitedURLDatabase


class FakeFetcher:
    def __init__(self, pages: dict[str, str]) -> None:
        self._pages = pages
        self.calls: list[str] = []

    def download(self, url: str) -> str:
        self.calls.append(url)
        return self._pages[url]


class FakeClock:
    def __init__(self, values: list[float]) -> None:
        self._values = iter(values)
        self._last = 0.0

    def __call__(self) -> float:
        try:
            self._last = next(self._values)
        except StopIteration:
            pass
        return self._last


class FakePageProcessor:
    def __init__(self, pages: dict[str, ProcessedCrawlPage]) -> None:
        self._pages = pages
        self.calls: list[str] = []

    def process(self, url: str) -> ProcessedCrawlPage:
        self.calls.append(url)
        return self._pages[url]


def _unlimited_rate_limiter() -> RateLimiter:
    return RateLimiter(0, jitter_min_seconds=0, jitter_max_seconds=0)


class BFSCrawlerTests(unittest.TestCase):
    def test_processes_each_page_before_discovering_the_next_page(self) -> None:
        with TemporaryDirectory() as temp_dir:
            start = "https://example.test/start"
            child = "https://example.test/child"
            processor = FakePageProcessor(
                {
                    start: ProcessedCrawlPage(
                        discovery_html='<a href="/child">Child</a>',
                        final_url=start,
                        download_size_bytes=120,
                        extraction_size_bytes=80,
                        extraction_collected=True,
                    ),
                    child: ProcessedCrawlPage(
                        discovery_html="<p>Child</p>",
                        final_url=child,
                        download_size_bytes=100,
                        extraction_size_bytes=60,
                        extraction_collected=True,
                    ),
                }
            )
            crawler = BFSCrawler(
                FakeFetcher({}),
                page_processor=processor,
                visited=VisitedURLDatabase(Path(temp_dir) / "visited.json"),
                max_depth=1,
                ignore_robots=True,
                rate_limiter=_unlimited_rate_limiter(),
            )

            stats = crawler.crawl(start)

            self.assertEqual(processor.calls, [start, child])
            self.assertEqual(stats.pages_visited, 2)
            self.assertEqual(stats.download_size_bytes, 220)
            self.assertEqual(stats.extraction_size_bytes, 140)
            self.assertTrue(stats.extraction_collected)

    def test_traverses_in_breadth_first_order_with_depth_limit(self) -> None:
        with TemporaryDirectory() as temp_dir:
            visited_path = Path(temp_dir) / "visited.json"
            pages = {
                "https://example.test/start": '<a href="/a">A</a><a href="/b">B</a>',
                "https://example.test/a": '<a href="/a/deep">A Deep</a>',
                "https://example.test/b": '<a href="/b/deep">B Deep</a>',
                "https://example.test/a/deep": "<p>A deep</p>",
                "https://example.test/b/deep": "<p>B deep</p>",
            }
            fetcher = FakeFetcher(pages)
            crawler = BFSCrawler(
                fetcher,
                visited=VisitedURLDatabase(visited_path),
                max_pages=10,
                max_depth=1,
                max_runtime_seconds=60,
                ignore_robots=True,
                rate_limiter=_unlimited_rate_limiter(),
            )

            stats = crawler.crawl("https://example.test/start")

            self.assertEqual(
                fetcher.calls,
                [
                    "https://example.test/start",
                    "https://example.test/a",
                    "https://example.test/b",
                ],
            )
            self.assertEqual(stats.pages_visited, 3)
            self.assertEqual(stats.max_depth_reached, 1)

    def test_stops_at_max_pages(self) -> None:
        with TemporaryDirectory() as temp_dir:
            visited_path = Path(temp_dir) / "visited.json"
            pages = {
                "https://example.test/start": '<a href="/a">A</a><a href="/b">B</a>',
                "https://example.test/a": "<p>A</p>",
                "https://example.test/b": "<p>B</p>",
            }
            fetcher = FakeFetcher(pages)
            crawler = BFSCrawler(
                fetcher,
                visited=VisitedURLDatabase(visited_path),
                max_pages=2,
                max_depth=3,
                max_runtime_seconds=60,
                ignore_robots=True,
                rate_limiter=_unlimited_rate_limiter(),
            )

            stats = crawler.crawl("https://example.test/start")

            self.assertEqual(stats.pages_visited, 2)
            self.assertEqual(stats.stop_reason, "max_pages")
            self.assertEqual(stats.queue_size_remaining, 1)

    def test_stops_at_max_runtime(self) -> None:
        with TemporaryDirectory() as temp_dir:
            visited_path = Path(temp_dir) / "visited.json"
            pages = {
                "https://example.test/start": '<a href="/a">A</a>',
                "https://example.test/a": "<p>A</p>",
            }
            fetcher = FakeFetcher(pages)
            clock = FakeClock([0.0, 0.0, 0.11, 0.11])
            crawler = BFSCrawler(
                fetcher,
                visited=VisitedURLDatabase(visited_path),
                max_pages=10,
                max_depth=3,
                max_runtime_seconds=0.1,
                time_provider=clock,
                ignore_robots=True,
                rate_limiter=_unlimited_rate_limiter(),
            )

            stats = crawler.crawl("https://example.test/start")

            self.assertEqual(stats.stop_reason, "max_runtime")
            self.assertEqual(stats.pages_visited, 1)

    def test_applies_delay_between_requests(self) -> None:
        with TemporaryDirectory() as temp_dir:
            visited_path = Path(temp_dir) / "visited.json"
            pages = {
                "https://example.test/start": '<a href="/a">A</a>',
                "https://example.test/a": "<p>A</p>",
            }
            fetcher = FakeFetcher(pages)
            sleep_calls: list[float] = []
            crawler = BFSCrawler(
                fetcher,
                visited=VisitedURLDatabase(visited_path),
                max_pages=10,
                max_depth=3,
                max_runtime_seconds=60,
                ignore_robots=True,
                rate_limiter=RateLimiter(
                    0.25,
                    jitter_min_seconds=0,
                    jitter_max_seconds=0,
                    clock=lambda: 0,
                    sleep=sleep_calls.append,
                ),
            )

            stats = crawler.crawl("https://example.test/start")

            self.assertEqual(stats.pages_visited, 2)
            self.assertEqual(sleep_calls, [0.25])

    def test_logs_every_page_visit(self) -> None:
        with TemporaryDirectory() as temp_dir:
            visited_path = Path(temp_dir) / "visited.json"
            pages = {
                "https://example.test/start": "<p>Start</p>",
            }
            fetcher = FakeFetcher(pages)
            crawler = BFSCrawler(
                fetcher,
                visited=VisitedURLDatabase(visited_path),
                max_pages=10,
                max_depth=0,
                max_runtime_seconds=60,
                ignore_robots=True,
                rate_limiter=_unlimited_rate_limiter(),
            )

            with self.assertLogs("knowledge_collector.crawler.bfs", level="INFO") as logs:
                stats = crawler.crawl("https://example.test/start")

            self.assertEqual(stats.pages_visited, 1)
            self.assertTrue(any("Visited page:" in message for message in logs.output))

    def test_blocks_disallowed_urls_before_downloading_them(self) -> None:
        with TemporaryDirectory() as temp_dir:
            start = "https://example.test/start"
            private = "https://example.test/private"
            fetcher = FakeFetcher(
                {
                    "https://example.test/robots.txt": "User-agent: *\nDisallow: /private\n",
                    start: '<a href="/private">Private</a>',
                    private: "<p>private</p>",
                }
            )
            crawler = BFSCrawler(
                fetcher,
                visited=VisitedURLDatabase(Path(temp_dir) / "visited.json"),
                max_depth=1,
                rate_limiter=_unlimited_rate_limiter(),
            )

            with self.assertLogs("knowledge_collector.crawler.robots", level="INFO") as logs:
                stats = crawler.crawl(start)

            self.assertEqual(stats.pages_visited, 1)
            self.assertNotIn(private, fetcher.calls)
            self.assertTrue(any("Allowed:" in message for message in logs.output))
            self.assertTrue(any("Blocked:" in message for message in logs.output))

    def test_recovers_from_interruption_without_revisiting_completed_pages(self) -> None:
        with TemporaryDirectory() as temp_dir:
            directory = Path(temp_dir)
            start = "https://example.test/start"
            first = "https://example.test/first"
            second = "https://example.test/second"
            checkpoint_path = directory / "crawl_checkpoint.json"
            visited_path = directory / "visited.json"

            class InterruptingFetcher(FakeFetcher):
                def download(self, url: str) -> str:
                    self.calls.append(url)
                    if url == first:
                        raise KeyboardInterrupt()
                    return self._pages[url]

            initial_fetcher = InterruptingFetcher(
                {
                    start: '<a href="/first">First</a><a href="/second">Second</a>',
                    first: "<p>First</p>",
                    second: "<p>Second</p>",
                }
            )
            initial = BFSCrawler(
                initial_fetcher,
                visited=VisitedURLDatabase(visited_path),
                max_depth=1,
                ignore_robots=True,
                rate_limiter=_unlimited_rate_limiter(),
                checkpoint_path=checkpoint_path,
            )

            with self.assertRaises(KeyboardInterrupt):
                initial.crawl(start)

            self.assertTrue(checkpoint_path.is_file())
            recovery_fetcher = FakeFetcher(
                {
                    start: '<a href="/first">First</a><a href="/second">Second</a>',
                    first: "<p>First</p>",
                    second: "<p>Second</p>",
                }
            )
            recovered = BFSCrawler(
                recovery_fetcher,
                visited=VisitedURLDatabase(visited_path),
                max_depth=1,
                ignore_robots=True,
                rate_limiter=_unlimited_rate_limiter(),
                checkpoint_path=checkpoint_path,
            )

            statistics = recovered.crawl(start, resume=True)

            self.assertEqual(recovery_fetcher.calls, [first, second])
            self.assertEqual(statistics.pages_visited, 3)
            self.assertFalse(checkpoint_path.exists())


if __name__ == "__main__":
    unittest.main()
