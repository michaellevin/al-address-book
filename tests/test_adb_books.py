import unittest
import os
import address_app as app


class TestAddressBook(unittest.TestCase):
    def setUp(self):
        self.root = "tests"
        self.adb = app.AdbDatabase(self.root)

    def test_add_remove_books(self):
        book = self.adb.create_address_book("TestBook")
        self.assertIsNotNone(book, "Book should be created")

        temp_book_name = "TestBook2"
        self.adb.create_address_book(temp_book_name)
        self.adb.delete_address_book(temp_book_name)
        self.assertIsNone(
            self.adb.get_address_book(temp_book_name), "Book should be removed"
        )

    def tearDown(self):
        # Clean up code here
        self.adb.clear()


if __name__ == "__main__":
    unittest.main()
