def main():
    # Load data on startup
    book = load_data()
    
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        
        if command in ["close", "exit"]:
            # We still save on exit just in case
            save_data(book)
            print("Good bye!")
            break
        
        elif command == "hello":
            print("How can I help you?")
        elif command in ["help", "?"]:
            print("Available commands: add, change, phone, all, add-birthday, show-birthday, birthdays, close, exit")
        
        # --- Commands that MODIFY data (Save after these) ---
        elif command == "add":
            print(add_contact(args, book))
            save_data(book)  # <--- Save immediately
            
        elif command == "change":
            print(change(args, book))
            save_data(book)  # <--- Save immediately

        elif command == "add-birthday":
            print(add_birthday(args, book))
            save_data(book)  # <--- Save immediately

        # --- Commands that READ data (No need to save) ---
        elif command == "phone":
            print(phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(get_upcoming_birthdays(book))
            
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()