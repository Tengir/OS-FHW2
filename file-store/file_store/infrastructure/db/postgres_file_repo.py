"""
SQLAlchemy-реализация FileRepository (sync).

Слой infrastructure: хранит данные в таблице `files`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable
from uuid import UUID

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from file_store.domain.entities.stored_file import StoredFile
from file_store.domain.interfaces import FileRepository
from file_store.infrastructure.db.models import Base, FileRow


class PostgresFileRepository(FileRepository):
    """Реализация FileRepository поверх PostgreSQL."""

    def __init__(self, dsn: str) -> None:
        """
        Parameters
        ----------
        dsn : str
            DSN в формате SQLAlchemy, напр.
            ``postgresql+psycopg2://scanner:scanner@db_store:5432/store``.
        """
        engine = create_engine(dsn, future=True)
        Base.metadata.create_all(engine)  # auto-migration для demo
        self._session_factory: Callable[[], Session] = scoped_session(
            sessionmaker(engine, autoflush=False, expire_on_commit=False)
        )

    # ------------------------------------------------------------------ #
    # CRUD (FileRepository interface)
    # ------------------------------------------------------------------ #

    def add(self, file: StoredFile) -> None:
        """INSERT FileRow."""
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
        """SELECT * FROM files WHERE id = :id."""
        with self._session_factory() as ss:
            row: FileRow | None = ss.get(FileRow, id)
            return self._row_to_entity(row)

    def get_by_hash(self, hash: str) -> StoredFile | None:
        """SELECT * FROM files WHERE hash = :hash."""
        stmt = select(FileRow).where(FileRow.hash == hash)
        with self._session_factory() as ss:
            row: FileRow | None = ss.scalar(stmt)
            return self._row_to_entity(row)

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #

    @staticmethod
    def _row_to_entity(row: FileRow | None) -> StoredFile | None:
        """Преобразует ORM-объект в доменную сущность или None."""
        if row is None:
            return None
        return StoredFile(
            id=row.id,
            name=row.name,
            hash=row.hash,
            location=Path(row.location),
        )
