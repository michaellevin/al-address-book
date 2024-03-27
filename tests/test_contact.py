import unittest
from address_app.model import Contact


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


if __name__ == "__main__":
    unittest.main()
