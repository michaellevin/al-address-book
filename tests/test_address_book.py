import unittest
import address_app as app


class TestAddressBook(unittest.TestCase):
    def setUp(self):
        self.adb = app.AdbDatabase()

    def test_add_record(self):
        book = self.adb.create_address_book("TestBook")
        book.add_record("Jane Doe", "456 Elm St", "555-6789")
        self.assertEqual(len(book), 1)

    def tearDown(self):
        # Clean up code here
        self.adb.remove_book("TestBook")


if __name__ == "__main__":
    unittest.main()
