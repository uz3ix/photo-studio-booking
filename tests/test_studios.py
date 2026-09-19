"""Проверки объектов студий и функций каталога."""

import pytest

from module.studios import (
    Studio, add_studio, filter_studios_by_price, get_studio,
    search_studios, sort_studios_by_price,
)


def test_studio():
    studio = Studio(1, " Свет ", 50, 1000)
    assert (studio.id, studio.name, studio.area) == (1, "Свет", 50)
    assert studio.calculate_price(3) == 3000
    assert str(studio) == "1. Свет: 50 м², 1000 руб./час"


def test_price_invalid():
    with pytest.raises(ValueError):
        Studio(1, "Свет", 50, 1000).calculate_price(0)


def test_add_studio():
    studios = [Studio(7, "Лофт", 60, 2000)]
    result = add_studio(studios, " Свет ", 50, 1000)
    assert studios[-1] is result
    assert (result.id, result.name) == (8, "Свет")


@pytest.mark.parametrize("name,area,price", [
    (" ", 50, 1000), ("Свет", 0, 1000), ("Свет", 50, -1),
])
def test_add_studio_invalid(name, area, price):
    studios = []
    with pytest.raises(ValueError):
        add_studio(studios, name, area, price)
    assert studios == []


def test_search_studios():
    studios = [Studio(1, "Свет", 50, 1000), Studio(2, "Лофт", 60, 2000)]
    assert search_studios(studios, "СВЕТ") == [studios[0]]
    assert search_studios(studios, "море") == []


def test_get_studio():
    studio = Studio(7, "Свет", 50, 1000)
    assert get_studio([studio], 7) is studio


def test_get_studio_missing():
    with pytest.raises(ValueError, match="не найдена"):
        get_studio([], 1)


def test_filter_studios_by_price():
    studios = [Studio(1, "Свет", 50, 1000), Studio(2, "Лофт", 60, 1500)]
    assert filter_studios_by_price(studios, 1000) == [studios[0]]


def test_sort_studios_by_price():
    studios = [Studio(1, "Лофт", 50, 1500), Studio(2, "Свет", 50, 1000)]
    assert sort_studios_by_price(studios) == [studios[1], studios[0]]
    assert studios[0].price_per_hour == 1500
