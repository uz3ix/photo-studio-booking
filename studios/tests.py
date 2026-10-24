"""Каталог, карточка, экранирование и расписание."""

from datetime import date

import pytest
from django.conf import settings


def test_studio_list(web_client):
    response = web_client.get("/studios/")
    assert response.status_code == 200
    html = response.content.decode()
    assert 'href="/studios/1/"' in html
    assert "&lt;script&gt;" in html
    assert "<script>alert" not in html


def test_schedule(web_client, monkeypatch):
    monkeypatch.setattr("studios.views.timezone.localdate",
                        lambda: date(2026, 10, 3))
    response = web_client.get("/studios/1/")
    assert response.status_code == 200
    html = response.content.decode()
    assert '14:00–15:00 <span class="badge bg-danger">занято' in html
    assert '16:00–17:00 <span class="badge bg-success">свободно' in html


@pytest.mark.parametrize("url", ["/studios/99/", "/studios/no/",
                                 "/studios/-1/"])
def test_missing_studio(web_client, url):
    assert web_client.get(url).status_code == 404


def test_empty_catalog(web_client):
    (settings.DATA_DIR / "studios.json").write_text("[]", encoding="utf-8")
    response = web_client.get("/studios/")
    assert response.status_code == 200
    assert "пока не добавлены" in response.content.decode()


def test_corrupt_catalog(web_client):
    (settings.DATA_DIR / "studios.json").write_text("{", encoding="utf-8")
    assert web_client.get("/studios/").status_code == 503


def test_studio_read_only(web_client):
    path = settings.DATA_DIR / "date_of_booking.json"
    before = path.read_bytes()
    assert web_client.post("/studios/1/").status_code == 405
    web_client.get("/studios/1/")
    assert path.read_bytes() == before


def test_studio_list_length_filter(web_client):
    html = web_client.get("/studios/").content.decode()
    assert "Всего фотостудий: 1" in html


def test_studio_card_include_and_default_filter():
    from django.template.loader import render_to_string

    html = render_to_string("studios/includes/studio_card.html", {
        "studio": {"id": 1, "name": "", "area": 50,
                   "price_per_hour": 1000},
    })
    assert "Без названия" in html
