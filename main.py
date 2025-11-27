from models import AddressBook
from storage import load_data, save_data
from commands import (
    parse_input,
    add_contact,
    change,
    phone,
    show_all,
    add_birthday,
    show_birthday,
    get_upcoming_birthdays,
)


def main():
    # Завантажуємо книгу при старті
    book: AddressBook = load_data()

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        if not user_input.strip():
            continue

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            # Зберігаємо книгу перед виходом
            save_data(book)
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command in ["help", "?"]:
            print(
                "Available commands:\n"
                "  add <name> <phone>\n"
                "  change <name> <old_phone> <new_phone>\n"
                "  phone <name>\n"
                "  all\n"
                "  add-birthday <name> <DD.MM.YYYY>\n"
                "  show-birthday <name>\n"
                "  birthdays\n"
                "  close / exit\n"
            )

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change(args, book))

        elif command == "phone":
            print(phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            upcoming = get_upcoming_birthdays(book)
            if upcoming:
                print("\n".join(upcoming))
            else:
                print("Немає днів народження в найближчі 7 днів.")

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
