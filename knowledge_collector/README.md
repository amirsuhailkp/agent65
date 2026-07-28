# Knowledge Collector Framework

Production-oriented project scaffold for Agent Cyber knowledge collection. This
initial version deliberately contains no downloading, parsing, cleaning, or
persistence business logic.

## Requirements

- Python 3.12+

## Setup

```powershell
cd knowledge_collector
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install chromium
python main.py
```

The entry point initializes console and file logging. Logs are written to
`logs/knowledge_collector.log`.

## Architecture

- `config/`: immutable runtime paths plus `sources.py`/`sources.yaml`, the
  dynamic, YAML-driven source registry (see "Configuration-driven sources").
- `collectors/`: source-facing abstractions; `BaseCollector` isolates source
  discovery from later processing stages. `collectors/generic.py` implements
  the shared `crawl()`/`download()`/`extract_links()`/`extract_content()`
  interface used by every configuration-driven source.
- `downloader/`, `extractor/`, `cleaner/`, `metadata/`, `storage/`: separate
  extension boundaries, preserving single responsibility.
- `logger/`: central, idempotent logging setup.
- `utils/`: shared helpers when needed.
- `raw/`, `processed/`, `logs/`: runtime data and log locations.
- `tests/`: automated-test package.

## Extension guidance

Implement a collector by subclassing `BaseCollector` and implementing
`source_name` plus `discover`. Keep source discovery independent from download,
transformation, metadata, and storage implementations. In practice, most new
sources need no new collector class at all -- see "Configuration-driven
sources" below.

## Configuration-driven sources

Every source the collector crawls is declared in `config/sources.yaml`.
**Adding a new source requires editing only that file** -- every source with
`enabled: true` automatically becomes a `--source` choice in the CLI. See
[docs/source_configuration.md](docs/source_configuration.md) for the full
field reference, and the file itself for working OWASP, PortSwigger,
HackTricks, ProjectDiscovery, and Assetnote examples.

```powershell
python main.py collect --source hacktricks --url https://book.hacktricks.wiki/some-page
python main.py site --source assetnote --url https://blog.assetnote.io/ --max-pages 0
```

Collector types (`generic_html`, `documentation_site`, `blog_site`,
`api_docs`, `rss_feed`, `sitemap_site`) share one common interface --
`crawl()`, `download()`, `extract_links()`, `extract_content()` -- in
`collectors/generic.py`; only seeding differs (plain HTML start pages vs.
parsing a sitemap or RSS feed into individual URLs).

## Page classification

The crawler no longer assumes every page is an article. `PageClassifier`
(`crawler/classifier.py`) scores each downloaded page as Listing, Article,
Documentation, Index, or Unknown using only structural and URL-shape signals
(link density, heading density, breadcrumbs, `<article>`/`<main>` presence,
card-grid link patterns) -- no site is hardcoded, so the same logic works for
OWASP, PortSwigger, HackTricks, ProjectDiscovery, Assetnote, and future
sources. Listing/Index pages have their links queued but are never sent to
extraction (this is what fixes crawls of hub pages such as
`https://portswigger.net/research`); Article/Documentation pages are
quality-scored (`crawler/content_quality.py`) instead of gated by one fixed
character minimum, deduplicated by content hash (`crawler/dedup.py`), and
saved as Markdown; Unknown pages are skipped safely. See
[docs/architecture.md](docs/architecture.md#page-classification) for the full
data flow.

## Unlimited and incremental crawling

Pass `--max-pages 0` to crawl an entire site without an arbitrary page cap;
the crawl then stops only when the queue is empty or robots.txt disallows
further URLs, and depth is automatically treated as effectively unbounded
too unless `--max-depth` is set explicitly. `crawler/incremental.py`
(`PageMetadataStore`) and the downloader's new conditional-request support
(`Downloader.download_document(url, conditional_headers=...)`, which raises
`NotModifiedError` on HTTP 304) provide the building blocks for future
changed-only recrawls of a source.

## Downloader

`Downloader` retrieves HTML only. It uses `requests`, follows redirects, sends
a configurable `User-Agent`, applies a configurable timeout, and retries common
temporary HTTP/network failures. HTTP and network failures are logged and
raised as `DownloaderError`.

## Extractor

`HTMLExtractor` accepts raw HTML and returns only the article HTML. It uses
Trafilatura first, retaining tables, links, and formatting; if that produces no
usable result or fails, it falls back to a BeautifulSoup structural extraction.
The fallback removes navigation, sidebars, footers, ads, cookie banners, menus,
and non-content document elements while preserving headings, paragraphs, lists,
tables, and code blocks.

When extraction from requests-downloaded HTML is suspiciously small, the
workflow can optionally retry extraction using Playwright-rendered HTML after a
`networkidle` page load. The requests downloader remains the primary path, and
Playwright runs only when needed.

## Markdown conversion

`MarkdownConverter` converts the extractor's cleaned HTML to Markdown. It
preserves headings, lists, tables, fenced code blocks, links, and images, while
pruning empty article sections before conversion.

## Markdown cleaning

`MarkdownCleaner` removes website boilerplate after conversion while leaving
fenced code blocks untouched. It strips base64 images, HTML comments, JavaScript
remnants, navigation-only link rows, donation/edit links, cookie notices, and
excess blank-line or trailing-whitespace noise. It also normalizes ATX heading
spacing without changing heading levels.

## Metadata generation

`MetadataGenerator` prepends valid YAML front matter to cleaned Markdown. It
derives the title from the first article heading, extracts the source domain from
the canonical URL, records the collector and a UTC collection timestamp, and
generates deterministic keyword tags from article text. Existing front matter is
replaced to avoid duplicate metadata blocks.

## Filesystem storage

`FilesystemStorage` saves raw and processed artifacts under `raw/` and
`processed/`. It creates those directories automatically, validates portable
filenames to block paths and unsafe names, and writes with exclusive creation.
When a name already exists, it saves a versioned filename such as
`article (1).md` rather than overwriting the existing artifact.

## OWASP single-page collector

`OWASPCollector.collect(url)` coordinates one OWASP URL only. It downloads the
page, extracts its article HTML, converts and cleans Markdown, prepends metadata,
then saves the raw HTML and final Markdown. The collector accepts only
`owasp.org` subdomains, returns the saved processed path, and has no crawling or
URL-discovery behavior.

## PortSwigger single-page collector

`PortSwiggerCollector.collect(url)` uses the same reusable single-page pipeline
as OWASP, with PortSwigger URL validation and source metadata. Both collectors
inherit `SinglePageCollector`, which centralizes processing and persistence while
leaving `discover()` empty as a future crawling extension point.

## CLI

Run the interactive menu with `python main.py`, then choose a source (every
enabled entry from `config/sources.yaml` is listed) and **Single URL**. The
command-line equivalent is:

```powershell
python main.py collect --source owasp --url https://owasp.org/www-project-top-ten/ --language en
```

The CLI reports progress through configured console logging, displays the
saved processed Markdown path (under `processed/<source>/`), and returns
clear errors with non-zero exit codes.

## Debug mode

Set `DEBUG=true` to capture one-run diagnostics for extraction failures:

```powershell
$env:DEBUG = "true"
python main.py collect --source owasp --url https://owasp.org/www-project-top-ten/
```

When enabled, the workflow writes these files under `logs/`:

- `raw_response.html`
- `cleaned_article.html`
- `extracted_markdown.md`
- `metadata.json`
- `redirect_history.json`
- `download_headers.json`

It also logs response headers, content type, encoding, redirect chain,
extraction statistics, markdown size, and cleaning statistics. With
`DEBUG=false` (default), none of these debug artifacts are written.

## Website crawler

`BFSCrawler` performs breadth-first, same-site collection from one start URL.
For every queued page it runs the shared collection workflow (download,
extract, convert, clean, generate metadata, and store) before discovering and
filtering the next links. Completed URLs are persisted only after both raw HTML
and processed Markdown are saved. Checkpoints and the visited database allow a
run to resume without repeating completed pages. Set `IGNORE_ROBOTS=true` (or
pass `ignore_robots=True` to a crawler) only when robots policy should be
bypassed.

Crawler requests are paced by default: after the first request, each request is
delayed by `CRAWL_DELAY_SECONDS` (default `1`) plus a random `0.2`–`0.8` second
jitter. This applies to both page and `robots.txt` requests.

Interactive crawls display the current URL, page and queue counts, depth,
elapsed time, and an ETA in the terminal. Each progress snapshot is also saved
to `logs/crawl.log`.

`BFSCrawler` saves an atomic `logs/crawl_checkpoint.json` snapshot after each
state change. If a run is interrupted, call `crawl(start_url, resume=True)` to
continue from the pending queue without downloading completed pages again.

## Entire-site CLI crawl

Run an entire-site crawl non-interactively with:

```powershell
python main.py site --source portswigger --url https://portswigger.net/research --max-pages 100 --max-depth 2
python main.py site --source hacktricks --url https://book.hacktricks.wiki/ --max-pages 0
```

The interactive menu offers the same flow: choose **Entire Site**, then supply
the starting URL, maximum pages (`0` for unlimited), and maximum crawl depth.
The CLI validates the source's configured domain(s), creates per-site state
under `logs/crawls/`, and delegates to `BFSCrawler` through a
`ClassifyingCrawlPageProcessor`. Every page is classified before extraction
(see "Page classification" above), so listing/hub pages have their links
queued instead of causing extraction failures. The crawler composes the
existing page workflow with URL discovery/domain filtering, robots policy,
content-hash deduplication, progress reporting, persistent visited URLs, and
atomic resume checkpoints. Raw HTML and Markdown are saved per source under
`raw/<source>/` and `processed/<source>/`.

The CLI writes `crawl_results.json` (completed URLs), `crawl_summary.json`
(run metrics), `crawl_statistics.json` (the full statistics record),
`failed_urls.json`, `skipped_urls.json` (with per-URL skip reasons --
`unknown_page_type`, `low_quality_content`, `duplicate_content`, or
`extraction_rejected`), and dashboard-ready `crawl_report.json` /
`crawl_report.md`. Extraction-size metrics are measured from extracted
article HTML. See [architecture documentation](docs/architecture.md) for
component boundaries.

## Integrated workflow

All source collectors delegate URL processing to `CollectionWorkflow`. It is
constructed from narrow interfaces for downloading, extraction, conversion,
cleaning, metadata generation, and storage, so each component remains
independently replaceable. See [the architecture diagram](docs/architecture.md)
for the complete data flow and reserved future extension points for chunking,
embedding generation, and ChromaDB.

Run the isolated unit tests with:

```powershell
python -m unittest discover -s tests
```
