from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Protocol
from uuid import UUID

from file_analysis.domain.entities.file_stats import FileStats


class StatsRepository(Protocol):
    def add(self, stats: FileStats) -> None: ...
    def get(self, file_id: UUID) -> FileStats | None: ...


class StoragePort(Protocol):
    def save(self, location: Path, data: bytes) -> None: ...
    def read(self, location: Path) -> bytes: ...


class CloudGeneratorPort(Protocol):
    async def generate(self, text: str, dst: Path) -> None: ...


class FileFetchPort(Protocol):
    async def fetch(self, file_id: UUID) -> str: ...
