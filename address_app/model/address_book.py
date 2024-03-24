"""
This module provides functionality for managing an address book, allowing for the addition,
retrieval, and searching of contacts. Each contact is represented as an `IContact` instance.

Classes:
    AddressBook: Represents an address book to manage `IContact` instances.
"""

import re
from fnmatch import fnmatch
from typing import Optional, List

from ..base import get_logger
from ..base.consts import VALIDATE_PHONE_NO_REGEX
from ..base.exceptions import (
    AddressAppException,
    InvalidContactAddressException,
    InvalidContactNameException,
    InvalidContactPhoneNumberException,
)
from .contact import IContact

logger = get_logger()


class AddressBook:
    """Represents a simple address book to manage contacts.

    This address book acts like a collection of contacts, allowing for adding new contacts,
    retrieving them by a unique identifier, searching, and direct iteration over the contacts.
    Contacts can be accessed directly using their unique ID through subscript notation (`[]`),
    and the number of contacts can be obtained with the `len()` function.

    Args:
        name (str, optional): The name of the address book. Defaults to "Default".

    Examples:
        Creating an address book and adding contacts:

        >>> address_book = AddressBook("My Contacts")
        >>> contact_id = address_book.add_record("John Doe", "123 Main St", "555-1234").id
        >>> print(address_book[contact_id])
        IContact(name=John Doe, address=123 Main St, phone_no=555-1234)

        Iterating over contacts in the address book:

        >>> for contact in address_book:
        ...     print(contact)

        Getting the number of contacts:

        >>> len(address_book)
        1

        Accessing a contact by ID:

        >>> print(address_book[contact_id])
        IContact(name=John Doe, address=123 Main St, phone_no=555-1234)
    """

    def __init__(self, name="Default"):
        self._name = name
        self._contacts = {}

    @property
    def name(self):
        """Returns the name of the address book."""
        return self._name

    def get_contact_by_id(self, contact_id: int) -> Optional[IContact]:
        """Retrieves a contact by its unique ID.

        Args:
            contact_id (int): The unique identifier for the contact.

        Returns:
            Optional[IContact]: The contact if found, otherwise None.
        """
        return self._contacts.get(contact_id)

    def add_record(
        self, name: str, address: str, phone_no: Optional[str]
    ) -> Optional[IContact]:
        """Attempts to add a new contact record to the address book.

        Validates the provided name, address, and phone number before addition.
        Logs an error and returns None if validation fails.

        Args:
            name (str): The name of the contact.
            address (str): The contact's address.
            phone_no (str, optional): The contact's phone number. Defaults to None.

        Returns:
            Optional[IContact]: The added contact object, or None if the addition fails.
        """
        try:
            if not isinstance(name, str) or not name.strip() or name.isdigit():
                raise InvalidContactNameException(name)
            if not isinstance(address, str) or not address.strip():
                raise InvalidContactAddressException(address)
            if phone_no is not None:
                # Validate phone number format
                if not re.match(VALIDATE_PHONE_NO_REGEX, phone_no):
                    raise InvalidContactPhoneNumberException(phone_no)
        except AddressAppException as e:
            logger.error(e.message)
            return None

        temp_contact = IContact(name, address, phone_no)
        if contact := self.get_contact_by_id(temp_contact.id):
            logger.warning(f"Contact {contact} already exists")
            return contact

        self._contacts[temp_contact.id] = temp_contact
        logger.info(f"Added contact {temp_contact}")
        return temp_contact

    def find_contact(self, **criteria) -> List[IContact]:
        """Finds contacts that match the given search criteria.

        Args:
            **criteria: Arbitrary number of keyword arguments representing the search criteria.

        Returns:
            List[IContact]: A list of contacts that match the criteria.

        Examples:
            Searching for contacts by name:

            >>> address_book.find_contact(name="John Doe")
            [IContact(name=John Doe, address=123 Main St, phone_no=555-1234)]

            Searching for contacts by phone number:

            >>> address_book.find_contact(phone_no="555-1234")
            [IContact(name=John Doe, address=123 Main St, phone_no=555-1234)]

            Searching for contacts by name and address:

            >>> address_book.find_contact(name="John Doe", address="123 Main St")
            [IContact(name=John Doe, address=123 Main St, phone_no=555-1234)]

        """
        results = list(self._contacts.values())
        for attr, pattern in criteria.items():
            results = [
                contact
                for contact in results
                if fnmatch(getattr(contact, attr, ""), pattern)
            ]
        return results

    # def remove_record(self, contact_id: int) -> Optional[IContact]: ...

    def to_dict(self):
        """Represents the address book as a dictionary.

        Returns:
            dict: A dictionary representation of the address book, including all contacts.
        """
        return {
            "name": self.name,
            "contacts": [contact.to_dict() for contact in self._contacts.values()],
        }

    def clear(self):
        """Clears all contacts from the address book."""
        self._contacts = {}

    def __getitem__(self, contact_id: int) -> Optional[IContact]:
        return self.get_contact_by_id(contact_id)

    def __len__(self):
        return len(self._contacts)

    def __repr__(self) -> str:
        return f"AddressBook(name={self.name}, contacts={self._contacts})"

    def __iter__(self):
        """Return an iterator over the contacts."""
        return iter(self._contacts.values())
