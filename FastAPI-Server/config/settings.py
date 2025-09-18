# config/settings.py

from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Optional
from datetime import timedelta

class Settings(BaseSettings):
    # 🔐 Безопасность
    SECRET_KEY: str
    ENCRYPTION_KEY: str  # для SQLCipher
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10  # 600 сек = 10 мин
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # 🗃️ База данных
    DB_NAME: str = "app.db"
    DB_WAL_MODE: bool = True
    DB_ENABLE_INTEGRITY_CHECK: bool = True

    # 🌐 Сетевые настройки
    ALLOWED_ORIGINS: list[str] = ["https://tsdterminal.bytewizard.ru", "http://localhost:3000"]
    RATE_LIMIT_PER_MINUTE: int = 100

    # 📁 Пути
    BASE_DIR: Path = Path(__file__).parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    BACKUP_DIR: Path = DATA_DIR / "backups"

    # 📊 Мониторинг
    SENTRY_DSN: Optional[str] = None
    ENABLE_PROMETHEUS: bool = True

    # 🧪 Тесты
    TESTING: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "forbid"  # запрещает неизвестные поля — безопасность!

# Создаём экземпляр настроек
settings = Settings()

# Создаём директории при импорте
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.BACKUP_DIR.mkdir(parents=True, exist_ok=True)