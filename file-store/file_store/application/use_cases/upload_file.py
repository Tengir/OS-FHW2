"""
Use-case «Загрузить файл».

Предотвращает дубликаты по sha256-хэшу: если файл с тем же хэшем уже есть,
возвращает существующий UUID вместо создания нового.
"""

import hashlib
from uuid import uuid4
from pathlib import Path

from file_store.domain.entities.stored_file import StoredFile
from file_store.domain.interfaces import FileRepository, StoragePort
from file_store.application.dto import UploadFileCmd, UploadFileResult


class UploadFileInteractor:
    """Сохраняет txt-файл в Storage + метаданные в репозиторий."""

    def __init__(self, repo: FileRepository, storage: StoragePort) -> None:
        self._repo = repo
        self._storage = storage

    def execute(self, cmd: UploadFileCmd) -> UploadFileResult:
        """
        Parameters
        ----------
        cmd : UploadFileCmd
            DTO с именем файла и его бинарным содержимым.

        Returns
        -------
        UploadFileResult
            UUID сохранённого (или уже существующего) файла.
        """
        file_hash = hashlib.sha256(cmd.content).hexdigest()

        # Проверяем дубликаты
        existing = self._repo.get_by_hash(file_hash)
        if existing:
            return UploadFileResult(id=existing.id)

        # Создаём новый идентификатор и путь
        file_id = uuid4()
        location = Path(f"{file_id}.txt")

        # Сохраняем физический файл
        self._storage.save(location, cmd.content)

        # Фиксируем в репозитории
        stored = StoredFile(
            id=file_id,
            name=cmd.filename,
            hash=file_hash,
            location=location,
        )
        self._repo.add(stored)

        return UploadFileResult(id=file_id)
