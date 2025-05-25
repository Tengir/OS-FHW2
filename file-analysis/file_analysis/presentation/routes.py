from uuid import UUID
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status, Response

from file_analysis.application.dto import AnalyseCmd, CloudQuery
from file_analysis.application.use_cases.analyse import AnalyseFileInteractor
from file_analysis.application.use_cases.get_stats import GetStatsInteractor
from file_analysis.application.use_cases.get_cloud import GetCloudInteractor
from file_analysis.presentation.dependencies import get_analyse_uc, get_stats_uc, get_cloud_uc

router = APIRouter(tags=["analysis"])


@router.post("/analyze/{file_id}", status_code=status.HTTP_201_CREATED)
async def analyze(
    file_id: UUID,
    uc: AnalyseFileInteractor = Depends(get_analyse_uc),
):
    return await uc.execute(AnalyseCmd(file_id=file_id))


@router.get("/stats/{file_id}")
async def stats(
    file_id: UUID,
    uc: GetStatsInteractor = Depends(get_stats_uc),
):
    return uc.execute(file_id)


@router.get(
    "/cloud/{location:path}",
    responses={200: {"content": {"image/png": {}}}},
    response_class=Response,
)
async def cloud(
    location: str,
    uc: GetCloudInteractor = Depends(get_cloud_uc),
):
    data = uc.execute(CloudQuery(location=Path(location)))
    return Response(data, media_type="image/png")
