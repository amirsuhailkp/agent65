"""Unit tests for crawler request pacing."""

import unittest

from crawler.rate_limiter import RateLimiter


class RateLimiterTests(unittest.TestCase):
    def test_waits_for_delay_plus_jitter_and_logs_the_wait(self) -> None:
        clock_values = iter([0.0, 0.5])
        sleep_calls: list[float] = []
        jitter_bounds: list[tuple[float, float]] = []

        limiter = RateLimiter(
            delay_seconds=1.0,
            clock=lambda: next(clock_values),
            sleep=sleep_calls.append,
            random_uniform=lambda low, high: jitter_bounds.append((low, high)) or low,
        )

        limiter.wait("https://example.test/first")
        with self.assertLogs("knowledge_collector.crawler.rate_limiter", level="INFO") as logs:
            limiter.wait("https://example.test/second")

        self.assertEqual(jitter_bounds, [(0.2, 0.8), (0.2, 0.8)])
        self.assertEqual(sleep_calls, [0.7])
        self.assertTrue(any("Waiting 0.700 seconds" in message for message in logs.output))

    def test_allows_zero_delay_and_jitter_for_test_or_local_use(self) -> None:
        sleep_calls: list[float] = []
        limiter = RateLimiter(
            delay_seconds=0,
            jitter_min_seconds=0,
            jitter_max_seconds=0,
            clock=lambda: 0,
            sleep=sleep_calls.append,
        )

        limiter.wait()
        limiter.wait()

        self.assertEqual(sleep_calls, [])


if __name__ == "__main__":
    unittest.main()
