"""Проверки вывода и меню без изменения данных проекта."""

import json

import pytest

import main as app


@pytest.fixture
def studio():
    return {"id": 1, "name": "Свет", "area": 50, "price_per_hour": 1000}


def test_show_studios(studio, capsys):
    app.show_studios([studio])
    output = capsys.readouterr().out
    assert "Свет" in output
    assert "50 м²" in output
    assert "1000 руб./час" in output


def test_show_studios_empty(capsys):
    app.show_studios([])
    assert "Студии не найдены" in capsys.readouterr().out


def test_choose_date_of_booking(monkeypatch, capsys):
    answers = iter(["2026.09.21", "16", "18"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    bookings = [{"studio_id": 1, "booking_date": "2026-09-21",
                 "start_hour": 14, "end_hour": 16}]
    assert app.choose_date_of_booking(bookings, 1) == (
        "2026-09-21", 16, 18,
    )
    output = capsys.readouterr().out
    assert "14:00–15:00 — занято" in output
    assert "15:00–16:00 — занято" in output
    assert "16:00–17:00 — свободно" in output


def test_show_bookings(studio, capsys):
    booking = {"id": 1, "studio_id": 1, "login": "ivan",
               "booking_date": "2026-09-21", "start_hour": 14,
               "end_hour": 16, "total_price": 2000}
    other = dict(booking, id=2, login="anna")
    app.show_bookings([booking, other], [studio], "ivan")
    output = capsys.readouterr().out
    assert "№1: Свет" in output
    assert "2000 руб." in output
    assert "№2" not in output


def test_show_bookings_empty(capsys):
    app.show_bookings([], [], "ivan")
    assert "пока нет бронирований" in capsys.readouterr().out


def test_main_registration_and_booking(tmp_path, monkeypatch, capsys,
                                       studio):
    for filename, data in [
        ("users.json", []), ("studios.json", [studio]),
        ("date_of_booking.json", []),
    ]:
        (tmp_path / filename).write_text(json.dumps(data), encoding="utf-8")
    monkeypatch.setattr(app, "DATA_DIR", tmp_path)
    answers = iter([
        "2", "ivan", "1234", "4", "1", "2026.09.21", "14", "16",
        "4", "1", "2026.09.21", "15", "17", "5", "0",
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    app.main()
    bookings = json.loads(
        (tmp_path / "date_of_booking.json").read_text(encoding="utf-8")
    )
    assert len(bookings) == 1
    assert bookings[0]["total_price"] == 2000
    assert bookings[0]["login"] == "ivan"
    users = json.loads((tmp_path / "users.json").read_text(encoding="utf-8"))
    assert users == [{"login": "ivan", "password": "1234"}]
    assert "уже занят" in capsys.readouterr().out

    # Повторный запуск проверяет вход по сохранённым данным.
    answers = iter(["1", "ivan", "1234", "5", "0"])
    app.main()
    assert "№1: Свет" in capsys.readouterr().out


def test_main_missing_data(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(app, "DATA_DIR", tmp_path)
    app.main()
    assert "Не удалось загрузить данные" in capsys.readouterr().out
