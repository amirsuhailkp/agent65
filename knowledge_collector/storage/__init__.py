"""Filesystem persistence services for collection artifacts."""

from .filesystem import FilesystemStorage, StorageError

__all__ = ["FilesystemStorage", "StorageError"]
