"""Главная страница и общая обработка ошибок через шаблоны."""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_safe


def error_response(
    request: HttpRequest, title: str, status: int,
) -> HttpResponse:
    """Вернуть страницу ошибки с общей навигацией."""
    return render(request, "error.html", {"title": title}, status=status)


@require_safe
def index(request: HttpRequest) -> HttpResponse:
    """Показать назначение сервиса и ссылки на разделы."""
    return render(request, "homepage/index.html")
