"""
HTTP-эндпоинты File-Store-сервиса.

• POST /upload         – загрузка .txt, предотвращение дубликатов
• GET  /files/{id}     – скачивание файла
"""

from uuid import UUID
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, Depends, status, Response, HTTPException

from file_store.application.dto import UploadFileCmd, UploadFileResult
from file_store.application.use_cases.upload_file import UploadFileInteractor
from file_store.application.use_cases.get_file import GetFileInteractor, GetFileQuery
from file_store.presentation.dependencies import get_upload_interactor, get_file_interactor

router = APIRouter(tags=["file-store"])


# ---------- upload -------------------------------------------------------- #

@router.post(
    "/upload",
    response_model=UploadFileResult,
    status_code=status.HTTP_201_CREATED,
)
async def upload_file(
    file: UploadFile = File(...),
    uc: UploadFileInteractor = Depends(get_upload_interactor),
) -> UploadFileResult:
    """
    Загрузить текстовый файл.

    Возвращает UUID — новый или уже существующий, если файл-дубликат.
    """
    cmd = UploadFileCmd(filename=file.filename, content=await file.read())
    return uc.execute(cmd)


# ---------- download ------------------------------------------------------ #

@router.get(
    "/files/{file_id}",
    responses={200: {"content": {"text/plain": {}}}},
    response_class=Response,
)
async def get_file(
    file_id: UUID,
    uc: GetFileInteractor = Depends(get_file_interactor),
) -> Response:
    """
    Скачать текстовый файл по UUID.

    Возвращает содержимое с `text/plain`. Если не найдено → 404.
    """
    try:
        dto = uc.execute(GetFileQuery(id=file_id))
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"File {file_id} not found") from None
    return Response(dto.content, media_type="text/plain")
