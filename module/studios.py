def add_studio(
    studios: list[dict], name: str, area: float, price_per_hour: float
) -> None:
    """Добавить студию с новым идентификатором."""
    if not name.strip() or area <= 0 or price_per_hour <= 0:
        raise ValueError("Укажите название, положительные площадь и цену")
    studios.append(
        {
            "id": max((s["id"] for s in studios), default=0) + 1,
            "name": name.strip(),
            "area": area,
            "price_per_hour": price_per_hour,
        }
    )


def search_studios(studios: list[dict], query: str) -> list[dict]:
    """Найти студии по части названия без учёта регистра."""
    return [s for s in studios if query.lower() in s["name"].lower()]


def get_studio(studios: list[dict], studio_id: int) -> dict:
    """Получить студию по идентификатору."""
    for studio in studios:
        if studio["id"] == studio_id:
            return studio
    raise ValueError("Студия с таким номером не найдена")


def filter_studios_by_price(
        studios: list[dict],
        max_price: float) -> list[dict]:
    """Выбрать студии не дороже заданной цены."""
    return [s for s in studios if s["price_per_hour"] <= max_price]


def sort_studios_by_price(studios: list[dict]) -> list[dict]:
    """Отсортировать студии по возрастанию цены."""
    return sorted(studios, key=lambda s: s["price_per_hour"])
