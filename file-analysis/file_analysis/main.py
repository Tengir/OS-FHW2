from fastapi import FastAPI
from file_analysis.presentation.routes import router as analysis_router

app = FastAPI(
    title="File Analysis Service",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
)

app.include_router(analysis_router)
