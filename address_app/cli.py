import argparse
import os
from address_app.database import AdbDatabase
from address_app.base.consts import DEFAULT_STORAGE_FULL_PATH
from address_app.base.job_status import Status
from address_app.model.address_book import (
    validate_name,
    validate_address,
    validate_phone_no,
)


def _is_initialized():
    return os.path.exists(DEFAULT_STORAGE_FULL_PATH)


def requires_initialization(func):
    """Decorator that checks if the database is initialized before proceeding."""

    def wrapper(*args, **kwargs):
        if not _is_initialized():
            print("Address Book Database is not initialized. Use 'adb init' to start.")
            return
        return func(*args, **kwargs)

    return wrapper


def get_validated_input(prompt, validate_func):
    """
    Prompts user for input and validates it, allowing up to two attempts.

    Args:
        prompt (str): The prompt message to display to the user.
        validate_func (callable): A function that validates the input.
            It should raise an exception if the validation fails.

    Returns:
        The validated input.

    Raises:
        The exception from validate_func if both attempts fail.
    """
    for _ in range(2):  # Allow two attempts
        try:
            value = input(prompt)
            validate_func(value)
            return value
        except Exception as e:
            print(e)
            print("Please try again.")
    raise Exception("Validation failed after two attempts.")


def init_database():
    """Initialize the address book database."""
    adb = AdbDatabase()
    print(f"Address Book Database initialized at {adb.storage_filepath}")


def check_status():
    """Check the status of the address book database."""
    if _is_initialized():
        print("Address Book Database is initialized.")
    else:
        print("Address Book Database is not initialized.")


def deinit_database():
    """De-initialize the address book database."""
    if _is_initialized():
        adb = AdbDatabase()
        adb.deinit()
        print("Address Book Database de-initialized.")
    else:
        print("Address Book Database is not initialized, nothing to de-initialize.")


@requires_initialization
def list_books():
    adb = AdbDatabase()
    books = adb.get_address_books()
    if books:
        print("Address Books:")
        for book in books:
            print(f"- {book} ({len(adb.get_address_book(book))} contacts)")
    else:
        print(
            "No address books found. Add a new address book using 'adb create-book <name>'."
        )


@requires_initialization
def create_book(name):
    adb = AdbDatabase()
    res = adb.create_address_book(name)
    if res.status == Status.CANCELLED:
        print(res.message)
    elif res.status == Status.SUCCESS:
        print(f"Address book '{name}' created.")


@requires_initialization
def add_contact(args):
    book_name = args.book_name

    # Possible values for name, address, and phone_no
    name = args.name
    address = args.address
    phone_no = args.phone

    adb = AdbDatabase()

    book = adb.get_address_book(book_name)
    if book is None:
        print(f"Address book '{book_name}' not found.")
        return

    # Interactive prompts to get contact details
    if name is None:
        try:
            name = get_validated_input("Enter name: ", validate_name)
        except Exception as e:
            print(e)
    if address is None:
        try:
            address = get_validated_input("Enter address: ", validate_address)
        except Exception as e:
            print(e)
    if phone_no is None:
        try:
            phone_no = get_validated_input(
                "Enter phone number [Optional]: ", validate_phone_no
            )
        except Exception as e:
            print(e)

    # Add the contact to the specified book
    status = adb.add_contact(book_name, name, address, phone_no)
    if status.status == Status.SUCCESS:
        print("Contact added!")
    else:
        print(f"Failed to add contact: {status.description}")


@requires_initialization
def list_contacts(book_name):
    adb = AdbDatabase()

    book = adb.get_address_book(book_name)
    if book is None:
        print(f"Address book '{book_name}' not found.")
        return

    ...
    #
    print(f"Contacts in '{book_name}':")
    for contact in book:
        print(f"- {contact}")

    #


def main():
    parser = argparse.ArgumentParser(description="Address Book CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Initialize subcommands
    subparsers.add_parser("init", help="Initialize the database")
    subparsers.add_parser("status", help="Check the database status")
    subparsers.add_parser("deinit", help="Deinitialize the database")
    subparsers.add_parser("list-books", help="List all books")
    subparsers.add_parser("create-book", help="Create a new book").add_argument(
        "name", type=str, help="Name of the book"
    )
    subparsers.add_parser(
        "list-contacts", help="List all contacts in a book"
    ).add_argument("book_name", type=str, help="Name of the address book")

    # Adjust 'add-contact' subcommand
    add_contact_parser = subparsers.add_parser("add-contact", help="Add a new contact")
    add_contact_parser.add_argument(
        "-b", "--book-name", type=str, help="Name of the address book", required=False
    )
    add_contact_parser.add_argument(
        "-n", "--name", type=str, help="Name of the contact", required=False
    )
    add_contact_parser.add_argument(
        "-a", "--address", type=str, help="Address of the contact", required=False
    )
    add_contact_parser.add_argument(
        "-p",
        "--phone",
        type=str,
        help="Phone of the contact [Optional]",
        required=False,
    )

    args = parser.parse_args()

    # Handle commands
    if args.command == "init":
        init_database()
    elif args.command == "status":
        check_status()
    elif args.command == "deinit":
        deinit_database()
    elif args.command == "list-books":
        list_books()
    elif args.command == "create-book":
        create_book(args.name)
    elif args.command == "list-contacts":
        list_contacts(args.book_name)
    elif args.command == "add-contact":
        add_contact(args)
    else:
        parser.print_help()


def display_help(arguments):
    """Display help for a specific command."""
    if not arguments:
        print("Usage: command [options] [arguments]")
        print(
            "Available commands: init, status, deinit, list-books, create-book, add-contact"
        )
        print("Use 'help [command]' to get more information on a specific command.")
        return

    command = arguments[0]
    if command == "create-book":
        print("create-book usage: create-book <book_name>")
        print("Creates a new address book with the specified name.")
    elif command == "add-contact":
        print(
            "add-contact usage: add-contact <book_name> --name <name> --address <address> --phone <phone>"
        )
        print(
            "Adds a new contact to the specified address book. The contact's name, address, and phone number are required."
        )
    # Add additional elif blocks for other commands as needed
    else:
        print(f"No specific help available for '{command}'.")


if __name__ == "__main__":
    main()
