import unittest
from unittest.mock import patch
import address_app.storage
import address_app.database
from address_app.database.db_schema import DbSchema
from address_app.serialize import SerializeStrategyRegistry


class TestDatabaseManager(unittest.TestCase):

    @patch("address_app.storage.DbFileSystemStorage.read")
    def test_database_init(self, mock_read):
        """ """
        db_schema = DbSchema()
        db_schema.books = {"TestBook": [3914141904, 3914141905]}
        db_schema.contacts = {
            3914141904: {
                "name": "John Doe",
                "address": "123 Main St",
                "phone_no": "555-1234",
            },
            3914141905: {
                "name": "Jane Doe",
                "address": "456 Elm St",
                "phone_no": "555-6789",
            },
        }
        mock_read.return_value = db_schema
        strategy = SerializeStrategyRegistry.get_strategy_for_extension()
        self.file_storage = address_app.storage.DbFileSystemStorage(strategy, "tests")

        db = address_app.database.DatabaseManager(self.file_storage)
        test_book = db.get_book("TestBook")
        none_book = db.get_book("NoneBook")
        self.assertEqual(test_book.name, "TestBook", "Should find TestBook")
        self.assertIsNone(none_book, "Should not find NoneBook")
        self.assertEqual(len(test_book), 2, "Should find two contacts in TestBook")

    @patch("address_app.storage.DbFileSystemStorage.read")
    def test_database_contacts(self, mock_read):
        """ """
        db_schema = DbSchema()
        db_schema.books = {"TestBook": []}
        db_schema.contacts = {}
        mock_read.return_value = db_schema

        strategy = SerializeStrategyRegistry.get_strategy_for_extension("xml")
        self.file_storage = address_app.storage.DbFileSystemStorage(strategy, "tests")

        db = address_app.database.DatabaseManager(self.file_storage)

        # add contact test
        db.add_contact("TestBook", "John Doe", "123 Main St", "555-1234")
        self.assertEqual(
            len(db.get_book("TestBook")), 1, "Should find one contact in TestBook"
        )

        # add second contact test
        db.add_contact("TestBook", "Jane Doe", "456 Elm St", "555-6789")
        self.assertEqual(
            len(db.get_book("TestBook")), 2, "Should find two contacts in TestBook"
        )

        # add contact to non-existent book test
        res = db.add_contact("NoneBook", "John Doe", "123 Main St", "555-1234")
        self.assertIsNone(res, "Should not add contact to NoneBook")

        # add duplicate contact test
        res = db.add_contact("TestBook", "John Doe", "123 Main St", "555-1234")
        self.assertIsNone(res, "Should not add duplicate contact to TestBook")

        # list contacts test
        db.add_contact("TestBook", "Craig Denver", "456 Elm St", "555-6789")
        all_contacts = db.list_contacts("TestBook")
        self.assertEqual(len(all_contacts), 3, "Should find three contacts in TestBook")

        # filter contact name test
        filtered_contacts = db.find_contacts("TestBook", name="*Doe")
        self.assertEqual(
            len(filtered_contacts), 2, "Should find two contacts in TestBook"
        )

        # filter contact address test
        filtered_contacts_address = db.find_contacts("TestBook", address="123*")
        self.assertEqual(
            len(filtered_contacts_address), 1, "Should find two contacts in TestBook"
        )

    def tearDown(self) -> None:
        self.file_storage.delete()
        pass


if __name__ == "__main__":
    unittest.main()
