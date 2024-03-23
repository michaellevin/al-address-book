import re
import logging
from fnmatch import fnmatch
from typing import Optional, List

from address_app import __app_name__
from ._singleton import SingletonArgMeta
from .contact import IContact
from .exceptions import (
    AddressAppException,
    InvalidContactAddressException,
    InvalidContactNameException,
    InvalidContactPhoneNumberException,
    UnknownFormatterException,
)
from .consts import VALIDATE_PHONE_NO_REGEX
from .formatter import FormatterRegistry

logger = logging.getLogger(__app_name__)


# class AddressBook(metaclass=SingletonArgMeta):
class AddressBook:
    def __init__(self, name="Default"):
        self._name = name
        self._formatter = FormatterRegistry.get_formatter("text")
        self._contacts = {}

    @property
    def name(self):
        return self._name

    def set_formatter(self, name: str):
        try:
            self._formatter = FormatterRegistry.get_formatter(name)
        except UnknownFormatterException as e:
            logger.error(e.message)

    def get_contact_by_id(self, contact_id: int) -> Optional[IContact]:
        return self._contacts.get(contact_id)

    def add_record(
        self, name: str, address: str, phone_no: Optional[str]
    ) -> Optional[IContact]:
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
        results = list(self._contacts.values())
        for attr, pattern in criteria.items():
            results = [
                contact
                for contact in results
                if fnmatch(getattr(contact, attr, ""), pattern)
            ]
        return results

    def clear(self):
        self._contacts = {}

    def display(self, formatter_name: Optional[str] = None) -> str:
        if formatter_name:
            self.set_formatter(formatter_name)
        output = self._formatter.format(self)
        print(output)
        return output

    def __len__(self):
        return len(self._contacts)

    def __repr__(self) -> str:
        return f"AddressBook(name={self.name}, contacts={self._contacts})"

    def __iter__(self):
        """Return an iterator over the contacts."""
        return iter(self._contacts.values())
