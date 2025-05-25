from functools import lru_cache
from pathlib import Path

from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    FILE_STORE_URL: AnyUrl = Field("http://file-store:8000")
    DB_DSN: str = Field("postgresql+psycopg2://scanner:scanner@db:5432/scanner")
    STORAGE_ROOT: Path = Field("/app/storage")
    HTTP_TIMEOUT: float = 5.0
    MAX_CONN: int = 50

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
