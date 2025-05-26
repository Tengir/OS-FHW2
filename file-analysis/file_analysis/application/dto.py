"""
DTO-модели слоя Application.

Используем Pydantic для простой валидации и автогенерации `.model_dump()`.
"""

from pathlib import Path
from uuid import UUID

from pydantic import BaseModel


class AnalyseCmd(BaseModel):
    """Команда на запуск анализа файла по его UUID."""
    file_id: UUID


class AnalyseResultDTO(BaseModel):
    """Результат анализа + путь к PNG-облаку."""
    file_id: UUID
    paragraphs: int
    words: int
    chars: int
    cloud_location: Path


class StatsDTO(BaseModel):
    """DTO для чтения статистики без PNG."""
    file_id: UUID
    paragraphs: int
    words: int
    chars: int


class CloudQuery(BaseModel):
    """Запрос на чтение PNG-облака слов."""
    location: Path
