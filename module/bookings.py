from datetime import date


def is_available(bookings: list[dict], studio_id: int,
                 booking_date: str, start_hour: int, end_hour: int) -> bool:
    """Проверить пересечения только для выбранной студии и даты."""
    for booking in bookings:
        if (booking["studio_id"] == studio_id
                and booking["booking_date"] == booking_date
                and start_hour < booking["end_hour"]
                and end_hour > booking["start_hour"]):
            return False
    return True


def create_booking(bookings: list[dict], studio: dict, login: str,
                   booking_date: str, start_hour: int,
                   end_hour: int) -> dict:
    """Проверить дату и часы, рассчитать стоимость и добавить бронь."""
    date.fromisoformat(booking_date)
    if not (9 <= start_hour < end_hour <= 18):
        raise ValueError("Выберите интервал с 9 до 18, начало раньше конца")
    if not is_available(bookings, studio["id"], booking_date,
                        start_hour, end_hour):
        raise ValueError("Выбранный интервал уже занят")
    booking = {
        "id": max((b["id"] for b in bookings), default=0) + 1,
        "studio_id": studio["id"], "login": login,
        "booking_date": booking_date,
        "start_hour": start_hour, "end_hour": end_hour,
        "total_price": (end_hour - start_hour) * studio["price_per_hour"],
    }
    bookings.append(booking)
    return booking
