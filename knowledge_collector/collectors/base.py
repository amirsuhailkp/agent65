"""Abstract contract for knowledge-source collectors."""

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Any


class BaseCollector(ABC):
    """Defines the source-facing boundary for all collectors.

    Concrete collectors own source-specific discovery only. Downloading,
    extraction, cleaning, metadata, and persistence remain separate concerns.
    """

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Return the stable identifier for this knowledge source."""

    @abstractmethod
    def discover(self) -> Iterable[dict[str, Any]]:
        """Declare the contract for discovering source items.

        Implementations will be introduced in a later phase.
        """
