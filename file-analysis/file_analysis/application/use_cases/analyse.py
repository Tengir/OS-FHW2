"""
Фасад (use-case) «Анализировать файл».

• Получает txt-контент из File-Store через FileFetchPort.
• Высчитывает простую статистику (параграфы, слова, символы).
• Запрашивает генератор облака слов (CloudGeneratorPort) → PNG-байты.
• Сохраняет PNG через StoragePort.
• Укладывает итоги в StatsRepository и возвращает DTO для слоя REST.

Архитектура: чистый слой Application, не зависит от внешних библиотек и
реализаций (интерфейсы передаются через конструктор).
"""

from pathlib import Path

from file_analysis.domain.interfaces import (
    StatsRepository,
    StoragePort,
    CloudGeneratorPort,
    FileFetchPort,
)
from file_analysis.domain.entities.file_stats import FileStats
from file_analysis.application.dto import AnalyseCmd, AnalyseResultDTO


class AnalyseFileInteractor:
    """Координирует процесс анализа одного txt-файла."""

    def __init__(
        self,
        stats_repo: StatsRepository,
        storage: StoragePort,
        cloud_gen: CloudGeneratorPort,
        fetcher: FileFetchPort,
    ) -> None:
        """
        Parameters
        ----------
        stats_repo : StatsRepository
            Абстракция для записи/чтения статистики.
        storage : StoragePort
            Порт для сохранения/чтения произвольных байтов (файлов).
        cloud_gen : CloudGeneratorPort
            Сервис генерации word-cloud-изображения.
        fetcher : FileFetchPort
            Порт для извлечения исходного .txt по UUID из File-Store.
        """
        self._stats_repo = stats_repo
        self._storage = storage
        self._cloud_gen = cloud_gen
        self._fetcher = fetcher

    async def execute(self, cmd: AnalyseCmd) -> AnalyseResultDTO:
        """
        Запустить анализ.

        Parameters
        ----------
        cmd : AnalyseCmd
            Команда с идентификатором исходного файла.

        Returns
        -------
        AnalyseResultDTO
            Результаты подсчёта статистики и расположение PNG-файла с облаком.
        """
        # 1. Получаем текст
        text = await self._fetcher.fetch(cmd.file_id)

        # 2. Считаем статистику
        paragraphs = len([p for p in text.splitlines() if p.strip() != ""])
        words = len(text.split())
        chars = len(text)

        # 3. Генерируем PNG-облако слов
        png_bytes = await self._cloud_gen.generate(text)

        # 4. Сохраняем PNG через StoragePort
        cloud_filename = f"cloud_{cmd.file_id}.png"
        self._storage.save(Path(cloud_filename), png_bytes)

        # 5. Создаём доменную сущность и сохраняем в репозитории
        stats = FileStats.create(
            source_file_id=cmd.file_id,
            paragraphs=paragraphs,
            words=words,
            chars=chars,
            cloud_location=Path(cloud_filename),
        )
        self._stats_repo.add(stats)

        # 6. Формируем DTO для слоя REST/GraphQL и т.п.
        return AnalyseResultDTO(
            file_id=stats.source_file_id,
            paragraphs=paragraphs,
            words=words,
            chars=chars,
            cloud_location=Path(cloud_filename),
        )
