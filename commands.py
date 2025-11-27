from datetime import datetime
from models import AddressBook, Record, Phone, Birthday


def parse_input(user_input: str):
    """
    Парсинг рядка користувача на команду та аргументи.
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error(func):
    """
    Декоратор для обробки типових помилок вводу.
    Повертає текст помилки, замість падіння програми.
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, KeyError, IndexError) as e:
            return str(e)
    return inner


@input_error
def add_contact(args, book: AddressBook):
    """
    add <name> <phone>
    Додає новий контакт або оновлює існуючий (додає телефон).
    """
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        phone_obj = Phone(phone)
        record.add_phone(phone_obj)
    return message


@input_error
def change(args, book: AddressBook):
    """
    change <name> <old_phone> <new_phone>
    Змінює номер телефону для контакту.
    """
    name, old_phone, new_phone, *_ = args
    record = book.find(name)

    if record is None:
        return f"Contact {name} phone {old_phone} - not found"

    old_phone_obj = Phone(old_phone)
    new_phone_obj = Phone(new_phone)

    if old_phone_obj in record.phones:
        record.edit_phone(old_phone_obj, new_phone_obj)
        return f"Phone for {name} changed from {old_phone} to {new_phone}."
    else:
        return f"Phone {old_phone} not found for contact '{name}'."


@input_error
def phone(args, book: AddressBook):
    """
    phone <name>
    Показує всі телефони контакту.
    """
    name, *_ = args
    record = book.find(name)
    if record is None:
        return f"Contact {name} not found"
    phone_list = "; ".join(p.value for p in record.phones) or "—"
    return f"{name}: {phone_list}"


@input_error
def show_all(book: AddressBook):
    """Показати всі контакти."""
    if not book.data:
        return "Address book is empty."
    lines = [str(record) for record in book.data.values()]
    return "\n".join(lines)


@input_error
def add_birthday(args, book: AddressBook):
    """
    add-birthday <name> <DD.MM.YYYY>
    Додає/оновлює день народження контакту.
    """
    name, birthday_str, *_ = args
    record = book.find(name)
    if record is None:
        return f"Contact '{name}' not found."

    birthday_obj = Birthday(birthday_str)
    record.birthday = birthday_obj
    return f"Birthday for '{name}' set to {birthday_str}."


@input_error
def show_birthday(args, book: AddressBook):
    """
    show-birthday <name>
    Показати день народження контакту.
    """
    name, *_ = args
    record = book.find(name)
    if record is None:
        return f"Contact '{name}' not found."

    if record.birthday:
        date_str = record.birthday.value.strftime("%d.%m.%Y")
        return f"{name}'s birthday is on {date_str}."
    else:
        return f"No birthday information for '{name}'."


def get_upcoming_birthdays(book: AddressBook):
    """
    Повертає список рядків про дні народження, які відбудуться
    протягом наступних 7 днів (включно з сьогодні).
    """
    today = datetime.today().date()
    upcoming = []

    for record in book.data.values():
        if not record.birthday:
            continue

        bday_date = record.birthday.value.date()
        bday_this_year = bday_date.replace(year=today.year)

        # Якщо день народження вже минув цього року — беремо наступний рік
        if bday_this_year < today:
            bday_this_year = bday_this_year.replace(year=today.year + 1)

        days_until_birthday = (bday_this_year - today).days

        if 0 <= days_until_birthday < 7:
            date_str = bday_this_year.strftime("%d.%m.%Y")
            upcoming.append(f"On {date_str} is {record.name.value} birthday")

    return upcoming
