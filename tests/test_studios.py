"""Проверки функций каталога фотостудий."""

import pytest

from module.studios import (
    add_studio, filter_studios_by_price, get_studio,
    search_studios, sort_studios_by_price,
)


def test_add_studio():
    studios = [{"id": 7}]
    add_studio(studios, " Свет ", 50, 1000)
    assert studios[-1] == {
        "id": 8, "name": "Свет", "area": 50, "price_per_hour": 1000,
    }


@pytest.mark.parametrize("name,area,price", [
    (" ", 50, 1000), ("Свет", 0, 1000), ("Свет", 50, -1),
])
def test_add_studio_invalid(name, area, price):
    studios = []
    with pytest.raises(ValueError):
        add_studio(studios, name, area, price)
    assert studios == []


def test_search_studios():
    studios = [{"name": "Студия Свет"}, {"name": "Лофт"}]
    assert search_studios(studios, "СВЕТ") == [studios[0]]
    assert search_studios(studios, "море") == []


def test_get_studio():
    studios = [{"id": 7, "name": "Свет"}]
    assert get_studio(studios, 7) == studios[0]


def test_get_studio_missing():
    with pytest.raises(ValueError, match="не найдена"):
        get_studio([], 1)


def test_filter_studios_by_price():
    studios = [{"price_per_hour": 1000}, {"price_per_hour": 1500}]
    assert filter_studios_by_price(studios, 1000) == [studios[0]]


def test_sort_studios_by_price():
    studios = [{"price_per_hour": 1500}, {"price_per_hour": 1000}]
    assert sort_studios_by_price(studios) == [studios[1], studios[0]]
    assert studios[0]["price_per_hour"] == 1500
