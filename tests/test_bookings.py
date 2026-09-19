"""Проверки связей объектов, пересечений и отмены."""

import pytest

from module.bookings import (
    Booking, cancel_booking, create_booking, is_available,
)
from module.studios import Studio
from module.users import User


@pytest.fixture
def studio():
    return Studio(1, "Свет", 50, 1000)


@pytest.fixture
def user():
    return User(1, "ivan", "1234")


@pytest.fixture
def booking(studio, user):
    return Booking(1, studio, user, "2026-09-21", 14, 16)


def test_booking_objects(booking, studio, user):
    assert booking.studio is studio
    assert booking.user is user
    assert booking.total_price == 2000
    assert booking.get_status() == "активна"
    assert "Свет" in str(booking)
    assert "2000 руб." in str(booking)


def test_free_interval(booking):
    assert is_available([booking], 1, "2026-09-21", 9, 12)


@pytest.mark.parametrize("start,end", [(15, 17), (14, 16), (13, 17), (14, 15)])
def test_overlap_rejected(booking, studio, user, start, end):
    bookings = [booking]
    with pytest.raises(ValueError, match="занят"):
        create_booking(bookings, studio, user, "2026-09-21", start, end)
    assert bookings == [booking]


@pytest.mark.parametrize("start,end", [(12, 14), (16, 18)])
def test_adjacent_interval(booking, start, end):
    assert is_available([booking], 1, "2026-09-21", start, end)


def test_other_studio(booking):
    assert is_available([booking], 2, "2026-09-21", 14, 16)


def test_other_date(booking):
    assert is_available([booking], 1, "2026-09-22", 14, 16)


def test_create_booking(booking, studio, user):
    bookings = [booking]
    result = create_booking(bookings, studio, user, "2026-09-21", 9, 12)
    assert result.id == 2
    assert result.total_price == 3000
    assert result.user is user
    assert bookings[-1] is result


@pytest.mark.parametrize("start,end", [(8, 10), (17, 19), (12, 12), (16, 14)])
def test_invalid_hours(studio, user, start, end):
    bookings = []
    with pytest.raises(ValueError):
        create_booking(bookings, studio, user, "2026-09-21", start, end)
    assert bookings == []


def test_invalid_date(studio, user):
    with pytest.raises(ValueError):
        create_booking([], studio, user, "2026-02-30", 9, 12)


def test_cancel_and_rebook(booking, studio, user):
    bookings = [booking]
    assert booking.overlaps(1, "2026-09-21", 14, 16)
    assert cancel_booking(bookings, 1, user) is booking
    assert booking.is_cancelled
    assert booking.get_status() == "отменена"
    assert not booking.overlaps(1, "2026-09-21", 14, 16)
    result = create_booking(bookings, studio, user, "2026-09-21", 14, 16)
    assert result.id == 2
    assert len(bookings) == 2


def test_cancel_other_user(booking):
    with pytest.raises(ValueError):
        cancel_booking([booking], 1, User(2, "anna", "1234"))
    assert not booking.is_cancelled


def test_cancel_missing(user):
    with pytest.raises(ValueError):
        cancel_booking([], 99, user)
