"""Список фотостудий и карточка с расписанием на сегодня."""

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html, format_html_join
from django.views.decorators.http import require_safe

from homepage.views import error_response, page
from models.bookings import is_available
from models.studios import get_studio
from storage import load_bookings, load_studios, load_users


@require_safe
def studios(request: HttpRequest) -> HttpResponse:
    """Загрузить каталог из JSON через классы ПР3."""
    try:
        items = load_studios(settings.DATA_DIR / "studios.json")
    except (OSError, ValueError, KeyError, TypeError):
        return error_response("Не удалось загрузить фотостудии", 503)
    cards = format_html_join(
        "", '<li class="list-group-item"><h2><a href="{}">{}</a></h2>'
        '<p>Площадь: {} м² · {} руб./час</p></li>',
        ((reverse("studios:detail", args=[s.id]), s.name, s.area,
          s.price_per_hour) for s in items),
    )
    content = format_html(
        '<h1>Фотостудии</h1><ul class="list-group">{}</ul>{}',
        cards, "" if items else "Фотостудии пока не добавлены.",
    )
    return HttpResponse(page("Каталог фотостудий", content))


@require_safe
def studio_detail(request: HttpRequest, studio_id: int) -> HttpResponse:
    """Показать характеристики и доступность каждого часового интервала."""
    try:
        items = load_studios(settings.DATA_DIR / "studios.json")
    except (OSError, ValueError, KeyError, TypeError):
        return error_response("Не удалось загрузить фотостудии", 503)
    try:
        studio = get_studio(items, studio_id)
    except ValueError:
        return error_response("Фотостудия не найдена", 404)
    try:
        users = load_users(settings.DATA_DIR / "users.json")
        bookings = load_bookings(
            settings.DATA_DIR / "date_of_booking.json", items, users,
        )
    except (OSError, ValueError, KeyError, TypeError):
        return error_response("Не удалось загрузить расписание", 503)
    today = timezone.localdate().isoformat()
    slots = []
    for hour in range(9, 18):
        free = is_available(bookings, studio.id, today, hour, hour + 1)
        slots.append((hour, hour + 1, "bg-success" if free else "bg-danger",
                      "свободно" if free else "занято"))
    schedule = format_html_join(
        "", '<li class="list-group-item">{}:00–{}:00 '
        '<span class="badge {}">{}</span></li>', slots,
    )
    content = format_html(
        '<article class="card"><h1>{}</h1>'
        '<p>Площадь: {} м²</p><p>Аренда: {} руб./час</p></article>'
        '<h2>Расписание на {}</h2><ul class="list-group">{}</ul>'
        '<a href="{}">← К списку студий</a>',
        studio.name, studio.area, studio.price_per_hour,
        today, schedule, reverse("studios:list"),
    )
    return HttpResponse(page(studio.name, content))
