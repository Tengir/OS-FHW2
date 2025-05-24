import hashlib
from pathlib import Path
from uuid import UUID

from ...domain.interfaces import (
    StatsRepository,
    StoragePort,
    CloudGeneratorPort,
    FileFetchPort,
)
from ...domain.entities import FileStats
from ..dto import AnalyseCmd, AnalyseResultDTO


class AnalyseFileInteractor:
    def __init__(
        self,
        stats_repo: StatsRepository,
        storage: StoragePort,
        cloud_gen: CloudGeneratorPort,
        fetcher: FileFetchPort,
    ) -> None:
        self._stats_repo = stats_repo
        self._storage = storage
        self._cloud_gen = cloud_gen
        self._fetcher = fetcher

    async def execute(self, cmd: AnalyseCmd) -> AnalyseResultDTO:
        text = await self._fetcher.fetch(cmd.file_id)

        paragraphs = text.count("\n\n") + 1
        words = len(text.split())
        chars = len(text)

        cloud_location = Path(f"cloud_{cmd.file_id}.png")
        await self._cloud_gen.generate(text, cloud_location)

        stats = FileStats.create(
            source_file_id=cmd.file_id,
            paragraphs=paragraphs,
            words=words,
            chars=chars,
            cloud_location=cloud_location,
        )
        self._stats_repo.add(stats)

        return AnalyseResultDTO(
            file_id=stats.source_file_id,
            paragraphs=paragraphs,
            words=words,
            chars=chars,
            cloud_location=cloud_location,
        )
