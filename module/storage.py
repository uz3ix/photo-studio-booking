"""Преобразование JSON в связанные объекты и обратно."""

import json
from pathlib import Path

from module.bookings import Booking
from module.studios import Studio, get_studio
from module.users import User


def load_json(filename: Path) -> list[dict]:
    """Прочитать список словарей, не скрывая повреждение файла."""
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise ValueError(f"В файле {filename.name} ожидается список")
    if not all(isinstance(item, dict) for item in data):
        raise ValueError(f"В файле {filename.name} ожидаются словари")
    return data


def save_json(filename: Path, data: list[dict]) -> None:
    """Атомарно заменить файл, сохранив исходный при ошибке записи."""
    temporary = filename.with_suffix(filename.suffix + ".tmp")
    try:
        with open(temporary, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
            file.write("\n")
        temporary.replace(filename)
    finally:
        if temporary.exists():
            temporary.unlink()


def load_studios(filename: Path) -> list[Studio]:
    """Восстановить студии из записей JSON."""
    return [Studio(s["id"], s["name"], s["area"], s["price_per_hour"])
            for s in load_json(filename)]


def save_studios(filename: Path, studios: list[Studio]) -> None:
    """Сохранить характеристики студий."""
    save_json(filename, [
        {"id": s.id, "name": s.name, "area": s.area,
         "price_per_hour": s.price_per_hour} for s in studios
    ])


def load_users(filename: Path) -> list[User]:
    """Восстановить пользователей, включая числовые пароли ПР2."""
    return [User(u["id"], u["login"], str(u["password"]),
                 u.get("is_active", True)) for u in load_json(filename)]


def save_users(filename: Path, users: list[User]) -> None:
    """Сохранить пользователей в учебном формате."""
    save_json(filename, [u.to_data() for u in users])


def load_bookings(filename: Path, studios: list[Studio],
                  users: list[User]) -> list[Booking]:
    """Связать брони с существующими студиями и пользователями."""
    bookings = []
    for record in load_json(filename):
        studio = get_studio(studios, record["studio_id"])
        user = next((u for u in users if u.id == record["user_id"]), None)
        if user is None:
            raise ValueError("Пользователь бронирования не найден")
        bookings.append(Booking(
            record["id"], studio, user, record["booking_date"],
            record["start_hour"], record["end_hour"],
            record.get("is_cancelled", False), record.get("total_price"),
        ))
    return bookings


def save_bookings(filename: Path, bookings: list[Booking]) -> None:
    """Сохранить ссылки как ID, а не вложенные Python-объекты."""
    save_json(filename, [
        {"id": b.id, "studio_id": b.studio.id, "user_id": b.user.id,
         "booking_date": b.booking_date, "start_hour": b.start_hour,
         "end_hour": b.end_hour, "is_cancelled": b.is_cancelled,
         "total_price": b.total_price} for b in bookings
    ])
