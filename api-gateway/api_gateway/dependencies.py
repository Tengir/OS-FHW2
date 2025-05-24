"""DI-фабрики: создаём httpx.AsyncClient c пулом и тайм-аутами."""
from functools import lru_cache

import httpx
from config import get_settings


@lru_cache
def get_http_client() -> httpx.AsyncClient:
    s = get_settings()
    limits = httpx.Limits(max_connections=s.MAX_CONNECTIONS, max_keepalive_connections=s.MAX_CONNECTIONS)
    return httpx.AsyncClient(timeout=s.REQUEST_TIMEOUT, limits=limits, follow_redirects=True)
