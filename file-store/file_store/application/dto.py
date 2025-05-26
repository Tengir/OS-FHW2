"""
DTO-объекты слоя Application для File-Store микросервиса.
"""

from uuid import UUID
from pathlib import Path

from pydantic import BaseModel, Field


class UploadFileCmd(BaseModel):
    """Команда: загрузить файл."""
    filename: str
    content: bytes


class UploadFileResult(BaseModel):
    """Результат загрузки: UUID файла (существующего или нового)."""
    id: UUID = Field(..., description="Идентификатор загруженного файла")


class GetFileQuery(BaseModel):
    """Запрос: получить файл по UUID."""
    id: UUID


class FileReadDTO(BaseModel):
    """DTO с полным содержимым файла."""
    id: UUID
    filename: str
    content: bytes
    location: Path
