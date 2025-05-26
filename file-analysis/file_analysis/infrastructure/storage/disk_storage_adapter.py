"""
Адаптер `StoragePort`, сохраняющий файлы на локальный диск.

Используется и для PNG-облаков, и для опциональных txt-файлов.
"""

from pathlib import Path

from file_analysis.domain.interfaces import StoragePort


class DiskStorageAdapter(StoragePort):
    """Примитивная файловая система на указанной директории `root`."""

    def __init__(self, root: Path) -> None:
        """
        Parameters
        ----------
        root : Path
            Базовая директория. Будет создана при первом сохранении.
        """
        self._root = root

    # ------------------------------------------------------------------ #
    # StoragePort interface
    # ------------------------------------------------------------------ #

    def save(self, location: Path, data: bytes) -> None:
        """Сохраняет `data` по относительному пути `location`."""
        path = self._root / location
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def read(self, location: Path) -> bytes:
        """Читает файл и возвращает его содержимое."""
        path = self._root / location
        return path.read_bytes()
