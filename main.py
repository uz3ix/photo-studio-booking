from pathlib import Path

from module.bookings import create_booking, is_available
from module.storage import load_json, save_json
from module.studios import get_studio, search_studios, sort_studios_by_price
from module.users import authorisation, register_user
from module.utils import input_date, input_int, input_range

DATA_DIR = Path(__file__).resolve().parent / "data"


def show_studios(studios: list[dict]) -> None:
    """Показать каталог с характеристиками студий."""
    if not studios:
        print("Студии не найдены")
    for studio in studios:
        print(f'{studio["id"]}. {studio["name"]}: '
              f'{studio["area"]} м², '
              f'{studio["price_per_hour"]} руб./час')


def choose_date_of_booking(bookings: list[dict],
                           studio_id: int) -> tuple[str, int, int]:
    """Выбрать день, показать расписание и запросить часы."""
    booking_date = input_date("Дата (ГГГГ.ММ.ДД): ").isoformat()
    for hour in range(9, 18):
        available = is_available(bookings, studio_id, booking_date,
                                 hour, hour + 1)
        status = "свободно" if available else "занято"
        print(f"{hour}:00–{hour + 1}:00 — {status}")
    start = input_range("Час начала: ", 9, 17)
    end = input_range("Час окончания: ", 10, 18)
    return booking_date, start, end


def show_bookings(bookings: list[dict], studios: list[dict],
                  login: str) -> None:
    """Вывести бронирования текущего пользователя."""
    own = [b for b in bookings if b.get("login") == login]
    if not own:
        print("У вас пока нет бронирований")
    for booking in own:
        studio = get_studio(studios, booking["studio_id"])
        print(f'№{booking["id"]}: {studio["name"]}, '
              f'{booking["booking_date"]}, '
              f'{booking["start_hour"]}:00–{booking["end_hour"]}:00, '
              f'{booking["total_price"]} руб.')


def main() -> None:
    """Загрузить данные и выполнять действия меню до выхода."""
    try:
        users = load_json(DATA_DIR / "users.json")
        studios = load_json(DATA_DIR / "studios.json")
        bookings = load_json(DATA_DIR / "date_of_booking.json")
    except (OSError, ValueError) as error:
        print(f"Не удалось загрузить данные: {error}")
        return

    user = None
    while user is None:
        print("\n1. Вход\n2. Регистрация\n0. Выход")
        action = input_range("Действие: ", 0, 2)
        if action == 0:
            return
        login = input("Логин: ").strip()
        password = input("Пароль: ")
        try:
            if action == 1:
                user = authorisation(users, login, password)
            else:
                updated_users = users.copy()
                registered = register_user(updated_users, login, password)
                save_json(DATA_DIR / "users.json", updated_users)
                users = updated_users
                user = registered
            print("Вы вошли в аккаунт")
        except (ValueError, OSError) as error:
            print(error)

    while True:
        print("\n1. Все студии\n2. Поиск по названию\n"
              "3. Информация о студии\n4. Бронирование\n"
              "5. Мои бронирования\n6. Студии по цене\n0. Выход")
        action = input_range("Действие: ", 0, 6)
        try:
            if action == 0:
                return
            elif action == 1:
                show_studios(studios)
            elif action == 2:
                show_studios(search_studios(studios, input("Название: ")))
            elif action == 3:
                studio = get_studio(studios, input_int("Номер студии: "))
                show_studios([studio])
            elif action == 4:
                show_studios(studios)
                studio = get_studio(studios, input_int("Номер студии: "))
                day, start, end = choose_date_of_booking(
                    bookings, studio["id"]
                )
                updated_bookings = bookings.copy()
                booking = create_booking(updated_bookings, studio,
                                         user["login"], day, start, end)
                save_json(DATA_DIR / "date_of_booking.json",
                          updated_bookings)
                bookings = updated_bookings
                print(f'Бронь №{booking["id"]} сохранена. '
                      f'Стоимость: {booking["total_price"]} руб.')
            elif action == 5:
                show_bookings(bookings, studios, user["login"])
            elif action == 6:
                show_studios(sort_studios_by_price(studios))
        except (ValueError, OSError) as error:
            print(error)


if __name__ == "__main__":
    main()
