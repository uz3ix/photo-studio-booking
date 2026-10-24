"""HTTP-проверки главной страницы."""
import pytest
from django.contrib.staticfiles import finders
from django.test.utils import setup_test_environment, teardown_test_environment
from django.urls import reverse


def test_homepage(web_client):
    response = web_client.get(reverse("homepage:index"))
    assert response.status_code == 200
    assert "text/html" in response["Content-Type"]
    html = response.content.decode()
    assert 'lang="ru"' in html
    assert 'name="viewport"' in html
    assert "bootstrap" in html
    assert 'href="/studios/"' in html
    assert 'href="/bookings/"' in html


def test_unknown_url(web_client):
    assert web_client.get("/missing/").status_code == 404


def test_homepage_rejects_post(web_client):
    assert web_client.post("/").status_code == 405


@pytest.mark.parametrize("url, template", [
    ("/", "homepage/index.html"),
    ("/studios/", "studios/studio_list.html"),
    ("/studios/1/", "studios/studio_detail.html"),
    ("/bookings/", "bookings/booking_list.html"),
    ("/bookings/1/", "bookings/booking_detail.html"),
])
def test_pages_use_templates_and_static(web_client, url, template):
    setup_test_environment()
    try:
        response = web_client.get(url)
        names = {item.name for item in response.templates}
        assert template in names
        assert "base.html" in names
        assert "includes/navigation.html" in names
        html = response.content.decode()
        for asset in ("css/style.css", "js/main.js", "img/logo.svg"):
            assert f"/static/homepage/{asset}" in html
            assert finders.find(f"homepage/{asset}")
    finally:
        teardown_test_environment()


@pytest.mark.parametrize("url", ["/studios/99/", "/bookings/99/"])
def test_error_page_uses_base_template(web_client, url):
    setup_test_environment()
    try:
        response = web_client.get(url)
        assert response.status_code == 404
        assert "base.html" in {item.name for item in response.templates}
    finally:
        teardown_test_environment()
