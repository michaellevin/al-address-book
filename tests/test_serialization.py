import unittest
from unittest.mock import patch
import os
from shutil import rmtree
import address_app

TEST_ROOT = "tests/test_serialization"


class TestSerialization(unittest.TestCase):

    def setUp(self):
        self.root = TEST_ROOT
        self.adb = address_app.AdbDatabase(self.root)
        job_output = self.adb.create_address_book("Book1")
        book1 = job_output.return_value
        self.adb.add_contact("Book1", "John Doe", "123 Main St", "555-1234")
        self.adb.add_contact("Book1", "John Denver", "123 Main St", "555-1234")
        self.serialize_manager = address_app.SerializationManager(book1)

    @patch(
        "address_app.serialize.strategies.yaml_serialization.try_import",
        return_value=None,
    )
    def test_yaml_installed(self, mock_import):
        """
        Test the behavior of the serialization manager when the YAML module is not installed.

        This test patches the try_import function to simulate the absence of the YAML module, ensuring
        that the appropriate exception is raised during serialization to YAML format.
        """
        with self.assertRaises(ModuleNotFoundError):
            self.serialize_manager.serialize(f"{self.root}/book1.yaml")

    def test_json_serialization(self):
        """
        Test the JSON serialization process.

        Verifies that the serialize manager can successfully serialize address book data into JSON format
        and that the resultant file exists on the filesystem.
        """
        self.serialize_manager.serialize(f"{self.root}/book1.json")
        self.assertTrue(os.path.exists(f"{self.root}/book1.json"))

    def test_yaml_serialization(self):
        """
        Test the YAML serialization process.

        Verifies that the serialize manager can successfully serialize address book data into YAML format
        and that the resultant file exists on the filesystem.
        """
        self.serialize_manager.serialize(f"{self.root}/book1.yaml")
        self.assertTrue(os.path.exists(f"{self.root}/book1.yaml"))

    def test_xml_serialization(self):
        """
        Test the XML serialization process.

        Verifies that the serialize manager can successfully serialize address book data into XML format
        and that the resultant file exists on the filesystem.
        """
        self.serialize_manager.serialize(f"{self.root}/book1.xml")
        self.assertTrue(os.path.exists(f"{self.root}/book1.xml"))

    def test_json_serialization_filtered(self):
        """
        This test should verify that serialization can filter contacts by a given criterion (e.g., name)
        and only serialize those that match.
        """
        # TODO
        ...
        # self.serialize_manager.serialize(f"{self.root}/book1.json", name="John*")
        # self.assertTrue(os.path.exists(f"{self.root}/book1.json"))

    def tearDown(self) -> None:
        self.adb.clear()

    @classmethod
    def tearDownClass(cls):
        """
        Clean up after all tests in this class have been run.

        Specifically, it deinitializes the address book database and removes any leftover files and
        directories created during testing.
        """
        adb = address_app.AdbDatabase(TEST_ROOT)
        adb.deinit()
        rmtree(TEST_ROOT)


if __name__ == "__main__":
    unittest.main()
