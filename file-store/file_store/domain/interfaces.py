"""Порты (абстракции), используемые application-слоем."""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Protocol, runtime_checkable
from uuid import UUID

from file_store.domain.entities.stored_file import StoredFile


@runtime_checkable
class FileRepository(Protocol):
    """Порт доступа к метаданным StoredFile."""
    def add(self, file: StoredFile) -> None: ...
    def get(self, id: UUID) -> StoredFile | None: ...
    def get_by_hash(self, hash: str) -> StoredFile | None: ...


@runtime_checkable
class StoragePort(Protocol):
    """Порт физического хранения контента."""
    def save(self, location: Path, data: bytes) -> None: ...
    def read(self, location: Path) -> bytes: ...
