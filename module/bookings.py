"""Совместимость импортов ПР3; реализация в models.bookings."""

from models.bookings import (
    Booking,
    is_available,
    create_booking,
    cancel_booking,
)

__all__ = [
    "Booking",
    "is_available",
    "create_booking",
    "cancel_booking",
]
