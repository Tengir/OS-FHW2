"""Use-case «Загрузить файл»."""
import hashlib
from uuid import uuid4
from pathlib import Path

from ...domain.entities.stored_file import StoredFile
from ...domain.interfaces import FileRepository, StoragePort
from ..dto import UploadFileCmd, UploadFileResult


class UploadFileInteractor:
    """Сохраняет файл, предотвращая дубликаты по sha256-хэшу."""

    def __init__(self, repo: FileRepository, storage: StoragePort) -> None:
        self._repo = repo
        self._storage = storage

    def execute(self, cmd: UploadFileCmd) -> UploadFileResult:
        file_hash = hashlib.sha256(cmd.content).hexdigest()

        existing = self._repo.get_by_hash(file_hash)
        if existing:
            return UploadFileResult(id=existing.id)

        file_id = uuid4()
        location = Path(f"{file_id}.txt")

        self._storage.save(location, cmd.content)

        stored = StoredFile(
            id=file_id,
            name=cmd.filename,
            hash=file_hash,
            location=location,
        )
        self._repo.add(stored)

        return UploadFileResult(id=file_id)
