"""
Порты (абстракции) доменного слоя.

Определяют контракты, которые реализуются в инфраструктуре и
передаются в Application через DI.
"""

from pathlib import Path
from typing import Protocol
from uuid import UUID

from file_analysis.domain.entities.file_stats import FileStats


class StatsRepository(Protocol):
    """Порт репозитория статистики."""

    def add(self, stats: FileStats) -> None: ...
    def get(self, file_id: UUID) -> FileStats | None: ...


class StoragePort(Protocol):
    """Унифицированное хранилище для произвольных байтов."""

    def save(self, location: Path, data: bytes) -> None: ...
    def read(self, location: Path) -> bytes: ...


class CloudGeneratorPort(Protocol):
    """Генератор PNG-облака слов."""

    async def generate(self, text: str) -> bytes: ...


class FileFetchPort(Protocol):
    """Получение исходного .txt из File-Store по UUID."""

    async def fetch(self, file_id: UUID) -> str: ...
