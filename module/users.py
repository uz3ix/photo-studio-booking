def register_user(users: list[dict], login: str, password: str) -> dict:
    """Добавить пользователя с уникальным непустым логином."""
    login = login.strip()
    if not login or not password.strip():
        raise ValueError("Логин и пароль не должны быть пустыми")
    if any(user["login"] == login for user in users):
        raise ValueError("Такой логин уже зарегистрирован")
    user = {"login": login, "password": password}
    users.append(user)
    return user


def authorisation(users: list[dict], login: str, password: str) -> dict:
    """Проверить данные входа, включая числовые пароли из ПР1."""
    for user in users:
        if user["login"] == login and str(user["password"]) == password:
            return user
    raise ValueError("Неверный логин или пароль")
