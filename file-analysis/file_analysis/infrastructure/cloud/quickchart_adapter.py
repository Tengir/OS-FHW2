import httpx
from pathlib import Path
from typing import Any

from ...domain.interfaces import CloudGeneratorPort


class QuickChartAdapter(CloudGeneratorPort):
    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def generate(self, text: str, dst: Path) -> None:
        payload: dict[str, Any] = {"text": text}
        resp = await self._client.post("https://quickchart.io/wordcloud", json=payload)
        resp.raise_for_status()
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(resp.content)
