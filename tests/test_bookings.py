"""Проверки основных правил бронирования."""

import pytest

from module.bookings import create_booking, is_available


def existing_bookings() -> list[dict]:
    """Вернуть независимый набор записей для проверки."""
    return [{"id": 1, "studio_id": 1, "booking_date": "2026-09-21",
             "start_hour": 14, "end_hour": 16}]


def test_free_interval():
    assert is_available(existing_bookings(), 1, "2026-09-21", 9, 12)


def test_overlap_rejected():
    studio = {"id": 1, "price_per_hour": 1000}
    bookings = existing_bookings()
    with pytest.raises(ValueError, match="занят"):
        create_booking(bookings, studio, "ivan", "2026-09-21", 15, 17)
    assert len(bookings) == 1


def test_adjacent_interval():
    assert is_available(existing_bookings(), 1, "2026-09-21", 16, 18)


def test_other_studio():
    assert is_available(existing_bookings(), 2, "2026-09-21", 14, 16)


def test_create_booking():
    bookings = existing_bookings()
    studio = {"id": 1, "price_per_hour": 1000}
    booking = create_booking(bookings, studio, "ivan", "2026-09-21", 9, 12)
    assert booking["total_price"] == 3000
    assert booking["id"] == 2
    assert booking["login"] == "ivan"
    assert bookings[-1] == booking
