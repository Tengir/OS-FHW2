from __future__ import annotations

from pathlib import Path
from typing import Callable
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy import create_engine

from ...domain.entities.stored_file import StoredFile
from ...domain.interfaces import FileRepository
from .models import Base, FileRow


class PostgresFileRepository(FileRepository):
    """SQLAlchemy-реализация FileRepository (sync)."""

    def __init__(self, dsn: str) -> None:
        engine = create_engine(dsn, future=True)
        Base.metadata.create_all(engine)              # auto-migration для demo
        self._session_factory: Callable[[], Session] = scoped_session(
            sessionmaker(engine, autoflush=False, expire_on_commit=False)
        )

    # CRUD -----------
    def add(self, file: StoredFile) -> None:
        with self._session_factory() as ss, ss.begin():
            ss.add(
                FileRow(
                    id=file.id,
                    name=file.name,
                    hash=file.hash,
                    location=str(file.location),
                )
            )

    def get(self, id: UUID) -> StoredFile | None:
        with self._session_factory() as ss:
            row: FileRow | None = ss.get(FileRow, id)
            return self._row_to_entity(row)

    def get_by_hash(self, hash: str) -> StoredFile | None:
        stmt = select(FileRow).where(FileRow.hash == hash)
        with self._session_factory() as ss:
            row: FileRow | None = ss.scalar(stmt)
            return self._row_to_entity(row)

    # util -----------
    @staticmethod
    def _row_to_entity(row: FileRow | None) -> StoredFile | None:
        if row is None:
            return None
        return StoredFile(
            id=row.id,
            name=row.name,
            hash=row.hash,
            location=Path(row.location),
        )
