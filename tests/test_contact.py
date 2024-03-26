import unittest
from address_app.model import Contact


class TestContact(unittest.TestCase):
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
        # Contacts with different names, addresses, or phone numbers should not be considered equal
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
        # Contact without a phone number should be handled correctly
        self.assertIsNotNone(
            self.contact2.phone_no,
            "Contact phone number should be None if not provided",
        )


if __name__ == "__main__":
    unittest.main()
