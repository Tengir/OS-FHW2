"""Загрузка настроек Gateway из переменных окружения (.env)."""
from functools import lru_cache
from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    FILE_STORE_URL:  AnyUrl = Field("http://file-store:8000", env="FILE_STORE_URL")
    ANALYSIS_URL:    AnyUrl = Field("http://file-analysis:8000", env="ANALYSIS_URL")
    REQUEST_TIMEOUT: float  = Field(5.0, env="REQUEST_TIMEOUT")      # seconds
    MAX_CONNECTIONS: int    = Field(50,  env="MAX_CONNECTIONS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Singleton настроек на всё время жизни процесса."""
    return Settings()
