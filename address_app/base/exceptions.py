from typing import Optional


class AddressAppException(Exception):
    title = "Address App Exception"

    def __init__(self, message="Error occurred"):
        self.message = message
        super().__init__(self.message)


# Database Exceptions
class AddressBookExistsException(AddressAppException):
    title = "Address Book Exists"

    def __init__(self, book_name: str = None):
        message = (
            f"`{book_name}` already exists"
            if book_name
            else "Address Book already exists"
        )
        super().__init__(message)


# Address Book Exceptions
class InvalidContactDataException(AddressAppException):
    title = "Invalid Contact Data"

    def __init__(
        self, data_value: str, data_type: str, additional_message=Optional[str]
    ):

        message = f"Invalid {data_type} format: {data_value}."
        message += f" {additional_message}" if additional_message else ""

        super().__init__(message)


class InvalidContactNameException(InvalidContactDataException):
    title = "Invalid Contact Name"

    def __init__(
        self,
        data_value: str,
        data_type: str = "Name",
        additional_message="Name cannot be empty or a number.",
    ):
        super().__init__(data_value, data_type, additional_message)


class InvalidContactAddressException(InvalidContactDataException):
    title = "Invalid Contact Address"

    def __init__(
        self,
        data_value: str,
        data_type: str = "Contact Address",
        additional_message="Address cannot be empty.",
    ):
        super().__init__(data_value, data_type, additional_message)


class InvalidContactPhoneNumberException(InvalidContactDataException):
    title = "Invalid Contact Phone Number"

    def __init__(
        self,
        data_value: str,
        data_type: str = "Contact Phone number",
        additional_message="Please enter only digits, spaces, +, (, ), and -.",
    ):
        super().__init__(data_value, data_type, additional_message)


# Formatter
class UnknownFormatterException(AddressAppException):
    title = "Formatter Exception"

    def __init__(self, name: str):
        message = f"Formatter {name} not found"
        super().__init__(message)


# Serialization
class SerializationException(AddressAppException):
    title = "Serialization Exception"

    def __init__(self, message: str):
        super().__init__(message)


class NoAvailableSerializationException(SerializationException):
    def __init__(self, name: str):
        message = f"{name} serialization not found"
        super().__init__(message)


class NotImplementerSerializationException(SerializationException):
    def __init__(self, name: str):
        message = f"{name} serialization not implemented yet"
        super().__init__(message)
