"""Configuration-driven knowledge source registry.

Replaces the CLI's hardcoded ``owasp``/``portswigger`` options. Every
*enabled* source declared in ``config/sources.yaml`` automatically becomes
available to the CLI; adding a new source requires editing only that YAML
file, never Python code.

Backward compatibility: the pre-upgrade file format (``name``/``type``/
``url``/``output``) is still accepted and mapped onto the richer schema
below, so an existing ``sources.yaml`` keeps working unmodified.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlsplit

import yaml


logger = logging.getLogger("knowledge_collector.config.sources")

DEFAULT_SOURCES_PATH = Path(__file__).resolve().parent / "sources.yaml"

#: Collector types a source may choose in YAML. See ``collectors/generic.py``
#: for what each type actually does with a source's start URLs.
VALID_COLLECTOR_TYPES = frozenset(
    {
        "generic_html",
        "documentation_site",
        "blog_site",
        "api_docs",
        "rss_feed",
        "sitemap_site",
    }
)
VALID_TRUST_LEVELS = frozenset({"low", "medium", "high"})
VALID_PLAYWRIGHT_MODES = frozenset({"auto", "always", "never"})

_UNLIMITED = 0


class SourceConfigError(ValueError):
    """Raised when ``sources.yaml`` is missing required or valid fields."""


@dataclass(frozen=True, slots=True)
class CrawlRules:
    """Source-specific URL shape hints that stay in configuration, not code."""

    listing_url_patterns: tuple[str, ...] = ()
    article_url_patterns: tuple[str, ...] = ()
    ignore_url_patterns: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class SourceConfig:
    """Everything needed to crawl and collect one knowledge source.

    ``name`` is the stable CLI-facing slug (e.g. ``"portswigger"``);
    ``display_name`` is only for human-readable output/reports.
    """

    name: str
    display_name: str
    enabled: bool = True
    collector_type: str = "generic_html"
    category: str = "uncategorized"
    trust: str = "medium"
    priority: int = 5
    output_directory: str = ""
    start_urls: tuple[str, ...] = ()
    crawl_rules: CrawlRules = field(default_factory=CrawlRules)
    respect_robots: bool = True
    rate_limit_seconds: float = 1.0
    max_pages: int = 500
    max_depth: int = 3
    use_playwright: str = "auto"

    @property
    def slug(self) -> str:
        """Return the folder-safe identifier used under ``raw/`` and ``processed/``."""

        return self.output_directory or self.name

    @property
    def is_unlimited_pages(self) -> bool:
        return self.max_pages == _UNLIMITED

    def allowed_hostnames(self) -> frozenset[str]:
        """Return the root hostnames this source's start URLs belong to.

        Used for domain validation on the ``collect`` (single-page) command
        without hardcoding a root domain per collector class.
        """

        hostnames = set()
        for url in self.start_urls:
            hostname = urlsplit(url).hostname
            if hostname:
                hostnames.add(hostname.casefold().removeprefix("www."))
        return frozenset(hostnames)


class SourceRegistry:
    """Load and expose configured knowledge sources."""

    def __init__(self, sources: tuple[SourceConfig, ...]) -> None:
        self._sources = {source.name: source for source in sources}
        self._order = tuple(source.name for source in sources)

    @classmethod
    def load(cls, path: Path | None = None) -> "SourceRegistry":
        """Load and validate all sources declared in ``sources.yaml``."""

        resolved_path = path or DEFAULT_SOURCES_PATH
        try:
            raw_text = resolved_path.read_text(encoding="utf-8")
        except OSError as exc:
            raise SourceConfigError(f"could not read source configuration: {resolved_path}") from exc

        try:
            document = yaml.safe_load(raw_text) or {}
        except yaml.YAMLError as exc:
            raise SourceConfigError(f"invalid YAML in {resolved_path}: {exc}") from exc

        raw_sources = document.get("sources")
        if not isinstance(raw_sources, list) or not raw_sources:
            raise SourceConfigError(f"{resolved_path} must declare a non-empty 'sources' list")

        sources = tuple(_parse_source(entry) for entry in raw_sources)
        names = [source.name for source in sources]
        duplicates = {name for name in names if names.count(name) > 1}
        if duplicates:
            raise SourceConfigError(f"duplicate source name(s) in {resolved_path}: {sorted(duplicates)}")

        logger.info("Loaded %s source(s) from %s (%s enabled)", len(sources), resolved_path, sum(s.enabled for s in sources))
        return cls(sources)

    def get(self, name: str) -> SourceConfig:
        """Return the named source, raising ``KeyError`` if it is unknown."""

        try:
            return self._sources[name]
        except KeyError:
            raise KeyError(
                f"unknown source: {name!r} (available: {', '.join(self.enabled_names()) or 'none'})"
            ) from None

    def enabled_sources(self) -> tuple[SourceConfig, ...]:
        """Return enabled sources in the order declared in YAML."""

        return tuple(self._sources[name] for name in self._order if self._sources[name].enabled)

    def enabled_names(self) -> tuple[str, ...]:
        """Return enabled source names; this is what populates the CLI's ``--source`` choices."""

        return tuple(source.name for source in self.enabled_sources())

    def all_sources(self) -> tuple[SourceConfig, ...]:
        return tuple(self._sources[name] for name in self._order)


def _parse_source(entry: object) -> SourceConfig:
    if not isinstance(entry, dict):
        raise SourceConfigError(f"each source must be a mapping, got: {entry!r}")

    entry = dict(entry)  # avoid mutating caller's parsed document
    _migrate_legacy_fields(entry)

    name = _require_str(entry, "name")
    slug = _slugify(name)
    collector_type = str(entry.get("collector_type", "generic_html"))
    if collector_type not in VALID_COLLECTOR_TYPES:
        raise SourceConfigError(
            f"source {name!r} has invalid collector_type {collector_type!r}; "
            f"expected one of {sorted(VALID_COLLECTOR_TYPES)}"
        )

    trust = str(entry.get("trust", "medium"))
    if trust not in VALID_TRUST_LEVELS:
        raise SourceConfigError(f"source {name!r} has invalid trust {trust!r}; expected one of {sorted(VALID_TRUST_LEVELS)}")

    use_playwright = str(entry.get("use_playwright", "auto"))
    if use_playwright not in VALID_PLAYWRIGHT_MODES:
        raise SourceConfigError(
            f"source {name!r} has invalid use_playwright {use_playwright!r}; "
            f"expected one of {sorted(VALID_PLAYWRIGHT_MODES)}"
        )

    start_urls = tuple(_require_list_of_str(entry, "start_urls", name))
    if not start_urls:
        raise SourceConfigError(f"source {name!r} must declare at least one start URL")

    crawl_rules_raw = entry.get("crawl_rules") or {}
    if not isinstance(crawl_rules_raw, dict):
        raise SourceConfigError(f"source {name!r} has an invalid crawl_rules mapping")
    crawl_rules = CrawlRules(
        listing_url_patterns=tuple(crawl_rules_raw.get("listing_url_patterns", []) or []),
        article_url_patterns=tuple(crawl_rules_raw.get("article_url_patterns", []) or []),
        ignore_url_patterns=tuple(crawl_rules_raw.get("ignore_url_patterns", []) or []),
    )

    max_pages = int(entry.get("max_pages", 500))
    if max_pages < 0:
        raise SourceConfigError(f"source {name!r} has negative max_pages; use 0 for unlimited")
    max_depth = int(entry.get("max_depth", 3))
    if max_depth < 0:
        raise SourceConfigError(f"source {name!r} has negative max_depth")
    rate_limit_seconds = float(entry.get("rate_limit_seconds", 1.0))
    if rate_limit_seconds < 0:
        raise SourceConfigError(f"source {name!r} has negative rate_limit_seconds")
    priority = int(entry.get("priority", 5))

    return SourceConfig(
        name=slug,
        display_name=str(entry.get("display_name", name)),
        enabled=bool(entry.get("enabled", True)),
        collector_type=collector_type,
        category=str(entry.get("category", "uncategorized")),
        trust=trust,
        priority=priority,
        output_directory=str(entry.get("output_directory") or slug),
        start_urls=start_urls,
        crawl_rules=crawl_rules,
        respect_robots=bool(entry.get("respect_robots", True)),
        rate_limit_seconds=rate_limit_seconds,
        max_pages=max_pages,
        max_depth=max_depth,
        use_playwright=use_playwright,
    )


def _migrate_legacy_fields(entry: dict) -> None:
    """Map the pre-upgrade minimal schema onto the current field names in place."""

    if "start_urls" not in entry and "url" in entry:
        entry["start_urls"] = [entry["url"]]
    if "output_directory" not in entry and "output" in entry:
        # Historical values looked like "raw_documents/owasp/"; keep only the
        # trailing folder segment as the new per-source slug.
        legacy_output = str(entry["output"]).strip("/")
        entry["output_directory"] = legacy_output.rsplit("/", 1)[-1] if legacy_output else None
    entry.pop("type", None)
    entry.pop("url", None)
    entry.pop("output", None)


def _require_str(entry: dict, key: str) -> str:
    value = entry.get(key)
    if not isinstance(value, str) or not value.strip():
        raise SourceConfigError(f"source entry is missing a non-empty '{key}': {entry!r}")
    return value.strip()


def _require_list_of_str(entry: dict, key: str, name: str) -> list[str]:
    value = entry.get(key, [])
    if isinstance(value, str):
        value = [value]
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        raise SourceConfigError(f"source {name!r} field '{key}' must be a list of non-empty strings")
    return [item.strip() for item in value]


def _slugify(name: str) -> str:
    return "".join(character for character in name.casefold().replace(" ", "-") if character.isalnum() or character == "-").strip("-") or "source"
