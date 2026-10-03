"""Пользователь, регистрация и авторизация."""


class User:
    """Пользователь; техническая архивная запись не допускает вход."""

    def __init__(self, user_id: int, login: str, password: str,
                 is_active: bool = True) -> None:
        """Создать пользователя, не раскрывая пароль при выводе."""
        if user_id <= 0 or not login.strip():
            raise ValueError("Укажите положительный ID и логин")
        if is_active and not password.strip():
            raise ValueError("Пароль не должен быть пустым")
        self.id = user_id
        self.login = login.strip()
        self._password = password
        self.is_active = is_active

    def check_password(self, password: str) -> bool:
        """Проверить пароль и возможность входа."""
        return self.is_active and self._password == password

    def to_data(self) -> dict:
        """Подготовить данные для учебного JSON-хранилища."""
        return {"id": self.id, "login": self.login,
                "password": self._password, "is_active": self.is_active}

    def __str__(self) -> str:
        """Вернуть идентификатор и логин без пароля."""
        return f"{self.id}. {self.login}"


def register_user(users: list[User], login: str, password: str) -> User:
    """Добавить пользователя с уникальным логином."""
    login = login.strip()
    if any(user.login == login for user in users):
        raise ValueError("Такой логин уже зарегистрирован")
    user = User(max((u.id for u in users), default=0) + 1, login, password)
    users.append(user)
    return user


def authorisation(users: list[User], login: str, password: str) -> User:
    """Найти пользователя и проверить пароль методом объекта."""
    for user in users:
        if user.login == login and user.check_password(password):
            return user
    raise ValueError("Неверный логин или пароль")
