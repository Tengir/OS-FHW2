from pathlib import Path
from uuid import UUID, uuid4


class StoredFile:
    _id: UUID
    _name: str
    _hash: str
    _location: Path

    def __init__(self, id: UUID, name: str, hash: str, location: Path):
        self._id = id
        self._name = name
        self._hash = hash
        self._location = location

    @classmethod
    def create(cls, name: str, hash_: str, location: Path) -> "StoredFile":
        return cls(uuid4(), name, hash_, location)

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def hash(self) -> str:
        return self._hash

    @property
    def location(self) -> Path:
        return self._location
