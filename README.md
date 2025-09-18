tsd-fastapi-server/
├── main.py                          # точка входа
├── config/                          # конфиги
│   ├── __init__.py
│   ├── settings.py                  # Pydantic-настройки с валидацией
│   └── logging.py                   # настройка structlog
├── security/                        # безопасность
│   ├── __init__.py
│   ├── auth.py                      # JWT/JWE, хеширование, зависимости
│   └── headers.py                   # middleware: HSTS, CSP, безопасные заголовки
├── database/                        # работа с БД
│   ├── __init__.py
│   ├── database.py                  # SQLCipher, инициализация, бэкапы
│   └── models.py                    # Pydantic-модели для валидации данных
├── api/                             # маршруты
│   ├── __init__.py
│   ├── deps.py                      # зависимости (например, get_current_user)
│   ├── v1/                          # версия API
│       ├── __init__.py
│       ├── auth.py                  # /login, /refresh, /logout
│       └── inventory.py             # основной функционал инвентаризации
├── monitoring/                      # мониторинг
│   ├── __init__.py
│   └── health.py                    # /health, метрики
├── utils/                           # утилиты
│   ├── __init__.py
│   └── backup.py                    # авто-бэкапы через apscheduler
├── tests/                           # тесты
│   ├── __init__.py
│   └── test_auth.py
├── .env                             # секреты (в .gitignore!)
├── requirements.txt
└── README.md