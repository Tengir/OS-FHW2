from pathlib import Path

from file_store.domain.interfaces import StoragePort


class DiskStorageAdapter(StoragePort):
    """Хранение файлов на локальном диске / volume."""

    def __init__(self, root: Path) -> None:
        self._root = root

    # API ----------
    def save(self, location: Path, data: bytes) -> None:
        full_path = self._root / location
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_bytes(data)

    def read(self, location: Path) -> bytes:
        full_path = self._root / location
        return full_path.read_bytes()
