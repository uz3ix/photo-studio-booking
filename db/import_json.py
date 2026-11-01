"""Перенос исходных JSON-файлов проекта в SQLite."""
import json
from pathlib import Path
import sqlite3

from db.database import get_connection, initialize_database


def load_json(path: Path):
    """Загрузить JSON-массив."""
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def import_json(data_dir: Path, db_path: Path | None = None) -> None:
    """Заменить содержимое SQLite данными студий, пользователей и броней.

    Таблицы очищаются в порядке от зависимых к главным, а вставка выполняется
    в порядке внешних ключей: studios, users, bookings.
    """
    initialize_database(db_path)
    studios = load_json(data_dir / "studios.json")
    users = load_json(data_dir / "users.json")
    bookings = load_json(data_dir / "date_of_booking.json")
    connection = get_connection(db_path)
    try:
        connection.execute("DELETE FROM bookings")
        connection.execute("DELETE FROM users")
        connection.execute("DELETE FROM studios")
        connection.executemany(
            """INSERT INTO studios
               (id, name, area, price_per_hour)
               VALUES (?, ?, ?, ?)""",
            [(x["id"], x["name"], x["area"], x["price_per_hour"])
             for x in studios],
        )
        connection.executemany(
            """INSERT INTO users
               (id, login, password, is_active)
               VALUES (?, ?, ?, ?)""",
            [(x["id"], x["login"], x.get("password", ""),
              int(x.get("is_active", True))) for x in users],
        )
        connection.executemany(
            """INSERT INTO bookings
               (id, studio_id, user_id, booking_date, start_hour,
                end_hour, is_cancelled, total_price)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            [(x["id"], x["studio_id"], x["user_id"], x["booking_date"],
              x["start_hour"], x["end_hour"], int(x["is_cancelled"]),
              x["total_price"]) for x in bookings],
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def main() -> None:
    """Импортировать данные из каталога data."""
    try:
        from django.conf import settings
        import django
        django.setup()
        data_dir = settings.DATA_DIR
        db_path = settings.SQLITE_DB_PATH
    except ImportError:
        from db.database import BASE_DIR, DB_PATH
        data_dir = BASE_DIR / "data"
        db_path = DB_PATH
    import_json(data_dir, db_path)


if __name__ == "__main__":
    main()
