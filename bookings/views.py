"""Просмотр связанных объектов бронирований из JSON."""
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_safe

from homepage.views import error_response
from models.bookings import Booking
from storage import load_bookings, load_studios, load_users


def booking_objects() -> list[Booking]:
    """Загрузить студии, пользователей и связи бронирований."""
    studios = load_studios(settings.DATA_DIR / "studios.json")
    users = load_users(settings.DATA_DIR / "users.json")
    return load_bookings(
        settings.DATA_DIR / "date_of_booking.json", studios, users,
    )


@require_safe
def bookings(request: HttpRequest) -> HttpResponse:
    """Показать записи и статусы без изменения данных."""
    try:
        items = booking_objects()
    except (OSError, ValueError, KeyError, TypeError):
        return error_response(
            request, "Не удалось загрузить бронирования", 503,
        )
    return render(
        request, "bookings/booking_list.html", {"bookings": items},
    )


@require_safe
def booking_detail(request: HttpRequest, booking_id: int) -> HttpResponse:
    """Показать связанную студию, клиента, интервал, цену и статус."""
    try:
        items = booking_objects()
    except (OSError, ValueError, KeyError, TypeError):
        return error_response(
            request, "Не удалось загрузить бронирования", 503,
        )
    booking = next((item for item in items if item.id == booking_id), None)
    if booking is None:
        return error_response(
            request, "Бронирование не найдено", 404,
        )
    return render(
        request, "bookings/booking_detail.html", {"booking": booking},
    )
