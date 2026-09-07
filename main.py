
def authorisation(login, password):
    with open("DB_txt/users.txt", "r", encoding="utf-8") as file:
        users = file.readlines()
        if (login + ":" + password in users):
            print("Авторизация прошла успешно")
            return True
        else: 
            print("Неверный логин и пароль")
            return False
            
def choose_studio():
    with open("DB_txt/studios.txt", "r", encoding="utf-8") as file:
        studios = file.readlines()
        for i in range(len(studios)):
            print(f"{i + 1}. {studios[i].strip()}")
        print("Выберите студию по номеру: ")
        choice = int(input())
        
        return studios[choice - 1].strip()
      
def write_order(studio, date, start_time, end_time):
    print(f"Вы выбали студию: {studio}, дата: {date}, время с {start_time}:00 до {end_time}:00")
          
            
def choose_date_of_booking():
    input_date = input("Напишите дату бронирования (2026.01.01): ").strip()

    with open("DB_txt/date_of_booking.txt", "r", encoding="utf-8") as file:
        dates = file.readlines()

    print("Расписание на выбранный день:")

    for hour in range(9, 18):
        is_busy = False

        for date in dates:
            parts = date.split()

            if parts and input_date == parts[0]:
                times = parts[1].split("-")

                busy_start = int(times[0].split(":")[0])
                busy_end = int(times[1].split(":")[0])

                if busy_start <= hour < busy_end:
                    is_busy = True
                    break

        if is_busy:
            print(f"{hour}:00 - {hour + 1}:00 - занято")
        else:
            print(f"{hour}:00 - {hour + 1}:00 - свободно")

    start_time = int(input("Час начала (например, 14): "))
    end_time = int(input("Час окончания (например, 16): "))

    if not (9 <= start_time < end_time <= 18):
        print("Нужно выбрать интервал с 9 до 18, начало раньше окончания")
        return

    for date in dates:
        parts = date.split()

        if parts and input_date == parts[0]:
            times = parts[1].split("-")

            busy_start = int(times[0].split(":")[0])
            busy_end = int(times[1].split(":")[0])

            if start_time < busy_end and end_time > busy_start:
                print("Выбранный интервал пересекается с существующей бронью")
                return
    return input_date, start_time, end_time
                    
        

def main():
    print("Войдите в аккаунт")
    login = input("Введите логин: ")
    password = input("Введите пароль: ")
    
    if (authorisation(login, password)):
        print("Выберите фотостудию")
        choice = choose_studio()
        result = choose_date_of_booking()

        if result is None:
            return 
        
        date, start_time, end_time = result
        write_order(choice, date, start_time, end_time)
        
if __name__ == "__main__":
    main()
    