"""Reusable ``robots.txt`` policy support for crawlers.

Policies are fetched lazily, once per origin, through the crawler's existing
download boundary.  This keeps network configuration and tests in one place.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from urllib.parse import urlsplit
from urllib.robotparser import RobotFileParser


logger = logging.getLogger("knowledge_collector.crawler.robots")


class RobotsPolicy:
    """Evaluate a URL against its origin's downloaded ``robots.txt`` file.

    Args:
        download: Callable used to retrieve a URL as text.
        user_agent: Crawler user-agent matched against robots directives.
        ignore_robots: When true, permit all URLs without fetching robots files.
    """

    def __init__(
        self,
        download: Callable[[str], str],
        *,
        user_agent: str = "*",
        ignore_robots: bool = False,
    ) -> None:
        if not user_agent.strip():
            raise ValueError("user_agent cannot be empty")
        self._download = download
        self._user_agent = user_agent
        self._ignore_robots = ignore_robots
        self._policies: dict[str, RobotFileParser | None] = {}

    def can_fetch(self, url: str) -> bool:
        """Return whether the configured crawler may download ``url``."""

        if self._ignore_robots:
            logger.info("Allowed: %s (robots.txt ignored)", url)
            return True

        origin = _origin(url)
        if origin is None:
            raise ValueError("url must be an absolute HTTP(S) URL")
        if origin not in self._policies:
            self._policies[origin] = self._download_policy(origin)

        policy = self._policies[origin]
        allowed = policy is None or policy.can_fetch(self._user_agent, url)
        logger.info("%s: %s", "Allowed" if allowed else "Blocked", url)
        return allowed

    def _download_policy(self, origin: str) -> RobotFileParser | None:
        robots_url = f"{origin}/robots.txt"
        try:
            content = self._download(robots_url)
        except Exception as exc:
            # An unavailable robots file is treated as absent, as specified by
            # the robots exclusion protocol's usual crawler behaviour.
            logger.info("Missing robots.txt: %s (%s)", robots_url, exc)
            return None

        parser = RobotFileParser()
        parser.set_url(robots_url)
        parser.parse(content.splitlines())
        return parser


def _origin(url: str) -> str | None:
    parsed = urlsplit(url)
    if parsed.scheme.casefold() not in {"http", "https"} or not parsed.netloc:
        return None
    return f"{parsed.scheme.casefold()}://{parsed.netloc}"
