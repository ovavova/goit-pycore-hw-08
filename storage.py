import pickle
from models import AddressBook


def save_data(book: AddressBook, filename: str = "addressbook.pkl"):
    """Серіалізація AddressBook у файл."""
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename: str = "addressbook.pkl") -> AddressBook:
    """Вигрузка AddressBook з файлу, або створення нової, якщо файл відсутній."""
    try:
        with open(filename, "rb") as f:
            book = pickle.load(f)
            if isinstance(book, AddressBook):
                return book
            return AddressBook()
    except FileNotFoundError:
        return AddressBook()
