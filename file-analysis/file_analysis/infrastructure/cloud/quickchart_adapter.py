from urllib.parse import urlencode

import httpx

from file_analysis.domain.interfaces import CloudGeneratorPort


class QuickChartAdapter(CloudGeneratorPort):
    """Генерирует облако слов через API quickchart.io и возвращает PNG-байты."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def generate(self, text: str) -> bytes:
        query = urlencode({"text": text, "format": "png"})
        url = f"https://quickchart.io/wordcloud?{query}"

        resp = await self._client.get(url)
        resp.raise_for_status()
        return resp.content # PNG-байты

