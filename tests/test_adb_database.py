import unittest
import os
import address_app as app


class TestAdbBase(unittest.TestCase):
    def setUp(self):
        self.root = "tests"
        self.adb = app.AdbDatabase(self.root)

    def test_init(self):
        self.assertIsNotNone(
            app.AdbDatabase(),
            "AdbDatabase instance should be created without a root path",
        )

        self.assertIsNotNone(
            app.AdbDatabase("tests"),
            "AdbDatabase instance should be created with a root path",
        )

        self.assertIsNotNone(
            app.AdbDatabase(123),
            "AdbDatabase instance should be created with a root path",
        )

        self.assertIsNotNone(
            app.AdbDatabase(None),
            "AdbDatabase instance should be created with a root path",
        )

    def test_singleton(self):
        """Test that the AdbDatabase is a singleton."""
        same_path = os.path.abspath(self.root)
        same_adb = app.AdbDatabase(same_path)

        self.assertIs(
            self.adb,
            same_adb,
            "AdbDatabase instances with different roots should not be the same (singleton)",
        )

        other_adb = app.AdbDatabase()
        self.assertIsNot(
            self.adb,
            other_adb,
            "AdbDatabase instances with the same root should be the same (singleton)",
        )

    def test_database_paths(self):
        """Test that the database paths are set correctly."""
        self.assertEqual(
            self.adb.root,
            os.path.abspath(self.root),
            "Root path should match the provided path",
        )

        self.assertTrue(
            os.path.exists(self.adb.storage_filepath),
            "Database file should exist",
        )

        self.assertEqual(
            self.adb.storage_filepath,
            os.path.abspath(
                os.path.join(
                    os.path.abspath(self.root), app.base.consts.RELATIVE_STORAGE_PATH
                )
            ),
            "Root path should match the provided path",
        )

    def tearDown(self):
        self.adb.clear()


class TestAdbAddRemoveBooks(unittest.TestCase):
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
        del self.adb


if __name__ == "__main__":
    unittest.main()