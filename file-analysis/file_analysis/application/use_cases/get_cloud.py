from pathlib import Path

from file_analysis.domain.interfaces import StoragePort
from file_analysis.application.dto import CloudQuery


class GetCloudInteractor:
    def __init__(self, storage: StoragePort) -> None:
        self._storage = storage

    def execute(self, query: CloudQuery) -> bytes:
        return self._storage.read(query.location)
