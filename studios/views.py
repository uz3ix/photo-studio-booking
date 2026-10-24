"""Список фотостудий и карточка с расписанием на сегодня."""
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_safe

from homepage.views import error_response
from models.bookings import is_available
from models.studios import get_studio
from storage import load_bookings, load_studios, load_users


@require_safe
def studios(request: HttpRequest) -> HttpResponse:
    """Загрузить каталог из JSON и передать его в шаблон."""
    try:
        items = load_studios(settings.DATA_DIR / "studios.json")
    except (OSError, ValueError, KeyError, TypeError):
        return error_response(request, "Не удалось загрузить фотостудии", 503)
    return render(request, "studios/studio_list.html", {"studios": items})


@require_safe
def studio_detail(request: HttpRequest, studio_id: int) -> HttpResponse:
    """Показать характеристики и доступность каждого часового интервала."""
    try:
        items = load_studios(settings.DATA_DIR / "studios.json")
        studio = get_studio(items, studio_id)
    except ValueError:
        return error_response(request, "Фотостудия не найдена", 404)
    except (OSError, KeyError, TypeError):
        return error_response(request, "Не удалось загрузить фотостудии", 503)
    try:
        users = load_users(settings.DATA_DIR / "users.json")
        bookings = load_bookings(
            settings.DATA_DIR / "date_of_booking.json", items, users,
        )
    except (OSError, ValueError, KeyError, TypeError):
        return error_response(request, "Не удалось загрузить расписание", 503)
    today = timezone.localdate().isoformat()
    slots = []
    for hour in range(9, 18):
        slots.append({
            "start": hour,
            "end": hour + 1,
            "is_free": is_available(
                bookings, studio.id, today, hour, hour + 1,
            ),
        })
    return render(request, "studios/studio_detail.html", {
        "studio": studio,
        "today": today,
        "slots": slots,
    })
