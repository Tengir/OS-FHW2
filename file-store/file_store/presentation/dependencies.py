"""
DI-фабрики для FastAPI-слоя File-Store.

Создают и кэшируют (через lru_cache) репозиторий и хранилище,
а затем подставляют их в интеракторы через Depends.
"""

from functools import lru_cache
from pathlib import Path
from os import getenv

from file_store.application.use_cases.upload_file import UploadFileInteractor
from file_store.application.use_cases.get_file import GetFileInteractor
from file_store.infrastructure.db.postgres_file_repo import PostgresFileRepository
from file_store.infrastructure.storage.disk_adapter import DiskStorageAdapter  # noqa: I202


# ---------- singletons (низкоуровневые) ----------------------------------- #

@lru_cache
def _repo() -> PostgresFileRepository:
    """
    Синглтон-репозиторий (PostgreSQL).

    DSN берётся из переменной окружения ``FILE_DB_DSN`` или дефолта.
    """
    dsn = getenv("FILE_DB_DSN", "postgresql+asyncpg://scanner:scanner@db:5432/scanner")
    return PostgresFileRepository(dsn)


@lru_cache
def _storage() -> DiskStorageAdapter:
    """
    Синглтон-хранилище на диске.

    Базовый путь — ``FILE_STORAGE_ROOT`` или ``/app/storage``.
    """
    base = Path(getenv("FILE_STORAGE_ROOT", "/app/storage"))
    base.mkdir(parents=True, exist_ok=True)
    return DiskStorageAdapter(base)


# ---------- use-case factories ------------------------------------------- #

def get_upload_interactor() -> UploadFileInteractor:
    """Factory для Depends → UploadFileInteractor."""
    return UploadFileInteractor(repo=_repo(), storage=_storage())


def get_file_interactor() -> GetFileInteractor:
    """Factory для Depends → GetFileInteractor."""
    return GetFileInteractor(repo=_repo(), storage=_storage())
