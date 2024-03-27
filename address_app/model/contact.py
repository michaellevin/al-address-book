from dataclasses import dataclass, field, fields
from typing import Dict
from ..base.aux_utils import hash_input


@dataclass
class Contact:
    """Represents a contact with a name, address, and phone number.

    Args:
        name: The name of the contact.
        address: The address of the contact.
        phone_no: The phone number of the contact.


    This class also includes a unique identifier (`id`) for each contact, which is generated
    based on the name, address, and phone number (with all leading and trailing spaces removed)
    to ensure that contacts with identical information will have the same `id`.

    Example:
        Creating and comparing contacts:

        >>> contact1 = Contact("John Doe", "123 Main St", "555-1234")
        >>> contact2 = Contact("John Doe", "123 Main St ", "555-1234")
        >>> contact3 = Contact("Jane Doe", "456 Park Ave", "555-5678")

        Since contact1 and contact2 have identical details (ignoring spaces),
        they are considered equal:

        >>> contact1 == contact2
        True

        Contact3 has different details, so it is not equal to contact1 or contact2:

        >>> contact1 == contact3
        False
        >>> contact2 == contact3
        False

    This comparison behavior allows for the effective management of contact uniqueness
    within collections or databases, preventing duplicates based on the essential contact details.

    """

    name: str
    address: str
    phone_no: str = None
    _id: int = field(init=False, repr=False, compare=False)

    def __post_init__(self):
        """Generates a unique identifier for the contact based on its name and address."""
        self._id = hash_input(self.name.strip() + self.address.strip())

    @property
    def id(self) -> int:
        """Returns the unique identifier for the contact. Read-only.

        Returns:
            int: The contact's unique identifier.
        """
        return self._id

    def to_dict(self) -> Dict:
        """Converts the contact details to a dictionary format, excluding the unique identifier.

        Returns:
            dict: A dictionary of the contact's details.
        """
        return {f.name: getattr(self, f.name) for f in fields(self) if f.name != "_id"}

    def __eq__(self, other: object) -> bool:
        """Determines if the contact is equal to another contact.

        Args:
            other (object): The object to compare with.

        Returns:
            bool: True if the other object is an `Contact` with the same id, False otherwise.
        """
        if not isinstance(other, Contact):
            return False
        return self._id == other._id

    def __repr__(self) -> str:
        """Provides a human-readable representation of the contact.

        Returns:
            str: A string representation of the contact.
        """
        return f"Contact(name={self.name}, address={self.address}, phone_no={self.phone_no})"
