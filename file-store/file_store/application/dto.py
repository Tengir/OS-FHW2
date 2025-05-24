from uuid import UUID
from pydantic import BaseModel, Field, FilePath


class UploadFileCmd(BaseModel):
    filename: str
    content: bytes


class UploadFileResult(BaseModel):
    id: UUID = Field(..., description="Идентификатор загруженного файла")


class GetFileQuery(BaseModel):
    id: UUID


class FileReadDTO(BaseModel):
    id: UUID
    filename: str
    content: bytes
    location: FilePath
