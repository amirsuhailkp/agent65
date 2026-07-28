"""Source collector abstractions and implementations."""

from .base import BaseCollector
from .crawler import WebsiteCrawler
from .owasp import OWASPCollector
from .portswigger import PortSwiggerCollector
from .single_page import SinglePageCollector

__all__ = ["BaseCollector", "OWASPCollector", "PortSwiggerCollector", "SinglePageCollector", "WebsiteCrawler"]
