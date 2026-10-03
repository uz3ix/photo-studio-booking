"""Совместимость импортов ПР3; реализация в models.users."""

from models.users import (
    User,
    register_user,
    authorisation,
)

__all__ = [
    "User",
    "register_user",
    "authorisation",
]
