"""
Инфраструктурный репозиторий статистики на PostgreSQL.

• Хранит/читает сущность `FileStats` в таблице `stats` (модель `StatsRow`).
• Использует SQLAlchemy ORM (sync-режим, future =True).
"""

from pathlib import Path
from uuid import UUID
from typing import Callable

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from file_analysis.domain.entities.file_stats import FileStats
from file_analysis.domain.interfaces import StatsRepository
from file_analysis.infrastructure.db.models import Base, StatsRow


class PostgresStatsRepository(StatsRepository):
    """Реализация `StatsRepository`, работающая поверх PostgreSQL + SQLAlchemy."""

    def __init__(self, dsn: str) -> None:
        """
        Parameters
        ----------
        dsn : str
            Строка подключения вида
            ``postgresql+psycopg2://user:password@host:port/dbname``.
        """
        eng = create_engine(dsn, future=True)
        Base.metadata.create_all(eng)  # «ленивая» миграция – лишь для учебного примера
        self._sf: Callable[[], Session] = scoped_session(
            sessionmaker(eng, autoflush=False, expire_on_commit=False)
        )

    # --------------------------------------------------------------------- #
    # StatsRepository interface
    # --------------------------------------------------------------------- #

    def add(self, stats: FileStats) -> None:
        """Сохраняет статистику одним INSERT-ом в транзакции."""
        with self._sf() as ss, ss.begin():
            ss.add(
                StatsRow(
                    id=stats.id,
                    source_file_id=stats.source_file_id,
                    paragraphs=stats.paragraphs,
                    words=stats.words,
                    chars=stats.chars,
                    cloud_location=str(stats.cloud_location),
                )
            )

    def get(self, file_id: UUID) -> FileStats | None:
        """Возвращает `FileStats` или `None`, если запись не найдена."""
        stmt = select(StatsRow).where(StatsRow.source_file_id == file_id)
        with self._sf() as ss:
            row: StatsRow | None = ss.scalar(stmt)
            if row is None:
                return None
            return FileStats(
                id=row.id,
                source_file_id=row.source_file_id,
                paragraphs=row.paragraphs,
                words=row.words,
                chars=row.chars,
                cloud_location=Path(row.cloud_location),
            )
