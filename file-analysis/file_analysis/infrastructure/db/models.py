from uuid import UUID

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class StatsRow(Base):
    __tablename__ = "stats"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    source_file_id: Mapped[UUID]
    paragraphs: Mapped[int]
    words: Mapped[int]
    chars: Mapped[int]
    cloud_location: Mapped[str]
