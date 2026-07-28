"""Safe filesystem persistence for raw and processed collection artifacts."""

import logging
import re
from pathlib import Path
from typing import Literal

from config.settings import settings


logger = logging.getLogger("knowledge_collector.storage")

StorageArea = Literal["raw", "processed"]
_INVALID_FILENAME_CHARACTERS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
_WINDOWS_RESERVED_NAMES = frozenset(
    {"CON", "PRN", "AUX", "NUL", *(f"COM{number}" for number in range(1, 10)), *(f"LPT{number}" for number in range(1, 10))}
)
_MAX_FILENAME_LENGTH = 200


class StorageError(RuntimeError):
    """Raised when an artifact cannot be saved to the filesystem."""


class FilesystemStorage:
    """Persist collection artifacts using validated, non-overwriting filenames."""

    def __init__(self, base_directory: Path | None = None) -> None:
        self._base_directory = (base_directory or settings.project_root).resolve()
        self._directories = {
            "raw": self._base_directory / "raw",
            "processed": self._base_directory / "processed",
        }
        self._ensure_directories()

    def save_raw(self, content: str | bytes, filename: str, *, subdirectory: str | None = None) -> Path:
        """Save raw source content and return its unique filesystem path.

        ``subdirectory`` (e.g. a source slug such as ``"portswigger"``) keeps
        each knowledge source in its own folder under ``raw/``. Omitting it
        preserves the historical flat layout for existing callers.
        """

        return self._save(content, filename, "raw", subdirectory=subdirectory)

    def save_processed(self, content: str | bytes, filename: str, *, subdirectory: str | None = None) -> Path:
        """Save processed content and return its unique filesystem path."""

        return self._save(content, filename, "processed", subdirectory=subdirectory)

    def _save(
        self,
        content: str | bytes,
        filename: str,
        area: StorageArea,
        *,
        subdirectory: str | None = None,
    ) -> Path:
        if not isinstance(content, (str, bytes)):
            raise TypeError("content must be str or bytes")

        safe_filename = validate_filename(filename)
        directory = self._directories[area]
        if subdirectory:
            directory = directory / _validate_subdirectory(subdirectory)
        directory.mkdir(parents=True, exist_ok=True)

        version = 0
        while True:
            candidate = directory / _versioned_filename(safe_filename, version)
            try:
                _write_exclusively(candidate, content)
            except FileExistsError:
                version += 1
                continue
            except OSError as exc:
                logger.exception("Unable to save %s artifact to %s", area, candidate)
                raise StorageError(f"unable to save {area} artifact: {candidate.name}") from exc

            logger.info("Saved %s artifact to %s", area, candidate)
            return candidate

    def _ensure_directories(self) -> None:
        for directory in self._directories.values():
            try:
                directory.mkdir(parents=True, exist_ok=True)
            except OSError as exc:
                logger.exception("Unable to create storage directory %s", directory)
                raise StorageError(f"unable to create storage directory: {directory}") from exc


def validate_filename(filename: str) -> str:
    """Validate a portable basename and reject paths, traversal, and reserved names."""

    if not isinstance(filename, str):
        raise TypeError("filename must be a string")
    if not filename or not filename.strip():
        raise ValueError("filename cannot be empty")
    if len(filename) > _MAX_FILENAME_LENGTH:
        raise ValueError(f"filename cannot exceed {_MAX_FILENAME_LENGTH} characters")
    if Path(filename).name != filename or "/" in filename or "\\" in filename:
        raise ValueError("filename must be a basename, not a path")
    if filename in {".", ".."} or filename.endswith((".", " ")):
        raise ValueError("filename cannot be a dot path or end in a space/dot")
    if _INVALID_FILENAME_CHARACTERS.search(filename):
        raise ValueError("filename contains invalid filesystem characters")

    stem = filename.split(".", maxsplit=1)[0].upper()
    if stem in _WINDOWS_RESERVED_NAMES:
        raise ValueError("filename uses a Windows-reserved device name")
    return filename


def _validate_subdirectory(subdirectory: str) -> str:
    """Validate a single-segment, traversal-safe source folder name."""

    if not isinstance(subdirectory, str) or not subdirectory.strip():
        raise ValueError("subdirectory cannot be empty")
    if Path(subdirectory).name != subdirectory or "/" in subdirectory or "\\" in subdirectory:
        raise ValueError("subdirectory must be a single path segment")
    if subdirectory in {".", ".."}:
        raise ValueError("subdirectory cannot be a dot path")
    return subdirectory


def _versioned_filename(filename: str, version: int) -> str:
    if version == 0:
        return filename
    path = Path(filename)
    return f"{path.stem} ({version}){path.suffix}"


def _write_exclusively(path: Path, content: str | bytes) -> None:
    """Atomically create a file, failing rather than replacing an existing file."""

    if isinstance(content, bytes):
        with path.open("xb") as artifact:
            artifact.write(content)
        return
    with path.open("x", encoding="utf-8", newline="\n") as artifact:
        artifact.write(content)
