from pathlib import Path
from uuid import UUID
from typing import Callable

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from file_analysis.domain.entities.file_stats import FileStats
from file_analysis.domain.interfaces import StatsRepository
from file_analysis.infrastructure.db.models import Base, StatsRow


class PostgresStatsRepository(StatsRepository):
    def __init__(self, dsn: str) -> None:
        eng = create_engine(dsn, future=True)
        Base.metadata.create_all(eng)
        self._sf: Callable[[], Session] = scoped_session(
            sessionmaker(eng, autoflush=False, expire_on_commit=False)
        )

    def add(self, stats: FileStats) -> None:
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
