# main.py

from fastapi import FastAPI
from config.settings import settings
from config.logging import configure_logging
from security.headers import setup_security_middlewares, limiter
from monitoring.health import router as health_router, setup_prometheus
from api.v1.auth import router as auth_router

# Настройка логирования
logger = configure_logging()

app = FastAPI(
    title="TSD Terminal API",
    description="Сервер для инвентаризации оборудования",
    version="1.0.0",
    docs_url="/docs" if not settings.TESTING else None,
    redoc_url="/redoc" if not settings.TESTING else None,
)

# Подключаем безопасность
setup_security_middlewares(app, settings)

# Подключаем мониторинг
setup_prometheus(app)

# Подключаем роутеры
app.include_router(health_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1/auth")

@app.on_event("startup")
async def startup():
    logger.info("🚀 Starting TSD Terminal Server...")
    # Здесь можно добавить проверку целостности БД, миграции и т.д.

@app.on_event("shutdown")
async def shutdown():
    logger.info("🛑 Shutting down TSD Terminal Server...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=settings.TESTING,
        ssl_keyfile="key.pem" if not settings.TESTING else None,
        ssl_certfile="cert.pem" if not settings.TESTING else None,
    )