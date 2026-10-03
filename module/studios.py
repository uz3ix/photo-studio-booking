"""Совместимость импортов ПР3; реализация в models.studios."""

from models.studios import (
    Studio,
    add_studio,
    search_studios,
    get_studio,
    filter_studios_by_price,
    sort_studios_by_price,
)

__all__ = [
    "Studio",
    "add_studio",
    "search_studios",
    "get_studio",
    "filter_studios_by_price",
    "sort_studios_by_price",
]
