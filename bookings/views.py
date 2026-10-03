"""Просмотр связанных объектов бронирований из JSON."""

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.utils.html import format_html, format_html_join
from django.views.decorators.http import require_safe

from homepage.views import error_response, page
from models.bookings import Booking
from storage import load_bookings, load_studios, load_users


def booking_objects() -> list[Booking]:
    """Загрузить студии, пользователей и восстановить связи бронирований."""
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
        return error_response("Не удалось загрузить бронирования", 503)
    rows = format_html_join(
        "", '<li class="list-group-item"><a href="{}">'
        '№{} · {} · {}</a> <span class="badge {}">{}</span></li>',
        ((reverse("bookings:detail", args=[b.id]), b.id, b.studio.name,
          b.booking_date, "bg-secondary" if b.is_cancelled else "bg-success",
          b.get_status()) for b in items),
    )
    content = format_html(
        '<h1>Бронирования</h1><ul class="list-group">{}</ul>{}',
        rows, "" if items else "Бронирований пока нет.",
    )
    return HttpResponse(page("Бронирования", content))


@require_safe
def booking_detail(request: HttpRequest, booking_id: int) -> HttpResponse:
    """Показать связанную студию, клиента, интервал, цену и статус."""
    try:
        items = booking_objects()
    except (OSError, ValueError, KeyError, TypeError):
        return error_response("Не удалось загрузить бронирования", 503)
    booking = next((b for b in items if b.id == booking_id), None)
    if booking is None:
        return error_response("Бронирование не найдено", 404)
    content = format_html(
        '<article class="card"><h1>Бронирование №{}</h1>'
        '<p>Студия: <a href="{}">{}</a></p><p>Дата: {}</p>'
        '<p>Время: {}:00–{}:00</p><p>Пользователь: {}</p>'
        '<p>Стоимость: {} руб.</p><p>Статус: '
        '<span class="badge {}">{}</span></p></article>'
        '<a href="{}">← К бронированиям</a>',
        booking.id, reverse("studios:detail", args=[booking.studio.id]),
        booking.studio.name, booking.booking_date, booking.start_hour,
        booking.end_hour, booking.user.login, booking.total_price,
        "bg-secondary" if booking.is_cancelled else "bg-success",
        booking.get_status(), reverse("bookings:list"),
    )
    return HttpResponse(page(f"Бронирование №{booking.id}", content))
