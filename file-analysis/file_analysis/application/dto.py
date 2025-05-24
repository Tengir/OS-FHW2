from pathlib import Path
from uuid import UUID

from pydantic import BaseModel, Field


class AnalyseCmd(BaseModel):
    file_id: UUID


class AnalyseResultDTO(BaseModel):
    file_id: UUID
    paragraphs: int
    words: int
    chars: int
    cloud_location: Path


class StatsDTO(BaseModel):
    file_id: UUID
    paragraphs: int
    words: int
    chars: int


class CloudQuery(BaseModel):
    location: Path
