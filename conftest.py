"""Настройка Django для pytest без базы данных и pytest-django."""

import os

import django
import pytest
from django.test import Client, override_settings

from models.bookings import Booking
from models.studios import Studio
from models.users import User
from storage import save_bookings, save_studios, save_users

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "photostudio.settings")
django.setup()


@pytest.fixture
def web_client(tmp_path):
    """Изолированные JSON для HTTP-тестов; реальные данные не меняются."""
    studio = Studio(1, 'Свет <script>alert(1)</script>', 50, 1000)
    user = User(1, "ivan", "hidden-password")
    active = Booking(1, studio, user, "2026-10-03", 14, 16)
    cancelled = Booking(2, studio, user, "2026-10-03", 16, 18)
    cancelled.cancel()
    save_studios(tmp_path / "studios.json", [studio])
    save_users(tmp_path / "users.json", [user])
    save_bookings(tmp_path / "date_of_booking.json", [active, cancelled])
    with override_settings(DATA_DIR=tmp_path, ALLOWED_HOSTS=["testserver"]):
        yield Client()
