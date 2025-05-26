"""Все публичные REST-энд-пойнты Gateway."""
from uuid import UUID
from urllib.parse import urljoin

import httpx
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status, Response

from api_gateway.config import get_settings
from api_gateway.dependencies import get_http_client

router = APIRouter(tags=["gateway"], prefix="")

# ---------- helpers ---------------------------------------------------------

def _proxy_error(exc: Exception) -> HTTPException:
    """Преобразовать внутренние ошибки в читабельный HTTP-ответ."""
    if isinstance(exc, httpx.TimeoutException):
        return HTTPException(status.HTTP_504_GATEWAY_TIMEOUT, "Upstream timeout")
    if isinstance(exc, httpx.RequestError):
        return HTTPException(status.HTTP_502_BAD_GATEWAY, "Service unreachable")
    return HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Unexpected gateway error")


# ---------- endpoints -------------------------------------------------------

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    client: httpx.AsyncClient = Depends(get_http_client),
):
    """Принимает текстовый .txt файл и проксирует его в File-Store."""
    try:
        files = {"file": (file.filename, await file.read(), file.content_type)}
        url = urljoin(str(get_settings().FILE_STORE_URL), "upload")
        resp = await client.post(url, files=files)
    except Exception as exc:
        raise _proxy_error(exc)

    return Response(resp.content, status_code=resp.status_code, media_type=resp.headers.get("content-type"))


@router.get("/files/{file_id}")
async def download_file(
    file_id: UUID,
    client: httpx.AsyncClient = Depends(get_http_client),
):
    """Отдаёт .txt по ID из File-Store."""
    try:
        url = urljoin(str(get_settings().FILE_STORE_URL), f"files/{file_id}")
        resp = await client.get(url)
    except Exception as exc:
        raise _proxy_error(exc)

    return Response(resp.content, status_code=resp.status_code, media_type=resp.headers.get("content-type"))


@router.get("/analyze/{file_id}")
async def analyze_file(
    file_id: UUID,
    client: httpx.AsyncClient = Depends(get_http_client),
):
    """Запрос статистики из File-Analysis."""
    try:
        url = urljoin(str(get_settings().ANALYSIS_URL), f"analyze/{file_id}")
        resp = await client.get(url)
    except Exception as exc:
        raise _proxy_error(exc)

    return Response(resp.content, status_code=resp.status_code, media_type=resp.headers.get("content-type"))


@router.get("/cloud/{path:path}")
async def get_cloud(
    path: str,
    client: httpx.AsyncClient = Depends(get_http_client),
):
    """Отдаёт png-облако слов из File-Analysis."""
    try:
        url = urljoin(str(get_settings().ANALYSIS_URL), f"cloud/{path}")
        resp = await client.get(url)
    except Exception as exc:
        raise _proxy_error(exc)

    return Response(resp.content, status_code=resp.status_code, media_type=resp.headers.get("content-type"))
