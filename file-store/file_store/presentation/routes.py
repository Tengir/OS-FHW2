"""HTTP-контроллеры File-store-сервиса."""
from uuid import UUID

from fastapi import APIRouter, UploadFile, File, Depends, status, Response

from ..application.dto import UploadFileCmd, UploadFileResult
from ..application.use_cases.upload_file import UploadFileInteractor
from ..application.use_cases.get_file import GetFileInteractor, GetFileQuery
from dependencies import get_upload_interactor, get_file_interactor

router = APIRouter(tags=["file-store"])


@router.post(
    "/upload",
    response_model=UploadFileResult,
    status_code=status.HTTP_201_CREATED,
)
async def upload_file(
    file: UploadFile = File(...),
    uc: UploadFileInteractor = Depends(get_upload_interactor),
) -> UploadFileResult:
    cmd = UploadFileCmd(filename=file.filename, content=await file.read())
    return uc.execute(cmd)


@router.get(
    "/files/{file_id}",
    responses={200: {"content": {"text/plain": {}}}},
    response_class=Response,
)
async def get_file(
    file_id: UUID,
    uc: GetFileInteractor = Depends(get_file_interactor),
) -> Response:
    dto = uc.execute(GetFileQuery(id=file_id))
    return Response(dto.content, media_type="text/plain")
