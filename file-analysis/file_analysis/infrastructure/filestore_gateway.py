from uuid import UUID

import httpx

from file_analysis.domain.interfaces import FileFetchPort


class FileStoreGatewayAdapter(FileFetchPort):
    def __init__(self, base_url: str, client: httpx.AsyncClient):
        self._base = base_url.rstrip("/")
        self._client = client

    async def fetch(self, file_id: UUID) -> str:
        resp = await self._client.get(f"{self._base}/files/{file_id}")
        resp.raise_for_status()
        return resp.text
