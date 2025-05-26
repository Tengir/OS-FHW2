"""
REST-эндпоинты file-analysis сервиса.

• GET /analyze/{file_id}  – считает статистику, генерирует PNG и возвращает DTO
• GET /cloud/{location}   – отдаёт PNG-файл из disk-storage
"""

from uuid import UUID
from pathlib import Path

from fastapi import APIRouter, Depends, status, Response, HTTPException

from file_analysis.application.dto import AnalyseCmd, CloudQuery
from file_analysis.application.use_cases.analyse import AnalyseFileInteractor
from file_analysis.application.use_cases.get_cloud import GetCloudInteractor
from file_analysis.presentation.dependencies import get_analyse_uc, get_cloud_uc

router = APIRouter(tags=["analysis"])


@router.get("/analyze/{file_id}", status_code=status.HTTP_200_OK)
async def analyze(
    file_id: UUID,
    uc: AnalyseFileInteractor = Depends(get_analyse_uc),
):
    """
    Запускает полный цикл анализа файла (txt → stats + png).

    Returns
    -------
    JSON
        Поля `file_id`, `paragraphs`, `words`, `chars`, `cloud_location`.
    """
    try:
        return await uc.execute(AnalyseCmd(file_id=file_id))
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"File {file_id} not found")


@router.get(
    "/cloud/{location:path}",
    responses={200: {"content": {"image/png": {}}}},
    response_class=Response,
)
async def cloud(
    location: str,
    uc: GetCloudInteractor = Depends(get_cloud_uc),
):
    """
    Отдаёт PNG-облако слов.

    Путь (`location`) приходит из `AnalyseResultDTO.cloud_location`.
    """
    try:
        data = uc.execute(CloudQuery(location=Path(location)))
        return Response(data, media_type="image/png")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"PNG {location} not found")
