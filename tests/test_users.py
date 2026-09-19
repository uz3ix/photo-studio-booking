"""Проверки регистрации и авторизации."""

import pytest

from module.users import authorisation, register_user


def test_register_user():
    users = []
    user = register_user(users, " ivan ", "1234")
    assert user == {"login": "ivan", "password": "1234"}
    assert users == [user]


def test_register_duplicate():
    users = [{"login": "ivan", "password": "1234"}]
    with pytest.raises(ValueError, match="зарегистрирован"):
        register_user(users, "ivan", "4321")
    assert len(users) == 1
    assert users[0]["password"] == "1234"


@pytest.mark.parametrize("login,password", [(" ", "123"), ("ivan", " ")])
def test_register_empty_fields(login, password):
    users = []
    with pytest.raises(ValueError):
        register_user(users, login, password)
    assert users == []


@pytest.mark.parametrize("saved_password", ["1234", 1234])
def test_authorisation(saved_password):
    user = {"login": "ivan", "password": saved_password}
    assert authorisation([user], "ivan", "1234") == user


@pytest.mark.parametrize("login,password", [
    ("ivan", "wrong"), ("unknown", "1234"),
])
def test_authorisation_invalid(login, password):
    users = [{"login": "ivan", "password": "1234"}]
    with pytest.raises(ValueError, match="Неверный"):
        authorisation(users, login, password)
