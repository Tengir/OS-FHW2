"""Bootstrap FastAPI-приложения file-store."""
from fastapi import FastAPI
from presentation.routes import router as file_router

app = FastAPI(
    title="File Store Service",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
)

app.include_router(file_router, prefix="")
