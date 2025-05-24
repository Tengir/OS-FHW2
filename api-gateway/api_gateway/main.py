"""Bootstrap FastAPI Gateway."""
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routes import router

app = FastAPI(
    title="API Gateway",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
)

# CORS (если фронт зовёт с браузера)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
