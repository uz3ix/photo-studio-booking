"""Проверки пользователя, регистрации и авторизации."""

import pytest

from module.users import User, authorisation, register_user


def test_user():
    user = User(1, "ivan", "secret")
    assert user.id == 1
    assert str(user) == "1. ivan"
    assert user.check_password("secret")
    assert not user.check_password("wrong")
    assert user.to_data() == {
        "id": 1, "login": "ivan", "password": "secret", "is_active": True,
    }


def test_archived_user():
    user = User(3, "archive_pr2", "", False)
    assert not user.check_password("")
    with pytest.raises(ValueError):
        authorisation([user], "archive_pr2", "")


def test_register_user():
    users = []
    user = register_user(users, " ivan ", "1234")
    assert user.login == "ivan"
    assert user.id == 1
    assert users == [user]


def test_register_duplicate():
    users = [User(1, "ivan", "1234")]
    with pytest.raises(ValueError, match="зарегистрирован"):
        register_user(users, "ivan", "4321")
    assert len(users) == 1
    assert users[0].check_password("1234")


@pytest.mark.parametrize("login,password", [(" ", "123"), ("ivan", " ")])
def test_register_empty_fields(login, password):
    users = []
    with pytest.raises(ValueError):
        register_user(users, login, password)
    assert users == []


def test_authorisation():
    user = User(1, "ivan", "1234")
    assert authorisation([user], "ivan", "1234") is user


@pytest.mark.parametrize("login,password", [
    ("ivan", "wrong"), ("unknown", "1234"),
])
def test_authorisation_invalid(login, password):
    with pytest.raises(ValueError, match="Неверный"):
        authorisation([User(1, "ivan", "1234")], login, password)
