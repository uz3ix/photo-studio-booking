"""Проверки ввода: monkeypatch заменяет ответы пользователя."""

from datetime import date

import pytest

from module.utils import input_date, input_int, input_range


def test_input_int(monkeypatch, capsys):
    answers = iter(["abc", " 12 "])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    assert input_int("Число: ") == 12
    assert "Нужно целое число" in capsys.readouterr().out


def test_input_date(monkeypatch, capsys):
    answers = iter(["2026.02.30", "wrong", "2026.09.21"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    assert input_date("Дата: ") == date(2026, 9, 21)
    assert capsys.readouterr().out.count("Неверный формат") == 2


@pytest.mark.parametrize("valid", [9, 18])
def test_input_range(monkeypatch, capsys, valid):
    answers = iter(["8", "19", str(valid)])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    assert input_range("Час: ", 9, 18) == valid
    assert capsys.readouterr().out.count("Число должно быть") == 2
