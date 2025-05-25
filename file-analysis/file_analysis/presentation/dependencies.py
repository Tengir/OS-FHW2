from functools import lru_cache
from pathlib import Path

import httpx

from file_analysis.application.use_cases.analyse import AnalyseFileInteractor
from file_analysis.application.use_cases.get_stats import GetStatsInteractor
from file_analysis.application.use_cases.get_cloud import GetCloudInteractor
from file_analysis.domain.interfaces import StatsRepository, StoragePort, CloudGeneratorPort, FileFetchPort
from file_analysis.infrastructure.db.postgres_stats_repo import PostgresStatsRepository
from file_analysis.infrastructure.storage.disk_storage_adapter import DiskStorageAdapter
from file_analysis.infrastructure.cloud.quickchart_adapter import QuickChartAdapter
from file_analysis.infrastructure.filestore_gateway import FileStoreGatewayAdapter
from .config import get_settings


@lru_cache
def _http_client() -> httpx.AsyncClient:
    s = get_settings()
    limits = httpx.Limits(max_connections=s.MAX_CONN, max_keepalive_connections=s.MAX_CONN)
    return httpx.AsyncClient(timeout=s.HTTP_TIMEOUT, limits=limits)


@lru_cache
def _stats_repo() -> StatsRepository:
    return PostgresStatsRepository(get_settings().DB_DSN)


@lru_cache
def _storage() -> StoragePort:
    root = get_settings().STORAGE_ROOT
    root.mkdir(parents=True, exist_ok=True)
    return DiskStorageAdapter(root)


@lru_cache
def _cloud_gen() -> CloudGeneratorPort:
    return QuickChartAdapter(_http_client())


@lru_cache
def _file_fetcher() -> FileFetchPort:
    return FileStoreGatewayAdapter(get_settings().FILE_STORE_URL, _http_client())


# -------- Use-case factories (DI) ----------

def get_analyse_uc() -> AnalyseFileInteractor:
    return AnalyseFileInteractor(
        stats_repo=_stats_repo(),
        storage=_storage(),
        cloud_gen=_cloud_gen(),
        fetcher=_file_fetcher(),
    )


def get_stats_uc() -> GetStatsInteractor:
    return GetStatsInteractor(repo=_stats_repo())


def get_cloud_uc() -> GetCloudInteractor:
    return GetCloudInteractor(storage=_storage())
