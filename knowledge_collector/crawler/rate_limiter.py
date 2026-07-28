"""Thread-safe request pacing for crawler network operations."""

from __future__ import annotations

import logging
import random
import threading
import time
from collections.abc import Callable


logger = logging.getLogger("knowledge_collector.crawler.rate_limiter")


class RateLimiter:
    """Ensure requests are separated by a delay plus random jitter.

    The first request proceeds immediately. Subsequent requests wait at least
    ``delay_seconds`` plus a jitter value between ``jitter_min_seconds`` and
    ``jitter_max_seconds``. Reservations are made under a lock, making one
    limiter safe to share among future concurrent crawler workers.
    """

    def __init__(
        self,
        delay_seconds: float = 1.0,
        *,
        jitter_min_seconds: float = 0.2,
        jitter_max_seconds: float = 0.8,
        clock: Callable[[], float] | None = None,
        sleep: Callable[[float], None] | None = None,
        random_uniform: Callable[[float, float], float] | None = None,
    ) -> None:
        if delay_seconds < 0:
            raise ValueError("delay_seconds cannot be negative")
        if jitter_min_seconds < 0 or jitter_max_seconds < jitter_min_seconds:
            raise ValueError("jitter bounds must be non-negative and ordered")

        self._delay_seconds = delay_seconds
        self._jitter_min_seconds = jitter_min_seconds
        self._jitter_max_seconds = jitter_max_seconds
        self._clock = clock or time.monotonic
        self._sleep = sleep or time.sleep
        self._random_uniform = random_uniform or random.uniform
        self._lock = threading.Lock()
        self._next_request_at: float | None = None

    def wait(self, url: str | None = None) -> None:
        """Wait until it is safe to issue the next request."""

        with self._lock:
            now = self._clock()
            scheduled_at = now if self._next_request_at is None else self._next_request_at
            wait_seconds = max(0.0, scheduled_at - now)
            interval = self._delay_seconds + self._random_uniform(
                self._jitter_min_seconds,
                self._jitter_max_seconds,
            )
            self._next_request_at = max(now, scheduled_at) + interval

        if wait_seconds > 0:
            logger.info("Waiting %.3f seconds before request%s", wait_seconds, f" to {url}" if url else "")
            self._sleep(wait_seconds)
