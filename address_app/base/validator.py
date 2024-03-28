from typing import Optional
import re

from .consts import VALIDATE_PHONE_NO_REGEX
from .exceptions import (
    InvalidContactAddressException,
    InvalidContactNameException,
    InvalidContactPhoneNumberException,
)


class ContactValidation:
    @staticmethod
    def validate_name(name: str):
        if not isinstance(name, str) or not name.strip() or name.isdigit():
            raise InvalidContactNameException(name)

    @staticmethod
    def validate_address(address: str):
        if not isinstance(address, str) or not address.strip():
            raise InvalidContactAddressException(address)

    @staticmethod
    def validate_phone_no(phone_no: Optional[str]):
        if phone_no is not None and not re.match(VALIDATE_PHONE_NO_REGEX, phone_no):
            raise InvalidContactPhoneNumberException(phone_no)

    @staticmethod
    def validate_contact(name: str, address: str, phone_no: Optional[str] = None):
        ContactValidation.validate_name(name)
        ContactValidation.validate_address(address)
        ContactValidation.validate_phone_no(phone_no)
