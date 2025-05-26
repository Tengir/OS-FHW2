"""
HTTP-адаптер, получающий txt-файл из микросервиса File-Store.

Использует `httpx.AsyncClient`, соединяет базовый URL и путь `files/{id}`
корректно через `urljoin`.
"""

from urllib.parse import urljoin
from uuid import UUID

import httpx
from pydantic import AnyUrl

from file_analysis.domain.interfaces import FileFetchPort


class FileStoreGatewayAdapter(FileFetchPort):
    """`FileFetchPort`, работающий по REST-у File-Store-сервиса."""

    _base: AnyUrl
    _client: httpx.AsyncClient

    def __init__(self, base_url: AnyUrl, client: httpx.AsyncClient) -> None:
        self._base = base_url
        self._client = client

    async def fetch(self, file_id: UUID) -> str:
        """
        GET /files/{file_id} → текст.

        Raises
        ------
        httpx.HTTPStatusError
            Если сервис File-Store вернул не-2xx статус.
        """
        url = urljoin(str(self._base).rstrip("/") + "/", f"files/{file_id}")
        resp = await self._client.get(url)
        resp.raise_for_status()
        return resp.text
