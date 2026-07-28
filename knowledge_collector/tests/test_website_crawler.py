"""Unit tests for checkpointed same-domain URL discovery."""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from collectors.crawler import WebsiteCrawler
from crawler.rate_limiter import RateLimiter


class FakeFetcher:
    def __init__(self, pages: dict[str, str]) -> None:
        self.pages = pages
        self.calls: list[str] = []

    def download(self, url: str) -> str:
        self.calls.append(url)
        return self.pages[url]


def _unlimited_rate_limiter() -> RateLimiter:
    return RateLimiter(0, jitter_min_seconds=0, jitter_max_seconds=0)


class WebsiteCrawlerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = TemporaryDirectory()
        self.queue_path = Path(self.temporary_directory.name) / "crawl_queue.json"
        self.visited_path = Path(self.temporary_directory.name) / "visited_urls.json"

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_discovers_internal_html_urls_with_depth_and_file_filters(self) -> None:
        start = "https://docs.example.test/start"
        pages = {
            start: """
                <a href="/guide">Guide</a><a href="/asset.pdf">PDF</a>
                <a href="https://other.example.test/page">External</a>
            """,
            "https://docs.example.test/guide": '<a href="/deep">Deep</a>',
            "https://docs.example.test/deep": "<p>Deep</p>",
        }
        crawler = WebsiteCrawler(
            FakeFetcher(pages),
            max_depth=1,
            queue_path=self.queue_path,
            visited_path=self.visited_path,
            respect_robots=False,
            rate_limiter=_unlimited_rate_limiter(),
        )

        urls = crawler.crawl(start)

        self.assertEqual(urls, [start, "https://docs.example.test/guide"])
        self.assertTrue(self.queue_path.is_file())

    def test_resume_restores_pending_queue(self) -> None:
        start = "https://docs.example.test/start"
        pages = {
            start: '<a href="/next">Next</a>',
            "https://docs.example.test/next": "<p>Next</p>",
        }
        first_run = WebsiteCrawler(
            FakeFetcher(pages),
            max_pages=1,
            queue_path=self.queue_path,
            visited_path=self.visited_path,
            respect_robots=False,
            rate_limiter=_unlimited_rate_limiter(),
        )
        self.assertEqual(first_run.crawl(start), [start])

        resumed = WebsiteCrawler(
            FakeFetcher(pages),
            max_pages=10,
            queue_path=self.queue_path,
            visited_path=self.visited_path,
            respect_robots=False,
            rate_limiter=_unlimited_rate_limiter(),
        )
        self.assertEqual(resumed.crawl(start, resume=True), [start, "https://docs.example.test/next"])

    def test_honors_robots_disallow_rules(self) -> None:
        start = "https://docs.example.test/start"
        robots = "https://docs.example.test/robots.txt"
        secret = "https://docs.example.test/private"
        fetcher = FakeFetcher(
            {
                robots: "User-agent: *\nDisallow: /private\n",
                start: '<a href="/private">Private</a>',
                secret: "<p>Should not be fetched</p>",
            }
        )
        crawler = WebsiteCrawler(
            fetcher,
            queue_path=self.queue_path,
            visited_path=self.visited_path,
            rate_limiter=_unlimited_rate_limiter(),
        )

        self.assertEqual(crawler.crawl(start), [start])
        self.assertNotIn(secret, fetcher.calls)

    def test_automatically_persists_visited_urls_between_runs(self) -> None:
        start = "https://docs.example.test/start"
        page = "https://docs.example.test/page"
        visited_path = Path(self.temporary_directory.name) / "visited_urls.json"

        first_fetcher = FakeFetcher(
            {
                start: '<a href="/page">Page</a>',
                page: "<p>Page</p>",
            }
        )
        first_run = WebsiteCrawler(
            first_fetcher,
            queue_path=self.queue_path,
            visited_path=visited_path,
            respect_robots=False,
            rate_limiter=_unlimited_rate_limiter(),
        )

        self.assertEqual(first_run.crawl(start), [start, page])
        self.assertTrue(visited_path.is_file())

        second_fetcher = FakeFetcher(
            {
                start: '<a href="/page">Page</a>',
                page: "<p>Page</p>",
            }
        )
        second_run = WebsiteCrawler(
            second_fetcher,
            queue_path=self.queue_path,
            visited_path=visited_path,
            respect_robots=False,
            rate_limiter=_unlimited_rate_limiter(),
        )

        self.assertEqual(second_run.crawl(start), [])
        self.assertEqual(second_fetcher.calls, [])
