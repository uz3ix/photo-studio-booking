"""Каталог студий и SQL-поиск свободных студий."""
import sqlite3

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_safe

from db.database import get_connection
from homepage.views import error_response


def _rows(sql: str, params=()):
    connection = get_connection(settings.SQLITE_DB_PATH)
    try:
        return connection.execute(sql, params).fetchall()
    finally:
        connection.close()


@require_safe
def studios(request: HttpRequest) -> HttpResponse:
    """Показать список студий, полученный запросом SELECT."""
    try:
        items = _rows("""SELECT id, name, area, price_per_hour
                       FROM studios ORDER BY name""")
    except sqlite3.Error:
        return error_response(request, "Не удалось загрузить фотостудии", 503)
    return render(request, "studios/studio_list.html", {"studios": items})


@require_safe
def studio_detail(request: HttpRequest, studio_id: int) -> HttpResponse:
    """Показать студию и расписание на сегодня из SQLite."""
    try:
        studio = _rows(
            "SELECT id, name, area, price_per_hour FROM studios WHERE id = ?",
            (studio_id,),
        )
        if not studio:
            return error_response(request, "Фотостудия не найдена", 404)
        studio = studio[0]
        today = timezone.localdate().isoformat()
        busy = _rows("""SELECT start_hour, end_hour FROM bookings
                      WHERE studio_id = ? AND booking_date = ?
                      AND is_cancelled = 0""", (studio_id, today))
    except sqlite3.Error:
        return error_response(request, "Не удалось загрузить расписание", 503)
    slots = []
    for hour in range(9, 18):
        slots.append({
            "start": hour,
            "end": hour + 1,
            "is_free": not any(
                row["start_hour"] <= hour < row["end_hour"] for row in busy
            ),
        })
    return render(request, "studios/studio_detail.html", {
        "studio": studio, "today": today, "slots": slots,
    })


@require_safe
def available_studios(request: HttpRequest) -> HttpResponse:
    """Найти студии без активной брони на дату параметризованным SQL."""
    booking_date = request.GET.get("date", "")
    items = []
    if booking_date:
        try:
            items = _rows("""SELECT s.id, s.name, s.area
                FROM studios AS s WHERE NOT EXISTS (
                SELECT 1 FROM bookings AS b WHERE b.studio_id = s.id
                AND b.booking_date = ? AND b.is_cancelled = 0)
                ORDER BY s.name""", (booking_date,))
        except sqlite3.Error:
            return error_response(request, "Не удалось выполнить поиск", 503)
    return render(request, "studios/available.html", {
        "studios": items, "booking_date": booking_date,
    })
