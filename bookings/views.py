"""Страницы бронирований и статистики на основе SQL-запросов."""
import sqlite3

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
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
def bookings(request: HttpRequest) -> HttpResponse:
    """Показать активные бронирования через JOIN."""
    try:
        items = _rows("""SELECT b.id, b.booking_date, b.start_hour,
            b.end_hour, b.total_price, s.name AS studio_name,
            s.area, u.login AS user_login FROM bookings AS b
            JOIN studios AS s ON b.studio_id = s.id
            JOIN users AS u ON b.user_id = u.id
            WHERE b.is_cancelled = 0 ORDER BY b.booking_date""")
    except sqlite3.Error:
        return error_response(request, "Не удалось загрузить бронирования", 503)
    return render(request, "bookings/booking_list.html", {"bookings": items})


@require_safe
def booking_detail(request: HttpRequest, booking_id: int) -> HttpResponse:
    """Показать одну бронь с данными связанных таблиц."""
    try:
        items = _rows("""SELECT b.id, b.booking_date, b.start_hour,
            b.end_hour, b.total_price, b.is_cancelled,
            s.id AS studio_id, s.name AS studio_name, u.login AS user_login
            FROM bookings AS b JOIN studios AS s ON b.studio_id = s.id
            JOIN users AS u ON b.user_id = u.id WHERE b.id = ?""", (booking_id,))
    except sqlite3.Error:
        return error_response(request, "Не удалось загрузить бронирование", 503)
    if not items:
        return error_response(request, "Бронирование не найдено", 404)
    return render(request, "bookings/booking_detail.html", {"booking": items[0]})


@require_safe
def statistics(request: HttpRequest) -> HttpResponse:
    """Показать число активных броней по каждой студии."""
    try:
        items = _rows("""SELECT s.name AS studio_name,
            COUNT(b.id) AS bookings_count FROM studios AS s
            LEFT JOIN bookings AS b ON s.id = b.studio_id
            AND b.is_cancelled = 0 GROUP BY s.id, s.name
            ORDER BY bookings_count DESC, s.name""")
    except sqlite3.Error:
        return error_response(request, "Не удалось загрузить статистику", 503)
    return render(request, "bookings/statistics.html", {"statistics": items})
