# database/database.py

import sqlite3
import os
from pathlib import Path
from apscheduler.schedulers.background import BackgroundScheduler
from config.settings import settings
import datetime

class DatabaseManager:
    def __init__(self, db_name: str = None):
        self.db_name = db_name or settings.DB_NAME
        self.db_path = settings.DATA_DIR / self.db_name
        self.connection = None
        self._initialize_database()

    def _initialize_database(self):
        """Подключение с SQLCipher и инициализация структуры"""
        self.connection = sqlite3.connect(str(self.db_path))
        
        # 🔐 Включаем шифрование (SQLCipher)
        self.connection.execute(f"PRAGMA key = '{settings.ENCRYPTION_KEY}'")
        
        # WAL mode для производительности
        if settings.DB_WAL_MODE:
            self.connection.execute("PRAGMA journal_mode=WAL")
        
        # Создаём таблицы
        self._create_tables()
        
        # Запускаем авто-бэкапы
        self._setup_backup_scheduler()

    def _create_tables(self):
        self.connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.connection.commit()

    def _setup_backup_scheduler(self):
        """Авто-бэкапы раз в день"""
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.backup_database, 'interval', days=1)
        scheduler.start()

    def backup_database(self):
        """Создание зашифрованной копии БД"""
        backup_path = settings.BACKUP_DIR / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        backup_conn = sqlite3.connect(str(backup_path))
        backup_conn.execute(f"PRAGMA key = '{settings.ENCRYPTION_KEY}'")
        with backup_conn:
            self.connection.backup(backup_conn)
        backup_conn.close()
        print(f"✅ Backup created: {backup_path}")

    # ... остальные методы (execute_query, fetch_all и т.д. — как раньше, но с PRAGMA key)