"""Совместимость импортов ПР3; реализация в storage."""

from storage import (
    load_json,
    save_json,
    load_studios,
    save_studios,
    load_users,
    save_users,
    load_bookings,
    save_bookings,
)

__all__ = [
    "load_json",
    "save_json",
    "load_studios",
    "save_studios",
    "load_users",
    "save_users",
    "load_bookings",
    "save_bookings",
]
