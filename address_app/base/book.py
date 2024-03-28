from . import get_logger
from ..database.db_schema import DbBooksTypeAlias, BookContactIdsTypeAlias
from .contact import Contact

logger = get_logger()


class Book:

    def __init__(self, name: str = "Default", contacts: BookContactIdsTypeAlias = []):
        self._name = name
        self._contacts = contacts  # List of contact ids

    @property
    def name(self):
        """Returns the name of the address book."""
        return self._name

    @property
    def contacts(self):
        """Returns the list of contact ids in the address book."""
        return self._contacts

    def add_record(self, contact: Contact) -> int:
        if contact.id in self._contacts:
            logger.warning(f"Contact {contact} already exists")
            return
        self._contacts.append(contact.id)
        return contact.id

    def is_empty(self) -> bool:
        return not bool(self._contacts)

    def contact_exists(self, contact_id: int) -> bool:
        return contact_id in self._contacts

    def as_dict(self) -> DbBooksTypeAlias:
        """Converts the address book to a dictionary format.

        Example:
            >>> book = AddressBook("TestBook")
            >>> contact1 = Contact("Jane Doe", "456 Elm St", "555-6789")
            >>> book.add_record(contact1)
            >>> contact2 = Contact("John Doe", "123 Elm St", "535-6789")
            >>> book.add_record(contact2)
            >>> book.as_dict()
                {
                    "TestBook": [contact1.id, contact2.id]
                }

        """
        return {
            self.name: self._contacts,
        }

    def __len__(self):
        return len(self._contacts)

    def __repr__(self) -> str:
        return f"AddressBook(name={self.name}, ({len(self)} contacts))"

    def __str__(self) -> str:
        return f"AddressBook(name={self.name}, ({len(self)} contacts))"
