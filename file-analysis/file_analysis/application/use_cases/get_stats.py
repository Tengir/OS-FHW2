from uuid import UUID

from file_analysis.domain.interfaces import StatsRepository
from file_analysis.application.dto import StatsDTO


class GetStatsInteractor:
    def __init__(self, repo: StatsRepository) -> None:
        self._repo = repo

    def execute(self, file_id: UUID) -> StatsDTO:
        stats = self._repo.get(file_id)
        if stats is None:
            raise FileNotFoundError(file_id)

        return StatsDTO(
            file_id=stats.source_file_id,
            paragraphs=stats.paragraphs,
            words=stats.words,
            chars=stats.chars,
        )
