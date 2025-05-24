from pathlib import Path
from uuid import UUID

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class FileRow(Base):
    """ORM-таблица files(id, name, hash, location)."""
    __tablename__ = "files"

    id:        Mapped[UUID] = mapped_column(primary_key=True)
    name:      Mapped[str]
    hash:      Mapped[str]  # sha256
    location:  Mapped[str]  # хранится как TEXT
