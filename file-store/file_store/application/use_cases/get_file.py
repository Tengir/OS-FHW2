"""
Use-case «Получить файл по ID».

Алгоритм
--------
1. Читает сущность `StoredFile` из репозитория (по UUID).
2. Если не найдено — бросает `FileNotFoundError` (перехватится
   FastAPI-handler'ом и превратится в 404).
3. Загружает содержимое файла из StoragePort.
4. Возвращает DTO, пригодный для ответа REST-слою.
"""

from file_store.application.dto import GetFileQuery, FileReadDTO
from file_store.domain.interfaces import FileRepository, StoragePort


class GetFileInteractor:
    """Синхронный интерактор, возвращающий файл пользователю."""

    def __init__(self, repo: FileRepository, storage: StoragePort) -> None:
        """
        Parameters
        ----------
        repo : FileRepository
            Репозиторий метаданных сохранённых файлов (Postgres, Memory и т.д.).
        storage : StoragePort
            Порт для фактического чтения байтов с диска / S3 / GridFS и т.п.
        """
        self._repo = repo
        self._storage = storage

    def execute(self, query: GetFileQuery) -> FileReadDTO:
        """
        Parameters
        ----------
        query : GetFileQuery
            Объект с UUID запрашиваемого файла.

        Returns
        -------
        FileReadDTO
            Полный DTO с ID, оригинальным именем, содержимым и путём.
        """
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
