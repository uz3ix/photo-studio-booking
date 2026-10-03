"""HTML-каркас и главная страница без шаблонов на этапе ПР5."""

from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.utils.html import format_html
from django.views.decorators.http import require_safe


def page(title: str, content: str) -> str:
    """Общий HTML; данные экранируются, разметка передаётся как SafeString."""
    return format_html(
        """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{}</title>
<link rel="stylesheet"
 href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
<style>
body {{ background:#f4f5f7; color:#182335; margin:0; font-family:Arial; }}
.container {{ max-width:1080px; margin:auto; padding:24px; }}
nav {{ background:#182335; }}
nav a {{ color:white; display:inline-block; padding:12px; }}
a {{ color:#2758a5; }}
h1 {{ margin:0 0 24px; }}
.card,.list-group-item {{ background:white; padding:20px;
 border:1px solid #dce1e8; border-radius:10px; margin-bottom:12px; }}
.badge {{ display:inline-block; padding:6px 10px; border-radius:6px; }}
.bg-success {{ background:#176d4b!important; color:white; }}
.bg-secondary {{ background:#596575!important; color:white; }}
.bg-danger {{ background:#ae3340!important; color:white; }}
.hero {{ padding:40px 0; }}
footer {{ padding:24px; color:#596575; }}
</style>
</head>
<body>
<nav aria-label="Основная навигация"><div class="container">
<a href="{}">Фотостудии</a><a href="{}">Каталог</a>
<a href="{}">Бронирования</a>
</div></nav>
<main class="container">{}</main>
<footer class="container">Система бронирования фотостудий</footer>
</body></html>""",
        title, reverse("homepage:index"), reverse("studios:list"),
        reverse("bookings:list"), content,
    )


def error_response(title: str, status: int) -> HttpResponse:
    """Вернуть оформленную страницу ошибки с навигацией."""
    content = format_html(
        '<h1>{}</h1><p><a href="{}">На главную</a></p>',
        title, reverse("homepage:index"),
    )
    return HttpResponse(page(title, content), status=status)


@require_safe
def index(request: HttpRequest) -> HttpResponse:
    """Показать назначение сервиса и ссылки на разделы."""
    content = format_html(
        """<section class="hero">
<p class="text-uppercase text-secondary">Пространство для ваших идей</p>
<h1>Найдите студию для следующей съёмки</h1>
<p class="lead">Сравните площадь и стоимость залов,
посмотрите расписание и информацию о бронированиях.</p>
<a class="btn btn-primary" href="{}">Посмотреть фотостудии</a>
</section>
<section class="card"><h2>Ваши планы на съёмку</h2>
<p>Дата, студия, время и статус — в списке бронирований.</p>
<a href="{}">Открыть бронирования →</a></section>""",
        reverse("studios:list"), reverse("bookings:list"),
    )
    return HttpResponse(page("Система бронирования фотостудий", content))
