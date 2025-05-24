"""DI-фабрики use-case-классов для FastAPI‐роутов."""
from functools import lru_cache
from pathlib import Path
from os import getenv

from ..application.use_cases.upload_file import UploadFileInteractor
from ..application.use_cases.get_file import GetFileInteractor
from ..infrastructure.db.postgres_file_repo import PostgresFileRepository
from ..infrastructure.storage.disk_adapter import DiskStorageAdapter


@lru_cache
def _repo() -> PostgresFileRepository:  # singleton на время жизни приложения
    dsn = getenv("FILE_DB_DSN", "postgresql+asyncpg://scanner:scanner@db:5432/scanner")
    return PostgresFileRepository(dsn)


@lru_cache
def _storage() -> DiskStorageAdapter:
    base = Path(getenv("FILE_STORAGE_ROOT", "/app/storage"))
    base.mkdir(parents=True, exist_ok=True)
    return DiskStorageAdapter(base)


def get_upload_interactor() -> UploadFileInteractor:
    return UploadFileInteractor(repo=_repo(), storage=_storage())


def get_file_interactor() -> GetFileInteractor:
    return GetFileInteractor(repo=_repo(), storage=_storage())
