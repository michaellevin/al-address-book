import argparse
import os
from address_app.database import AdbDatabase
from address_app.base.consts import DEFAULT_STORAGE_FULL_PATH

# Initialize the AdbDatabase instance
adb = None


def init_database(path=None):
    global adb
    adb = AdbDatabase()

    print(f"Address Book Database initialized at {adb.storage_filepath}")


def check_status():
    if os.path.exists(DEFAULT_STORAGE_FULL_PATH):
        print("Address Book Database is initialized.")
    else:
        print("Address Book Database is not initialized.")


def deinit_database():
    if os.path.exists(DEFAULT_STORAGE_FULL_PATH):
        adb = AdbDatabase()
        adb.deinit()
        print("Address Book Database de-initialized.")
    else:
        print("Address Book Database is not initialized, nothing to de-initialize.")


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
        choices=[
            "init",
            "status",
            "deinit",
            "list",
            "create-book",
            "add-contact",
            "help",
        ],
    )
    parser.add_argument("arguments", nargs="*", help="Arguments for the command")
    args = parser.parse_args()

    if args.command == "init":
        init_database()
    elif args.command == "status":
        check_status()
    elif args.command == "deinit":
        deinit_database()
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
