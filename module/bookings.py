"""Бронирование связывает пользователя со студией."""

from datetime import date
from typing import Optional

from module.studios import Studio
from module.users import User


class Booking:
    """Бронь с сохранённой стоимостью и состоянием отмены."""

    def __init__(self, booking_id: int, studio: Studio, user: User,
                 booking_date: str, start_hour: int, end_hour: int,
                 is_cancelled: bool = False,
                 total_price: Optional[float] = None) -> None:
        """Проверить параметры и связать существующие объекты."""
        if booking_id <= 0:
            raise ValueError("ID брони должен быть положительным")
        date.fromisoformat(booking_date)
        if not (9 <= start_hour < end_hour <= 18):
            raise ValueError("Выберите часы с 9 до 18, начало раньше конца")
        if total_price is not None and total_price < 0:
            raise ValueError("Стоимость не может быть отрицательной")
        self.id = booking_id
        self.studio = studio
        self.user = user
        self.booking_date = booking_date
        self.start_hour = start_hour
        self.end_hour = end_hour
        self.is_cancelled = is_cancelled
        self.total_price = (
            studio.calculate_price(end_hour - start_hour)
            if total_price is None else total_price
        )

    def cancel(self) -> None:
        """Отменить бронь, сохранив её в истории."""
        self.is_cancelled = True

    def get_status(self) -> str:
        """Вернуть текстовое состояние брони."""
        return "отменена" if self.is_cancelled else "активна"

    def overlaps(self, studio_id: int, booking_date: str,
                 start_hour: int, end_hour: int) -> bool:
        """Проверить пересечение с активной бронью."""
        return (
            not self.is_cancelled and self.studio.id == studio_id
            and self.booking_date == booking_date
            and start_hour < self.end_hour and end_hour > self.start_hour
        )

    def __str__(self) -> str:
        """Показать студию, время, стоимость и статус."""
        return (f"№{self.id}: {self.studio.name}, {self.booking_date}, "
                f"{self.start_hour}:00–{self.end_hour}:00, "
                f"{self.total_price:g} руб. — {self.get_status()}")


def is_available(bookings: list[Booking], studio_id: int,
                 booking_date: str, start_hour: int, end_hour: int) -> bool:
    """Проверить коллекцию активных бронирований."""
    return not any(b.overlaps(studio_id, booking_date, start_hour, end_hour)
                   for b in bookings)


def create_booking(bookings: list[Booking], studio: Studio, user: User,
                   booking_date: str, start_hour: int,
                   end_hour: int) -> Booking:
    """Создать бронь после проверки параметров и пересечений."""
    booking = Booking(max((b.id for b in bookings), default=0) + 1,
                      studio, user, booking_date, start_hour, end_hour)
    if not is_available(bookings, studio.id, booking_date,
                        start_hour, end_hour):
        raise ValueError("Выбранный интервал уже занят")
    bookings.append(booking)
    return booking


def cancel_booking(bookings: list[Booking], booking_id: int,
                   user: User) -> Booking:
    """Отменить только собственную бронь пользователя."""
    for booking in bookings:
        if booking.id == booking_id and booking.user.id == user.id:
            booking.cancel()
            return booking
    raise ValueError("Ваша бронь с таким номером не найдена")
