from address_app import AdbConnector
import shlex

global adb
adb = AdbConnector()


def list_books():
    print("Listing all books...")
    print(adb.db_manager.list_books())


def create_book(name):
    adb.db_manager.create_empty_book(name)


def list_contacts(book_name):
    print(f"Listing contacts in book: {book_name}")
    print(adb.db_manager.list_contacts(book_name))


def add_contact(book_name, name, address, phone=None):
    res = adb.db_manager.add_contact(book_name, name, address, phone)
    if res:
        print(
            f"Contact added to {book_name}: {name}, {address}, Phone: {phone if phone else 'N/A'}"
        )
    else:
        print(f"Failed to add contact to {book_name}.")


def filter_contacts(book_name, search_str):
    """
    Filter contacts in a specified address book by a search string. The function supports
    basic filtering by any field (name, address, phone) using a specific search pattern.
    It allows for both general searches across all fields or targeted searches within
    specific fields.

    Parameters:
    - book_name (str): The name of the address book from which to filter contacts.
    - search_str (str): The search pattern used for filtering. The pattern can be
        a general string that is matched against all fields, or it can be prefixed
        with a field specifier (e.g., "@name=", "@address=", "@phone_no=") to filter
        by a specific field. Wildcards (*) are used to denote the start or anywhere
        matches:
        - "John*" finds entries starting with "John" in any field.
        - "*123*" finds entries containing "123" in any field.
        - "@name=John*" finds entries with names starting with "John".
        - "@address=123*" finds entries with addresses starting with "123".

    Examples:
    >>> filter_contacts("friends", "John*")
    Filtering contacts in book: friends with search string: John*

    >>> filter_contacts("work", "*123*")
    Filtering contacts in book: work with search string: *123*

    >>> filter_contacts("family", "@name=Jane*")
    Filtering contacts in book: family with name: Jane*

    >>> filter_contacts("services", "@phone_no=*555*")
    Filtering contacts in book: services with phone_no: *555*

    Note:
    - The function prints the result of the filtering directly. In a real-world application,
      consider returning the filtered contacts to allow further processing or display
      in different contexts.
    - Wildcard (*) usage is simple and does not support complex patterns like regular expressions.
    """
    if search_str.startswith("@"):
        field, value = search_str[1:].split("=")
        if field not in ["name", "address", "phone_no"]:
            print("Invalid field. Must be 'name' or 'address' or 'phone_no'")
            return
        if field == "name":
            print(f"Filtering contacts in book: {book_name} with name: {value}")
        elif field == "address":
            print(f"Filtering contacts in book: {book_name} with address: {value}")
        else:
            print(f"Filtering contacts in book: {book_name} with phone_no: {value}")

        try:
            print(field, value)
            contacts = adb.db_manager.find_contacts(book_name, **{field: value})
            print(contacts)
        except Exception as e:
            print(f"Error filtering contacts: {e}")
    else:
        print(
            f"Filtering contacts in book: {book_name} with search string: {search_str}"
        )
        filtered_name_contacts = adb.db_manager.find_contacts(
            book_name, name=search_str
        )
        filtered_address_contacts = adb.db_manager.find_contacts(
            book_name, address=search_str
        )
        filtered_phone_contacts = adb.db_manager.find_contacts(
            book_name, phone_no=search_str
        )
        print(
            filtered_name_contacts + filtered_address_contacts + filtered_phone_contacts
        )


def process_command(command):
    parts = shlex.split(command)
    if not parts:
        return
    cmd = parts[0]
    args = parts[1:]

    if cmd == "list-books":
        list_books()
    elif cmd == "create-book" and len(args) >= 1:
        create_book(" ".join(args))
    elif cmd == "list-contacts" and len(args) >= 1:
        list_contacts(" ".join(args))
    elif cmd == "add-contact" and len(args) >= 3:
        add_contact(args[0], args[1], args[2], args[3] if len(args) > 3 else None)
    elif cmd == "filter-contacts" and len(args) >= 2:
        filter_contacts(args[0], args[1])

    else:
        print("Unknown command or insufficient arguments.")


def main_loop():
    print("Welcome to the Address Book CLI.")
    print("Type 'exit' to exit or 'help' for help.")
    while True:
        command = input("> ").strip()
        if command == "exit":
            print("Exiting the program.")
            break
        elif command == "help":
            print("Available commands:")
            print("  list-books - List all books")
            print("  create-book <name> - Create a new book with the given name")
            print(
                "  list-contacts <book_name> - List all contacts in the specified book"
            )
            print(
                "  add-contact <book_name> <name> <address> [phone] - Add a new contact"
            )
        else:
            process_command(command)


if __name__ == "__main__":
    main_loop()
