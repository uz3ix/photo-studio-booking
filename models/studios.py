"""Фотостудия и операции с каталогом."""


class Studio:
    """Зал с характеристиками и почасовым тарифом."""

    def __init__(self, studio_id: int, name: str, area: float,
                 price_per_hour: float) -> None:
        """Создать студию с корректными характеристиками."""
        if studio_id <= 0 or not name.strip():
            raise ValueError("Укажите положительный ID и название студии")
        if area <= 0 or price_per_hour <= 0:
            raise ValueError("Площадь и цена должны быть положительными")
        self.id = studio_id
        self.name = name.strip()
        self.area = area
        self.price_per_hour = price_per_hour

    def calculate_price(self, hours: int) -> float:
        """Рассчитать стоимость положительного количества часов."""
        if hours <= 0:
            raise ValueError("Продолжительность должна быть положительной")
        return self.price_per_hour * hours

    def __str__(self) -> str:
        """Представить студию для вывода в каталоге."""
        return (f"{self.id}. {self.name}: {self.area:g} м², "
                f"{self.price_per_hour:g} руб./час")


def add_studio(studios: list[Studio], name: str, area: float,
               price_per_hour: float) -> Studio:
    """Создать студию и добавить в каталог."""
    studio = Studio(max((s.id for s in studios), default=0) + 1,
                    name, area, price_per_hour)
    studios.append(studio)
    return studio


def search_studios(studios: list[Studio], query: str) -> list[Studio]:
    """Найти студии по части названия без учёта регистра."""
    return [s for s in studios if query.lower() in s.name.lower()]


def get_studio(studios: list[Studio], studio_id: int) -> Studio:
    """Найти студию по идентификатору."""
    for studio in studios:
        if studio.id == studio_id:
            return studio
    raise ValueError("Студия с таким номером не найдена")


def filter_studios_by_price(studios: list[Studio],
                            max_price: float) -> list[Studio]:
    """Выбрать студии не дороже заданной цены."""
    return [s for s in studios if s.price_per_hour <= max_price]


def sort_studios_by_price(studios: list[Studio]) -> list[Studio]:
    """Вернуть новый список в порядке возрастания цены."""
    return sorted(studios, key=lambda s: s.price_per_hour)
