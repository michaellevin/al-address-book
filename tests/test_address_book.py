import unittest
from address_app.model import AddressBook


class TestAddressBook(unittest.TestCase):
    def setUp(self):
        self.book = AddressBook("TestBook")

    def test_add_valid_record(self):
        contact = self.book.add_record("John Doe", "123 Main St", "555-1234")
        self.assertIsNotNone(contact, "Valid contact should be added")

    def test_add_invalid_record(self):
        contact = self.book.add_record("", "123 Main St", "555-1234")
        self.assertIsNone(contact, "Invalid contact should not be added")

    def test_find_contact_by_name(self):
        self.book.add_record("Jane Doe", "456 Elm St", "555-6789")
        self.book.add_record("John Doe", "123 Elm St", "535-6789")
        results = self.book.find_contact(name="*Doe")
        self.assertEqual(
            len(results), 2, "Should find two contacts matching name pattern"
        )

    def tearDown(self):
        # Clean up code here
        self.book.clear()
        del self.book


if __name__ == "__main__":
    unittest.main()
