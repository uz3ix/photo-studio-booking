"""Проверки JSON и восстановления связей на временных файлах."""

import json

import pytest

from module.bookings import Booking
from module.storage import (
    load_bookings, load_json, load_studios, load_users,
    save_bookings, save_json, save_studios, save_users,
)
from module.studios import Studio
from module.users import User


def test_load_json(tmp_path):
    path = tmp_path / "studios.json"
    path.write_text('[{"name": "Свет"}]', encoding="utf-8")
    assert load_json(path) == [{"name": "Свет"}]


def test_load_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_json(tmp_path / "missing.json")


@pytest.mark.parametrize("content", ["{broken", "{}", "[1]"])
def test_load_invalid_data(tmp_path, content):
    path = tmp_path / "invalid.json"
    path.write_text(content, encoding="utf-8")
    with pytest.raises(ValueError):
        load_json(path)
    assert path.read_text(encoding="utf-8") == content


def test_save_json(tmp_path):
    path = tmp_path / "studios.json"
    path.write_text("old content", encoding="utf-8")
    data = [{"id": 1, "name": "Свет"}]
    save_json(path, data)
    assert json.loads(path.read_text(encoding="utf-8")) == data
    assert not path.with_suffix(".json.tmp").exists()


def test_save_failure(tmp_path):
    with pytest.raises(OSError):
        save_json(tmp_path / "missing" / "data.json", [])


def test_failed_serialization_preserves_original(tmp_path):
    path = tmp_path / "data.json"
    path.write_text("[]", encoding="utf-8")
    with pytest.raises(TypeError):
        save_json(path, [{"bad": object()}])
    assert path.read_text(encoding="utf-8") == "[]"
    assert not path.with_suffix(".json.tmp").exists()


def test_studios_round_trip(tmp_path):
    path = tmp_path / "studios.json"
    save_studios(path, [Studio(1, "Свет", 50, 1000)])
    studios = load_studios(path)
    assert isinstance(studios[0], Studio)
    assert (studios[0].id, studios[0].name) == (1, "Свет")
    assert studios[0].calculate_price(2) == 2000


def test_users_round_trip(tmp_path):
    path = tmp_path / "users.json"
    save_users(path, [User(1, "ivan", "1234"), User(2, "archive", "", False)])
    users = load_users(path)
    assert users[0].check_password("1234")
    assert not users[1].is_active
    assert users[1].login == "archive"


def test_numeric_password(tmp_path):
    path = tmp_path / "users.json"
    save_json(path, [{"id": 1, "login": "ivan", "password": 1234}])
    assert load_users(path)[0].check_password("1234")


def test_bookings_round_trip(tmp_path):
    path = tmp_path / "bookings.json"
    studio = Studio(1, "Свет", 50, 1000)
    user = User(1, "ivan", "1234")
    booking = Booking(1, studio, user, "2026-09-21", 14, 16)
    booking.cancel()
    save_bookings(path, [booking])
    raw = load_json(path)[0]
    assert raw["user_id"] == user.id and raw["studio_id"] == studio.id
    studio.price_per_hour = 5000
    restored = load_bookings(path, [studio], [user])[0]
    assert restored.studio is studio
    assert restored.user is user
    assert restored.is_cancelled
    assert restored.total_price == 2000


@pytest.mark.parametrize("missing", ["studio", "user"])
def test_missing_reference(tmp_path, missing):
    path = tmp_path / "bookings.json"
    studio = Studio(1, "Свет", 50, 1000)
    user = User(1, "ivan", "1234")
    save_bookings(path, [Booking(1, studio, user, "2026-09-21", 14, 16)])
    with pytest.raises(ValueError):
        load_bookings(path, [] if missing == "studio" else [studio],
                      [] if missing == "user" else [user])
