"""HTTP-проверки главной страницы."""

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
