import unittest
from address_app.base.book import Book
from address_app.base.contact import Contact


class TestAddressBook(unittest.TestCase):

    def test_book_as_dict(self):
        self.book = Book("TestBook")

        contact1 = Contact("Jane Doe", "456 Elm St", "555-6789")
        self.book.add_record(contact1)
        contact2 = Contact("John Doe", "123 Elm St", "535-6789")
        self.book.add_record(contact2)

        book_as_dict = self.book.as_dict()
        self.assertEqual(book_as_dict, {"TestBook": [contact1.id, contact2.id]})
        self.assertIsInstance(book_as_dict, dict)


if __name__ == "__main__":
    unittest.main()
