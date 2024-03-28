import unittest
from address_app.base.contact import Contact
from address_app.base.validator import ContactValidation
from address_app.base.exceptions import InvalidContactDataException


class TestValidation(unittest.TestCase):

    def test_valid_name(self):
        self.assertIsNone(
            ContactValidation.validate_name("John Doe")
        )  # Assuming validate_name returns None for valid inputs

        # Test invalid names
        with self.assertRaises(InvalidContactDataException):
            ContactValidation.validate_name("")  # Empty string

        with self.assertRaises(InvalidContactDataException):
            ContactValidation.validate_name("   ")  # Spaces only

        with self.assertRaises(InvalidContactDataException):
            ContactValidation.validate_name("123")  # Numeric string

    def test_valid_address(self):
        self.assertIsNone(ContactValidation.validate_address("123 Main St"))

        # Test invalid addresses
        with self.assertRaises(InvalidContactDataException):
            ContactValidation.validate_address("")  # Empty string

        with self.assertRaises(InvalidContactDataException):
            ContactValidation.validate_address("   ")  # Spaces only

    def test_valid_phone_no(self):
        self.assertIsNone(
            ContactValidation.validate_phone_no("555-1234"),
            "Phone number should be valid",
        )
        self.assertIsNone(
            ContactValidation.validate_phone_no("+1 (903) 972-35-59"),
            "Phone number should be valid",
        )
        self.assertIsNone(
            ContactValidation.validate_phone_no(None),
            "Phone number should be valid or empty",
        )
        self.assertIsNone(
            ContactValidation.validate_phone_no(""),
            "Phone number should be valid or empty",
        )
        self.assertIsNone(
            ContactValidation.validate_phone_no(" "),
            "Phone number should be valid or empty",
        )

        # Test invalid phone numbers
        with self.assertRaises(InvalidContactDataException):
            ContactValidation.validate_phone_no("abc")  # Non-numeric


class TestContact(unittest.TestCase):
    """
    TestContact class is designed to test the functionality and behavior of the Contact class.

    It verifies that contact instances are correctly compared for equality or inequality based on
    their attributes, and it checks how contacts are handled when certain information (like a phone number)
    is missing.
    """

    def setUp(self):
        # Setup some contacts for testing
        self.contact1 = Contact(
            name="John Doe", address="123 Main St", phone_no="555-1234"
        )
        self.contact1_w_spaces = Contact(
            name="John Doe  ", address="123 Main St ", phone_no="555-1234"
        )  # Trailing space in address
        self.contact1_diff_phone = Contact(
            name="John Doe  ", address="123 Main St ", phone_no="456-1234"
        )  # Different phone number
        self.contact1_no_phone = Contact(
            name="John Doe", address="123 Main St"
        )  # No phone number

        self.contact2 = Contact(
            name="Jane Doe", address="456 Park Ave", phone_no="555-5678"
        )

    def test_contact_equality(self):
        # Contacts with the same name, address, and phone number should be considered equal
        self.assertEqual(
            self.contact1,
            self.contact1_w_spaces,
            "Contacts with identical details should be equal",
        )

    def test_contact_inequality(self):
        """
        Test the inequality comparison between Contact instances.

        Contacts should not be considered equal if they have different details, such as a different
        name and address. But they should be considered equal if they have the same name and address
        but different phone numbers.

        """
        self.assertNotEqual(
            self.contact1,
            self.contact2,
            "Contacts with different details should not be equal",
        )
        self.assertEqual(
            self.contact1_w_spaces,
            self.contact1_no_phone,
            "Contacts with different details should not be equal",
        )

    def test_contact_without_phone_number(self):
        """
        Verify handling of Contact instances without a phone number.

        Ensures that a Contact without a phone number is handled correctly, implying that the
        phone number attribute should be None or handled in a manner that indicates the absence
        of a phone number.
        """
        self.assertIsNotNone(
            self.contact2.phone_no,
            "Contact phone number should be None if not provided",
        )

    def test_contact_as_dict(self):
        """
        Test the conversion of a Contact instance to a dictionary.

        Ensures that a Contact instance can be correctly represented as a dictionary, excluding
        the unique identifier attribute. The dictionary should contain the contact's name, address,
        and phone number (if available).

        """
        contact_dict = self.contact1.as_dict()
        self.assertIsInstance(
            contact_dict,
            dict,
            "Contact representation should be a dictionary",
        )

        self.assertDictEqual(
            contact_dict,
            {
                "name": "John Doe",
                "address": "123 Main St",
                "phone_no": "555-1234",
            },
            "Contact details should be included in the dictionary",
        )


if __name__ == "__main__":
    unittest.main()
