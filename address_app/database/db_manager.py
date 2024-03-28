from typing import Union, List
from dataclasses import dataclass
import fnmatch

from ..base import get_logger
from .db_schema import DbBooksTypeAlias
from ..base.book import Book
from ..base.contact import Contact
from ..base.validator import ContactValidation
from ..base.exceptions import InvalidContactDataException

logger = get_logger()


class DatabaseManager:
    """DatabaseManager class for managing the database."""

    def __init__(self, storage):
        """Initialize the DatabaseManager with a storage object.

        Args:
            storage (IStorage): The storage object to use for database operations.

        """
        self._storage = storage
        self._storage.init()

    def list_books(self) -> DbBooksTypeAlias:
        """List all books in the database.

        Returns:
            Dict[str, List[int]]: A list of all books in the database.

        """
        db_contents = self._storage.read()
        return [
            Book(name, contact_ids) for name, contact_ids in db_contents.books.items()
        ]

    def get_book(self, name: str) -> Union[Book, None]:
        """Get a book from the database.

        Args:
            name (str): The name of the book to retrieve.

        Returns:
            Union[Book, None]: The book if found, otherwise None.

        """
        books = self.list_books()
        for book in books:
            if book.name == name:
                return book

        logger.warning(f"Book '{name}' not found.")
        return None

    def add_book(self, book: Book) -> bool:
        """Add a book to the database.

        Args:
            book (Book): The book to add to the database.

        Returns:
            bool: True if the book was added, False if it already exists.

        """
        if self.get_book(book.name) is not None:
            logger.warning(f"Book '{book.name}' already exists.")
            return False
        db_contents = self._storage.read()
        db_contents.books[book.name] = book.contacts
        self._storage.write(db_contents)
        return True

    def create_empty_book(self, name: str) -> bool:
        """Create an empty book with the specified name."""
        self.add_book(Book(name))

    def add_contact(
        self, book_name: str, name: str, address: str, phoneno: str
    ) -> Union[Contact | None]:
        """Add a contact to a book.

        Args:
            book_name (str): The name of the book to add the contact to.
            name (str): The name of the contact.
            address (str): The address of the contact.
            phoneno (str): The phone number of the contact.

        Returns:
            Union[Contact, None]: The added contact if successful, otherwise None.

        Example:
            >>> dbm = DatabaseManager()
            >>> dbm.create_empty_book("TestBook")
            >>> dbm.add_contact("TestBook", "John Doe", "123 Elm St", "555-6789")
            Contact(name='John Doe', address='123 Elm St', phone_no='555-6789')

        """
        try:
            ContactValidation.validate_contact(name, address, phoneno)
        except InvalidContactDataException as e:
            logger.warning(f"Invalid contact data: {e.message}")
            return

        book = self.get_book(book_name)
        if book is None:
            logger.warning(f"Book '{book_name}' not found.")
            return

        db_contents = self._storage.read()
        contact = Contact(name, address, phoneno)

        # Add Contact to Book
        if book.contact_exists(contact.id):
            logger.warning(f"Contact '{contact}' already exists in '{book_name}'")
            return
        book.add_record(contact)
        if contact.id not in db_contents.contacts:
            db_contents.contacts[contact.id] = contact.as_dict()

        # Save the updated book and contact
        db_contents.books[book_name] = book.contacts
        self._storage.write(db_contents)
        return contact

    def list_contacts(self, book_name: Book) -> List[Contact]:
        """List all contacts in a book.

        Args:
            book_name (str): The name of the book to list contacts from.

        Returns:
            List[Contact]: A list of contacts in the book.

        Example:
            >>> dbm = DatabaseManager()
            >>> dbm.create_empty_book("TestBook")
            >>> dbm.add_contact("TestBook", "John Doe", "123 Elm St", "555-6789")
            >>> dbm.list_contacts("TestBook")
            [Contact(name='John Doe', address='123 Elm St', phone_no='555-6789')]
        """
        book = self.get_book(book_name)
        if book is None:
            logger.warning(f"Book '{book_name}' not found.")
            return []
        db_contents = self._storage.read()
        return [
            Contact(**db_contents.contacts[contact_id]) for contact_id in book.contacts
        ]

    def find_contacts(self, book_name: str, **criteria) -> List[Contact]:
        """Find contacts in the specified book that match the criteria.

        Args:
            book_name (str): The name of the book to search.
            **criteria: Key-value pairs of contact attributes to match.

        Returns:
            List[Contact]: A list of contacts that match the criteria.

        Example:
            >>> dbm = DatabaseManager()
            >>> dbm.create_empty_book("TestBook")
            >>> dbm.add_contact("TestBook", "John Doe", "123 Elm St", "555-6789")
            >>> dbm.find_contacts("TestBook", name="John Doe")
            [Contact(name='John Doe', address='123 Elm St', phone_no='555-6789')]
            >>> dbm.find_contacts("TestBook", address="123 Elm St")
            [Contact(name='John Doe', address='123 Elm St', phone_no='555-6789')]
        """
        contacts = self.list_contacts(book_name)
        return [
            contact
            for contact in contacts
            if all(
                fnmatch.fnmatch(str(getattr(contact, key)), value)
                for key, value in criteria.items()
            )
        ]
