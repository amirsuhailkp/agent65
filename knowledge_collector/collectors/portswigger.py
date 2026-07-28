"""Single-page PortSwigger knowledge collector."""

from .single_page import SinglePageCollector, validate_source_url


class PortSwiggerCollector(SinglePageCollector):
    """Collect one PortSwigger page using the shared single-page pipeline.

    The inherited empty ``discover`` method is a deliberate extension point for
    a future source-specific crawler; this implementation processes only an
    explicitly supplied URL.
    """

    default_category = "web-security"

    @property
    def source_name(self) -> str:
        return "portswigger"

    def _validate_source_url(self, url: str) -> None:
        validate_source_url(
            url,
            root_domain="portswigger.net",
            collector_name="PortSwiggerCollector",
        )
