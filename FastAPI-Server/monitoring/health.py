# monitoring/health.py

from fastapi import APIRouter
from prometheus_fastapi_instrumentator import Instrumentator

router = APIRouter()

@router.get("/health")
async def health_check():
    # Проверка БД, зависимостей и т.д.
    return {"status": "ok", "version": "1.0.0", "uptime": "99.99%"}

def setup_prometheus(app: FastAPI):
    if settings.ENABLE_PROMETHEUS:
        Instrumentator().instrument(app).expose(app, endpoint="/metrics")