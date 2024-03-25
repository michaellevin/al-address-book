import argparse
import sys
from address_app.database import AdbDatabase

# Initialize the AdbDatabase instance
adb = None


def init_database(path=None):
    global adb
    adb = AdbDatabase(path) if path else AdbDatabase()

    print(f"Address Book Database initialized at {adb.storage_filepath}")


def check_status():
    if adb is not None:
        print(f"Adb initialized at {adb.root_path}")
    else:
        print("Adb is not initialized. Use 'adb init' to start.")


def list_books():
    if adb is None:
        print("Adb is not initialized. Use 'adb init' to start.")
        return
    books = adb.list_books()
    if books:
        print("Address Books:")
        for book in books:
            print(f"- {book}")
    else:
        print("No address books found.")


def create_book(name):
    if adb is None:
        print("Adb is not initialized. Use 'adb init' to start.")
        return
    adb.create_book(name)
    print(f"Address book '{name}' created.")


def add_contact(book_name):
    if adb is None:
        print("Adb is not initialized. Use 'adb init' to start.")
        return
    name = input("Name: ")
    address = input("Address: ")
    phone_no = input("Phone Number: ")
    adb.add_contact(book_name, name, address, phone_no)
    print("Contact added.")


def main():
    parser = argparse.ArgumentParser(description="Address Book CLI")
    parser.add_argument(
        "command",
        help="Command to run",
        choices=["init", "status", "list", "create-book", "add-contact"],
    )
    parser.add_argument("arguments", nargs="*", help="Arguments for the command")
    args = parser.parse_args()

    if args.command == "init":
        path = args.arguments[0] if args.arguments else None
        init_database(path)
    elif args.command == "status":
        check_status()
    elif args.command == "list":
        list_books()
    elif args.command == "create-book":
        if not args.arguments:
            print("Please specify a name for the address book.")
            return
        create_book(args.arguments[0])
    elif args.command == "add-contact":
        if not args.arguments:
            print("Please specify the address book name.")
            return
        add_contact(args.arguments[0])
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
