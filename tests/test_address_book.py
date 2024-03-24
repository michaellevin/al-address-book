import unittest
import address_app as app


class TestAddressBook(unittest.TestCase):
    def setUp(self):
        self.adb = app.AdbDatabase()

    def test_add_valid_record(self):
        book = self.adb.create_address_book("TestBook")
        contact = book.add_record("John Doe", "123 Main St", "555-1234")
        self.assertIsNotNone(contact, "Valid contact should be added")

    def test_add_invalid_record(self):
        book = self.adb.create_address_book("TestBook")
        contact = book.add_record("", "123 Main St", "555-1234")
        self.assertIsNone(contact, "Invalid contact should not be added")

    def test_find_contact_by_name(self):
        book = self.adb.create_address_book("TestBook")
        book.add_record("Jane Doe", "456 Elm St", "555-6789")
        results = book.find_contact(name="Jane*")
        self.assertEqual(
            len(results), 1, "Should find one contact matching name pattern"
        )

    def test_find_contact_no_match(self):
        book = self.adb.create_address_book("TestBook")
        book.add_record("Jane Doe", "456 Elm St", "555-6789")
        results = book.find_contact(name="John*")
        self.assertEqual(
            len(results),
            0,
            "Should find no contacts matching non-existent name pattern",
        )

    def test_address_book_singleton(self):
        adb2 = app.AdbDatabase()
        self.assertIs(
            self.adb, adb2, "AdbDatabase instances should be the same (singleton)"
        )

    def tearDown(self):
        # Clean up code here
        self.adb.remove_book("TestBook")


if __name__ == "__main__":
    unittest.main()
