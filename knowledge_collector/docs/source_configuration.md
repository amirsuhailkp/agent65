# Source Configuration (`config/sources.yaml`)

Every knowledge source the collector supports is declared in
`config/sources.yaml`. **Adding a new source requires editing only this
file** -- no Python changes, no new collector class. Every source with
`enabled: true` automatically appears as a `--source` choice in the CLI.

## Minimal example

```yaml
sources:
  - name: my-new-source
    display_name: My New Source
    enabled: true
    collector_type: blog_site
    category: web-security
    start_urls:
      - https://example.com/blog/
```

Any field not shown above falls back to a sensible default (see the field
reference below).

## Field reference

| Field | Type | Default | Meaning |
| --- | --- | --- | --- |
| `name` | string | *required* | Human-readable name. Slugified (lowercased, spaces -> `-`) to produce the CLI's `--source` value and the default output folder name. |
| `display_name` | string | `name` | Human-readable label used in CLI/report output. |
| `enabled` | bool | `true` | Whether this source appears in the CLI at all. |
| `collector_type` | string | `generic_html` | One of `generic_html`, `documentation_site`, `blog_site`, `api_docs`, `rss_feed`, `sitemap_site`. Determines how initial crawl seed URLs are resolved -- see below. |
| `category` | string | `uncategorized` | Default metadata category for collected pages (overridable per CLI invocation with `--category`). |
| `trust` | string | `medium` | One of `low`, `medium`, `high`. Informational; carried through to reports for downstream consumers. |
| `priority` | integer | `5` | Informational ordering hint for downstream consumers (lower = higher priority). |
| `output_directory` | string | source slug | Folder name under `raw/` and `processed/` for this source's artifacts, e.g. `raw/portswigger/`. |
| `start_urls` | list of strings | *required, non-empty* | Seed URL(s). Also used to derive the allowed hostname(s) for single-page URL validation. |
| `crawl_rules.listing_url_patterns` | list of strings | `[]` | Informational URL-shape hints for listing/hub pages. The page classifier does not require these -- it works from page structure -- but they are available to future collector-type refinements. |
| `crawl_rules.article_url_patterns` | list of strings | `[]` | Same, for article-shaped URLs. |
| `crawl_rules.ignore_url_patterns` | list of strings | `[]` | Same, for URLs that should never be queued (e.g. `/assets/`, `/cve-`). |
| `respect_robots` | bool | `true` | Whether robots.txt is honored for this source (the crawler-wide `IGNORE_ROBOTS` environment variable still overrides this globally). |
| `rate_limit_seconds` | float | `1.0` | Informational per-source delay hint; the crawler-wide `CRAWL_DELAY_SECONDS` setting is what's actually enforced today. |
| `max_pages` | integer | `500` | Default page limit for `site`/`resume` crawls of this source. **`0` means unlimited** -- the crawl then stops only when the queue is empty or robots.txt disallows further URLs. |
| `max_depth` | integer | `3` | Default crawl depth for this source. When `max_pages: 0` and the CLI's `--max-depth` is not explicitly set, this is overridden with an effectively unbounded depth so page count, not depth, is the limiting factor. |
| `use_playwright` | string | `auto` | One of `auto`, `always`, `never`. `auto` (current behavior) retries extraction with Playwright only when requests-based extraction looks suspiciously small. If Playwright is not installed, a warning is logged once and the crawl continues using requests-only HTML. |

## Collector types and seeding

All collector types share the same downstream pipeline (download, classify,
extract, convert, clean, store). They differ only in how a source's initial
crawl seeds are resolved from `start_urls`:

- **`generic_html` / `documentation_site` / `blog_site` / `api_docs`** --
  `start_urls` are used directly as crawl seeds; further pages are discovered
  by following links (this is the "normal" case; use `documentation_site` or
  `blog_site` mainly for readability/reporting purposes, since the crawl
  behavior is identical).
- **`sitemap_site`** -- each `start_urls` entry is fetched and parsed as a
  sitemap XML document; every `<loc>` becomes a seed URL. Falls back to the
  raw `start_urls` if parsing fails.
- **`rss_feed`** -- each `start_urls` entry is fetched and parsed as an
  RSS/Atom feed; every `<link>` becomes a seed URL. Falls back to the raw
  `start_urls` if parsing fails.

## Backward compatibility

The pre-upgrade minimal schema is still accepted and mapped onto the fields
above automatically:

```yaml
sources:
  - name: OldStyleSource
    type: crawler
    url: https://example.com/start
    output: raw_documents/old-style-source/
```

is equivalent to:

```yaml
sources:
  - name: OldStyleSource
    start_urls: ["https://example.com/start"]
    output_directory: old-style-source
```

## Validation

`SourceRegistry.load()` (`config/sources.py`) validates the file at CLI
startup and raises `SourceConfigError` with a specific message for:
missing/empty `sources` list, duplicate source names, invalid
`collector_type`/`trust`/`use_playwright` values, missing/empty
`start_urls`, and negative `max_pages`/`max_depth`/`rate_limit_seconds`.
