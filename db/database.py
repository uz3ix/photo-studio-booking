"""Подключение к SQLite для SQL-слоя проекта."""
from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "photo_studio.sqlite"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"


def get_connection(db_path: Path | None = None) -> sqlite3.Connection:
    """Создать соединение с именованными строками и внешними ключами."""
    if db_path is None:
        try:
            from django.conf import settings
            path = getattr(settings, "SQLITE_DB_PATH", DB_PATH)
        except ImportError:
            path = DB_PATH
    else:
        path = db_path
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(db_path: Path | None = None) -> None:
    """Создать таблицы по SQL-схеме, если их ещё нет."""
    connection = get_connection(db_path)
    try:
        connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        connection.commit()
    finally:
        connection.close()
