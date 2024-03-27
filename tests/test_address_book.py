import unittest
from address_app.model import (
    AddressBook,
    validate_name,
    validate_address,
    validate_phone_no,
)
from address_app.base.exceptions import InvalidContactDataException
from address_app.base.job_status import Status


class TestValidation(unittest.TestCase):

    def test_valid_name(self):
        self.assertIsNone(
            validate_name("John Doe")
        )  # Assuming validate_name returns None for valid inputs

        # Test invalid names
        with self.assertRaises(InvalidContactDataException):
            validate_name("")  # Empty string

        with self.assertRaises(InvalidContactDataException):
            validate_name("   ")  # Spaces only

        with self.assertRaises(InvalidContactDataException):
            validate_name("123")  # Numeric string

    def test_valid_address(self):
        self.assertIsNone(validate_address("123 Main St"))

        # Test invalid addresses
        with self.assertRaises(InvalidContactDataException):
            validate_address("")  # Empty string

        with self.assertRaises(InvalidContactDataException):
            validate_address("   ")  # Spaces only

    def test_valid_phone_no(self):
        self.assertIsNone(validate_phone_no("555-1234"), "Phone number should be valid")
        self.assertIsNone(
            validate_phone_no("+1 (903) 972-35-59"), "Phone number should be valid"
        )
        self.assertIsNone(
            validate_phone_no(None), "Phone number should be valid or empty"
        )
        self.assertIsNone(
            validate_phone_no(""), "Phone number should be valid or empty"
        )
        self.assertIsNone(
            validate_phone_no(" "), "Phone number should be valid or empty"
        )

        # Test invalid phone numbers
        with self.assertRaises(InvalidContactDataException):
            validate_phone_no("abc")  # Non-numeric


class TestAddressBook(unittest.TestCase):
    def setUp(self):
        self.book = AddressBook("TestBook")

    def test_add_valid_record(self):
        job_output = self.book.add_record("John Doe", "123 Main St", "555-1234")
        self.assertEqual(
            job_output.status, Status.SUCCESS, "Valid contact should be added"
        )

    def test_find_contact_by_name(self):
        self.book.add_record("Jane Doe", "456 Elm St", "555-6789")
        self.book.add_record("John Doe", "123 Elm St", "535-6789")
        results = self.book.find_contacts(name="*Doe")
        self.assertEqual(
            len(results), 2, "Should find two contacts matching name pattern"
        )

    def tearDown(self):
        # Clean up code here
        self.book.clear()
        del self.book


if __name__ == "__main__":
    unittest.main()
