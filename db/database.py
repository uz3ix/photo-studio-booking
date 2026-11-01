"""Подключение к SQLite и небольшие операции с базой."""
from pathlib import Path
import sqlite3

from django.conf import settings


def get_connection(db_path: Path | None = None) -> sqlite3.Connection:
    """Создать соединение с включённой проверкой внешних ключей."""
    path = db_path or settings.SQLITE_DB_PATH
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(db_path: Path | None = None) -> None:
    """Создать таблицы по SQL-схеме, если их ещё нет."""
    schema_path = Path(__file__).parent.parent / "sql" / "schema.sql"
    connection = get_connection(db_path)
    try:
        connection.executescript(schema_path.read_text(encoding="utf-8"))
        connection.commit()
    finally:
        connection.close()
