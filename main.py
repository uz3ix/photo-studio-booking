from copy import copy
from pathlib import Path

from module.bookings import (
    Booking, cancel_booking, create_booking, is_available,
)
from module.storage import (
    load_bookings, load_studios, load_users, save_bookings, save_users,
)
from module.studios import (
    Studio, get_studio, search_studios, sort_studios_by_price,
)
from module.users import User, authorisation, register_user
from module.utils import input_date, input_int, input_range

DATA_DIR = Path(__file__).resolve().parent / "data"


def show_studios(studios: list[Studio]) -> None:
    """Показать каталог через строковое представление объектов."""
    if not studios:
        print("Студии не найдены")
    for studio in studios:
        print(studio)


def choose_date_of_booking(
    bookings: list[Booking], studio_id: int
) -> tuple[str, int, int]:
    """Выбрать день, показать расписание и запросить часы."""
    booking_date = input_date("Дата (ГГГГ.ММ.ДД): ").isoformat()
    for hour in range(9, 18):
        available = is_available(
            bookings,
            studio_id,
            booking_date,
            hour,
            hour + 1)
        status = "свободно" if available else "занято"
        print(f"{hour}:00–{hour + 1}:00 — {status}")
    start = input_range("Час начала: ", 9, 17)
    end = input_range("Час окончания: ", 10, 18)
    return booking_date, start, end


def show_bookings(bookings: list[Booking], user: User) -> None:
    """Показать собственные бронирования, включая отменённые."""
    own = [b for b in bookings if b.user.id == user.id]
    if not own:
        print("У вас пока нет бронирований")
    for booking in own:
        print(booking)


def main() -> None:
    """Загрузить данные и выполнять действия меню до выхода."""
    try:
        users = load_users(DATA_DIR / "users.json")
        studios = load_studios(DATA_DIR / "studios.json")
        bookings = load_bookings(
            DATA_DIR / "date_of_booking.json", studios, users
        )
    except (OSError, ValueError, KeyError, TypeError) as error:
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
                save_users(DATA_DIR / "users.json", updated_users)
                users = updated_users
                user = registered
            print("Вы вошли в аккаунт")
        except (ValueError, OSError) as error:
            print(error)

    while True:
        print(
            "\n1. Все студии\n2. Поиск по названию\n"
            "3. Информация о студии\n4. Бронирование\n"
            "5. Мои бронирования\n6. Студии по цене\n"
            "7. Отменить бронь\n0. Выход"
        )
        action = input_range("Действие: ", 0, 7)
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
                    bookings, studio.id)
                updated_bookings = bookings.copy()
                booking = create_booking(
                    updated_bookings, studio, user, day, start, end
                )
                save_bookings(
                    DATA_DIR / "date_of_booking.json", updated_bookings
                )
                bookings = updated_bookings
                print(
                    f'Бронь №{booking.id} сохранена. '
                    f'Стоимость: {booking.total_price} руб.'
                )
            elif action == 5:
                show_bookings(bookings, user)
            elif action == 6:
                show_studios(sort_studios_by_price(studios))
            elif action == 7:
                show_bookings(bookings, user)
                booking_id = input_int("Номер вашей брони: ")
                updated_bookings = [copy(b) for b in bookings]
                cancel_booking(updated_bookings, booking_id, user)
                save_bookings(
                    DATA_DIR / "date_of_booking.json", updated_bookings
                )
                bookings = updated_bookings
                print("Бронирование отменено")
        except (ValueError, OSError) as error:
            print(error)


if __name__ == "__main__":
    main()
