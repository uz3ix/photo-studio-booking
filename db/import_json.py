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
    """Заменить содержимое SQLite данными студий, пользователей и броней."""
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
            "INSERT INTO studios VALUES (?, ?, ?, ?)",
            [(x["id"], x["name"], x["area"], x["price_per_hour"])
             for x in studios],
        )
        connection.executemany(
            "INSERT INTO users VALUES (?, ?, ?, ?)",
            [(x["id"], x["login"], x.get("password", ""),
              int(x.get("is_active", True))) for x in users],
        )
        connection.executemany(
            "INSERT INTO bookings VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
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
    from django.conf import settings
    import django
    django.setup()
    import_json(settings.DATA_DIR, settings.SQLITE_DB_PATH)


if __name__ == "__main__":
    main()
