import unittest
from shutil import rmtree
import address_app
from address_app.base.job_status import Status

TEST_ROOT = "tests/test_adbdatabse_books"


class TestAdbAddRemoveBooks(unittest.TestCase):
    """
    TestAdbAddRemoveBooks conducts tests on adding, removing, and managing address books within
    the AdbDatabase. It validates the functionality for creating new books, ensuring duplicates are
    handled correctly, and records within the books can be added and identified uniquely.
    """

    def setUp(self):
        self.root = TEST_ROOT
        self.adb = address_app.AdbDatabase(self.root)

    def test_add_remove_books(self):
        """
        Test the addition and subsequent removal of address books.

        Verifies that a new address book can be added to the database and then removed, ensuring
        the database does not retain any information about the deleted book.
        """
        book = self.adb.create_address_book("TestBook")
        self.assertIsNotNone(book, "Book should be created")

        temp_book_name = "TestBook2"
        self.adb.create_address_book(temp_book_name)
        self.adb.delete_address_book(temp_book_name)
        self.assertIsNone(
            self.adb.get_address_book(temp_book_name), "Book should be removed"
        )

    def test_add_existing_book(self):
        """
        Test adding an address book that already exists.

        Ensures that attempting to create an address book with a name that already exists in the
        database simply returns the existing book without creating a duplicate.
        """
        job_output = self.adb.create_address_book("TestBook")
        self.assertIsNotNone(job_output.return_value, "Book should be created")

        other_job_output = self.adb.create_address_book("TestBook")
        self.assertIs(
            other_job_output.return_value,
            job_output.return_value,
            "Creating an existing book should return the existing book",
        )

    def test_add_record(self):
        """
        Test adding a contact record to an address book.

        Validates that a new contact can be added to an existing book and that adding a duplicate
        contact does not create a new record but instead returns the existing record, with an
        appropriate status indicating the operation was cancelled due to duplication.
        """
        job_output = self.adb.create_address_book("TestBook")
        self.assertIsNotNone(job_output.return_value, "Book should be created")

        job_output = self.adb.add_contact(
            "TestBook", "John Doe", "123 Main St", "555-1234"
        )
        self.assertEqual(job_output.status, Status.SUCCESS, "Record should be added")

        other_job_output = self.adb.add_contact(
            "TestBook", "John Doe", "123 Main St", "555-1234"
        )
        self.assertIs(
            other_job_output.return_value,
            job_output.return_value,
            "Record should not be added, already exists",
        )
        self.assertIs(
            other_job_output.status,
            Status.CANCELLED,
            "Record should not be added, already exists",
        )

    def tearDown(self) -> None:
        """_summary_"""
        self.adb.clear()

    @classmethod
    def tearDownClass(cls):
        """
        Clean up after all tests in this class have been run.

        Deinitializes the address book database and removes any leftover files and directories
        created during testing to ensure a clean environment.
        """
        adb = address_app.AdbDatabase(TEST_ROOT)
        adb.deinit()
        rmtree(TEST_ROOT)


if __name__ == "__main__":
    unittest.main()
