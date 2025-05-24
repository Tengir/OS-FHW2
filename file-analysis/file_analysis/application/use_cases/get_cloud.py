from pathlib import Path

from ...domain.interfaces import StoragePort
from ..dto import CloudQuery


class GetCloudInteractor:
    def __init__(self, storage: StoragePort) -> None:
        self._storage = storage

    def execute(self, query: CloudQuery) -> bytes:
        return self._storage.read(query.location)
