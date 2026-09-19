"""Проверки вывода и меню на временных данных."""

import json

import pytest

import main as app
from module.bookings import Booking
from module.storage import save_bookings, save_studios, save_users
from module.studios import Studio
from module.users import User


@pytest.fixture
def studio():
    return Studio(1, "Свет", 50, 1000)


def test_show_studios(studio, capsys):
    app.show_studios([studio])
    output = capsys.readouterr().out
    assert "Свет" in output
    assert "50 м²" in output
    assert "1000 руб./час" in output


def test_show_studios_empty(capsys):
    app.show_studios([])
    assert "Студии не найдены" in capsys.readouterr().out


def test_choose_date_of_booking(monkeypatch, capsys, studio):
    answers = iter(["2026.09.21", "16", "18"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    user = User(1, "ivan", "1234")
    bookings = [Booking(1, studio, user, "2026-09-21", 14, 16)]
    assert app.choose_date_of_booking(bookings, 1) == (
        "2026-09-21", 16, 18,
    )
    output = capsys.readouterr().out
    assert "14:00–15:00 — занято" in output
    assert "15:00–16:00 — занято" in output
    assert "16:00–17:00 — свободно" in output


def test_show_bookings(studio, capsys):
    user = User(1, "ivan", "1234")
    other = User(2, "anna", "1234")
    bookings = [
        Booking(1, studio, user, "2026-09-21", 14, 16),
        Booking(2, studio, other, "2026-09-22", 14, 16),
    ]
    app.show_bookings(bookings, user)
    output = capsys.readouterr().out
    assert "№1: Свет" in output
    assert "2000 руб." in output
    assert "№2" not in output


def test_show_bookings_empty(capsys):
    app.show_bookings([], User(1, "ivan", "1234"))
    assert "пока нет бронирований" in capsys.readouterr().out


def test_main_registration_and_booking(tmp_path, monkeypatch, capsys,
                                       studio):
    save_users(tmp_path / "users.json", [])
    save_studios(tmp_path / "studios.json", [studio])
    save_bookings(tmp_path / "date_of_booking.json", [])
    monkeypatch.setattr(app, "DATA_DIR", tmp_path)
    answers = iter([
        "2", "ivan", "1234", "1", "2", "Свет", "3", "1", "6",
        "4", "1", "2026.09.21", "14", "16",
        "4", "1", "2026.09.21", "15", "17", "5",
        "7", "1", "4", "1", "2026.09.21", "14", "16", "0",
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    app.main()
    bookings = json.loads(
        (tmp_path / "date_of_booking.json").read_text(encoding="utf-8")
    )
    assert len(bookings) == 2
    assert bookings[0]["is_cancelled"]
    assert not bookings[1]["is_cancelled"]
    assert bookings[1]["total_price"] == 2000
    assert bookings[1]["user_id"] == 1
    assert "уже занят" in capsys.readouterr().out
    answers = iter(["1", "ivan", "1234", "5", "0"])
    app.main()
    output = capsys.readouterr().out
    assert "№1: Свет" in output and "отменена" in output
    assert "№2: Свет" in output and "активна" in output


def test_main_missing_data(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(app, "DATA_DIR", tmp_path)
    app.main()
    assert "Не удалось загрузить данные" in capsys.readouterr().out


@pytest.mark.parametrize("action", ["create", "cancel"])
def test_failed_save_keeps_state(
    tmp_path, monkeypatch, capsys, studio, action,
):
    user = User(1, "ivan", "1234")
    original = Booking(1, studio, user, "2026-09-21", 14, 16)
    save_users(tmp_path / "users.json", [user])
    save_studios(tmp_path / "studios.json", [studio])
    path = tmp_path / "date_of_booking.json"
    save_bookings(path, [original])
    before = path.read_bytes()
    monkeypatch.setattr(app, "DATA_DIR", tmp_path)

    def fail_save(*args):
        raise OSError("Нет доступа к файлу")

    monkeypatch.setattr(app, "save_bookings", fail_save)
    operation = (["4", "1", "2026.09.21", "16", "18"]
                 if action == "create" else ["7", "1"])
    answers = iter(["1", "ivan", "1234"] + operation + ["5", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    app.main()
    output = capsys.readouterr().out
    assert "Нет доступа к файлу" in output
    assert "сохранена" not in output
    assert "отменено" not in output
    assert "№2:" not in output
    assert "отменена" not in output
    assert path.read_bytes() == before
