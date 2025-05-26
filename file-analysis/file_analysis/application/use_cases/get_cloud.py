"""
Use-case «Получить PNG-облако слов из хранилища».

Инкапсулирует лишь вызов StoragePort, поэтому синхронный.
"""

from pathlib import Path

from file_analysis.domain.interfaces import StoragePort
from file_analysis.application.dto import CloudQuery


class GetCloudInteractor:
    """Читает PNG-файл по запрошенному пути."""

    def __init__(self, storage: StoragePort) -> None:
        """
        Parameters
        ----------
        storage : StoragePort
            Порт работы с файловым хранилищем.
        """
        self._storage = storage

    def execute(self, query: CloudQuery) -> bytes:
        """
        Загрузить содержимое PNG-файла.

        Parameters
        ----------
        query : CloudQuery
            DTO с путём до изображения.

        Returns
        -------
        bytes
            Сырые байты PNG (готовы к отдаче через FastAPI/Flask и т.д.).
        """
        return self._storage.read(query.location)
