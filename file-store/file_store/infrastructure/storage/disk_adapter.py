"""
Адаптер StoragePort, сохраняющий данные на локальный диск (docker-volume).

Используется микросервисом **File-Store** для хранения загруженных .txt-файлов.
"""

from pathlib import Path

from file_store.domain.interfaces import StoragePort


class DiskStorageAdapter(StoragePort):
    """Файловая система, «привязанная» к директории `root`."""

    def __init__(self, root: Path) -> None:
        """
        Parameters
        ----------
        root : Path
            Базовая директория. Должна быть примонтирована в docker-volume,
            чтобы данные сохранялись вне контейнера.
        """
        self._root = root

    # ------------------------------------------------------------------ #
    # StoragePort interface
    # ------------------------------------------------------------------ #

    def save(self, location: Path, data: bytes) -> None:
        """
        Сохраняет байты по относительному пути `location`.

        Создаёт промежуточные папки, если их ещё нет.
        """
        full_path = self._root / location
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_bytes(data)

    def read(self, location: Path) -> bytes:
        """Читает файл и возвращает его содержимое."""
        full_path = self._root / location
        return full_path.read_bytes()
