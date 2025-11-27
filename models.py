import re
from collections import UserDict
from datetime import datetime


class Field:
    """Базовий клас для полів запису."""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Birthday(Field):
    """Поле для зберігання дати народження у форматі DD.MM.YYYY."""

    def __init__(self, value: str):
        pattern = r'\b(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(\d{4})\b'
        if not re.match(pattern, value):
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        try:
            date_value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(date_value)


class Name(Field):
    """Ім'я контакту. Обов'язкове поле."""
    def __init__(self, name: str):
        if not name:
            raise ValueError("Поле імʼя не може бути порожнім")
        super().__init__(name)


class Phone(Field):
    """Телефон з валідацією формату (рівно 10 цифр)."""
    def __init__(self, phone_number: str):
        ph = str(phone_number).strip()
        if len(ph) != 10 or not ph.isdigit():
            raise ValueError("Номер має бути у форматі 10 цифр")
        super().__init__(ph)

    def __eq__(self, other):
        return isinstance(other, Phone) and self.value == other.value


class Record:
    """Запис контакту: ім'я, телефони, день народження."""
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday | None = None

    def add_phone(self, phone: Phone):
        if phone in self.phones:
            raise ValueError("Такий номер вже є")
        self.phones.append(phone)

    def remove_phone(self, phone: Phone):
        self.phones = [p for p in self.phones if p != phone]

    def edit_phone(self, old_phone: Phone, new_phone: Phone):
        for idx, p in enumerate(self.phones):
            if p == old_phone:
                self.phones[idx] = new_phone
                return
        raise ValueError(f"{old_phone.value} не знайдено")

    def find_phone(self, phone: str):
        phone_obj = Phone(phone)
        for p in self.phones:
            if p == phone_obj:
                return p.value
        return None

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones) or "—"
        bday = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "—"
        return f"{self.name.value}: {phones} | Birthday: {bday}"


class AddressBook(UserDict):
    """Колекція записів контактів."""
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name_to_find: str) -> Record | None:
        return self.data.get(name_to_find)

    def find_by_phone(self, phone_to_find: str) -> Record | None:
        """Пошук запису за номером телефону."""
        for record in self.data.values():
            if any(p.value == phone_to_find for p in record.phones):
                return record
        return None

    def delete(self, name: str):
        record = self.data.pop(name, None)
        if record:
            print(f"Запис {name} видалено")
        else:
            print(f"Запис {name} не знайдено")
