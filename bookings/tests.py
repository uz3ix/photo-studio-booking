"""Проверки HTTP-страниц бронирований."""

import pytest
from django.conf import settings


def test_booking_list(web_client):
    response = web_client.get("/bookings/")
    assert response.status_code == 200
    html = response.content.decode()
    assert "активна" in html and "отменена" in html
    assert 'href="/bookings/1/"' in html


def test_booking_detail(web_client):
    response = web_client.get("/bookings/1/")
    assert response.status_code == 200
    html = response.content.decode()
    assert "ivan" in html and "2000" in html
    assert 'href="/studios/1/"' in html
    assert "hidden-password" not in html
    assert "<script>alert" not in html


@pytest.mark.parametrize("url", ["/bookings/99/", "/bookings/no/"])
def test_booking_not_found(web_client, url):
    assert web_client.get(url).status_code == 404


def test_empty_bookings(web_client):
    path = settings.DATA_DIR / "date_of_booking.json"
    path.write_text("[]", encoding="utf-8")
    assert "пока нет" in web_client.get("/bookings/").content.decode()


def test_broken_reference(web_client):
    (settings.DATA_DIR / "users.json").write_text("[]", encoding="utf-8")
    assert web_client.get("/bookings/1/").status_code == 503


def test_booking_read_only(web_client):
    path = settings.DATA_DIR / "date_of_booking.json"
    before = path.read_bytes()
    assert web_client.post("/bookings/1/").status_code == 405
    web_client.get("/bookings/")
    assert path.read_bytes() == before
