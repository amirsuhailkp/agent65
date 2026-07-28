"""Single-page OWASP knowledge collector."""

from .single_page import SinglePageCollector, validate_source_url


class OWASPCollector(SinglePageCollector):
    """Collect one OWASP page using the shared single-page pipeline."""

    default_category = "web-security"

    @property
    def source_name(self) -> str:
        return "owasp"

    def _validate_source_url(self, url: str) -> None:
        validate_source_url(url, root_domain="owasp.org", collector_name="OWASPCollector")
