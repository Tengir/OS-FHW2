"""Use-case «Получить файл по ID»."""
from uuid import UUID

from ...domain.interfaces import FileRepository, StoragePort
from ..dto import GetFileQuery, FileReadDTO


class GetFileInteractor:
    """Возвращает файл пользователю."""

    def __init__(self, repo: FileRepository, storage: StoragePort) -> None:
        self._repo = repo
        self._storage = storage

    def execute(self, query: GetFileQuery) -> FileReadDTO:
        stored = self._repo.get(query.id)
        if stored is None:
            raise FileNotFoundError(query.id)

        content = self._storage.read(stored.location)
        return FileReadDTO(
            id=stored.id,
            filename=stored.name,
            content=content,
            location=stored.location,
        )
