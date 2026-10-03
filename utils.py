from datetime import date, datetime


def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число.

    При некорректном вводе запрос повторяется.
    """
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Нужно целое число, попробуйте снова")


def input_date(prompt: str) -> date:
    """Запросить у пользователя дату в формате 2026.01.01."""
    while True:
        try:
            return datetime.strptime(input(prompt).strip(), "%Y.%m.%d").date()
        except ValueError:
            print("Неверный формат даты, пример: 2026.01.01")


def input_range(prompt: str, low: int, high: int) -> int:
    """Запросить целое число в диапазоне [low, high]."""
    while True:
        value = input_int(prompt)
        if low <= value <= high:
            return value
        print(f"Число должно быть от {low} до {high}")
