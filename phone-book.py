import csv

PHONEBOOK_FILE: str = "phonebook.csv"
HEADERS: list = [
    "Фамилия",
    "Имя",
    "Отчество",
    "Организация",
    "Рабочий телефон",
    "Личный телефон",
]


def upload_phonebook() -> list:
    """
    Функция upload_phonebook() загружает телефонную книгу из файла и возвращает ее в виде списка словарей.

    return:
        список, содержащий содержимое файла телефонной книги.
    """
    try:
        with open(PHONEBOOK_FILE, mode="r", encoding="utf-8") as file:
            reader: csv = csv.DictReader(file)
            phonebook: list = list(reader)
    except FileNotFoundError:
        phonebook: list = []
    return phonebook


def update_phonebook(phonebook) -> None:
    """
    Функция update_phonebook сохраняет телефонную книгу в файл формата CSV.

    param phonebook:
        Параметр «phonebook» представляет собой список словарей, где каждый словарь представляет
        контакт в телефонной книге.
    """
    with open(PHONEBOOK_FILE, mode="w", encoding="utf-8", newline="") as file:
        writer: csv = csv.DictWriter(file, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(phonebook)


def display_entry(entry) -> None:
    """
    Функция display_entry принимает на вход словарную запись и выводит значения, связанные с
    определенными ключами.

    param entry:
        Параметр `entry` — это словарь, содержащий информацию о человеке.
    """
    print("Фамилия:", entry["Фамилия"])
    print("Имя:", entry["Имя"])
    print("Отчество:", entry["Отчество"])
    print("Организация:", entry["Организация"])
    print("Рабочий телефон:", entry["Рабочий телефон"])
    print("Личный телефон:", entry["Личный телефон"])


def display_phonebook(phonebook, page_number, entries_per_page) -> None:
    """
    Функция display_phonebook принимает в качестве входных данных телефонную книгу, номер страницы и
    записи на странице и отображает записи на указанной странице.

    param phonebook:
        Список записей телефонной книги. Каждая запись представляет собой словарь,
        содержащий такую информацию, как имя, номер телефона и адрес.

    param page_number:
        Номер страницы — это текущая страница телефонной книги, которую вы хотите
        отобразить. Это целочисленное значение.

    param entries_per_page:
        Параметр «entries_per_page» представляет количество записей телефонной
        книги, отображаемых на каждой странице.
    """
    start_index: int = (page_number - 1) * entries_per_page
    end_index: int = min(start_index + entries_per_page, len(phonebook))
    for entry in phonebook[start_index:end_index]:
        display_entry(entry)
        print("=" * 20)


def add_entry() -> None:
    """
    Функция add_entry позволяет пользователю вводить данные для новой записи в телефонной книге и
    добавлять ее в список телефонной книги.
    """
    new_entry: dict = {}
    for header in HEADERS:
        new_entry[header] = input(f"Введите {header}: ")
    phonebook.append(new_entry)
    update_phonebook(phonebook)
    print("Новая запись добавлена успешно.")


def edit_entry() -> None:
    """
    Функция «edit_entry()» позволяет пользователю искать определенную запись в телефонной книге,
    редактировать ее значения и сохранять обновленную телефонную книгу.
    """
    search_query: str = input("Введите фамилию для поиска: ")
    found_entries: dict = [
        entry for entry in phonebook if entry["Фамилия"] == search_query
    ]

    if len(found_entries) == 0:
        print("Запись не найдена.")
        return
    elif len(found_entries) > 1:
        print("Найдено несколько записей с такой фамилией.")
        display_phonebook(found_entries, 1, len(found_entries))
        entry_index: int = int(input("Введите номер записи для редактирования: ")) - 1
    else:
        entry_index: dict = phonebook.index(found_entries[0])

    edited_entry: dict = phonebook[entry_index].copy()

    for header in HEADERS:
        edited_entry[header] = input(f"Введите новое значение для {header}: ")
    phonebook[entry_index] = edited_entry
    update_phonebook(phonebook)
    print("Запись успешно отредактирована.")


def search_entries() -> None:
    """
    Функция search_entries принимает введенные пользователем данные для поискового запроса, ищет
    соответствующие записи в телефонной книге и отображает найденные записи.
    """
    search_query: str = input("Введите фамилию или другую характеристику для поиска: ")
    found_entries: dict = [
        entry
        for entry in phonebook
        if any(search_query.lower() in value.lower() for value in entry.values())
    ]
    if len(found_entries) == 0:
        print("Запись не найдена.")
        return
    display_phonebook(found_entries, 1, len(found_entries))


phonebook: list = upload_phonebook()

while True:
    print("\nМеню:")
    print("1. Вывод постранично записей из справочника на экран")
    print("2. Добавление новой записи в справочник")
    print("3. Возможность редактирования записей в справочнике")
    print("4. Поиск записей по одной или нескольким характеристикам")
    print("5. Выход")
    choice: str = input("Выберите действие (1-5): ")

    if choice == "1":
        page_number: int = int(input("Введите номер страницы: "))
        entries_per_page: int = int(input("Введите количество записей на странице: "))
        display_phonebook(phonebook, page_number, entries_per_page)
    elif choice == "2":
        add_entry()
    elif choice == "3":
        edit_entry()
    elif choice == "4":
        search_entries()
    elif choice == "5":
        print("Выход из программы.")
        break
    else:
        print("Неверный выбор. Попробуйте снова.")
