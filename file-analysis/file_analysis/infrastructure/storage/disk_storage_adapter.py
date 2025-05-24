from pathlib import Path

from ...domain.interfaces import StoragePort


class DiskStorageAdapter(StoragePort):
    def __init__(self, root: Path) -> None:
        self._root = root

    def save(self, location: Path, data: bytes) -> None:
        path = self._root / location
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def read(self, location: Path) -> bytes:
        path = self._root / location
        return path.read_bytes()
