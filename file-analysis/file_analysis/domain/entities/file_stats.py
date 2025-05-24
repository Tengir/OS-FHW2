# domain/entities/file_stats.py
from pathlib import Path
from uuid import UUID, uuid4


class FileStats:
    """Доменная сущность статистики текстового файла."""

    _id: UUID
    _source_file_id: UUID
    _paragraphs: int
    _words: int
    _chars: int
    _cloud_location: Path

    # ---------------- ctor / factory -----------------
    def __init__(
            self,
            id: UUID,
            source_file_id: UUID,
            paragraphs: int,
            words: int,
            chars: int,
            cloud_location: Path,
    ) -> None:
        self._id = id
        self._source_file_id = source_file_id
        self._paragraphs = paragraphs
        self._words = words
        self._chars = chars
        self._cloud_location = cloud_location

    @classmethod
    def create(
            cls,
            source_file_id: UUID,
            paragraphs: int,
            words: int,
            chars: int,
            cloud_location: Path,
    ) -> "FileStats":
        return cls(uuid4(), source_file_id, paragraphs, words, chars, cloud_location)

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def source_file_id(self) -> UUID:
        return self._source_file_id

    @property
    def paragraphs(self) -> int:
        return self._paragraphs

    @property
    def words(self) -> int:
        return self._words

    @property
    def chars(self) -> int:
        return self._chars

    @property
    def cloud_location(self) -> Path:
        return self._cloud_location
