import unittest
from pathlib import Path
import address_app.storage
from address_app.base.consts import DEFAULT_ROOT_PATH, RELATIVE_STORAGE_PATH
from address_app.database.db_schema import DbSchema
from address_app.serialize import SerializeStrategyRegistry


class TestFileSystemStorage(unittest.TestCase):

    def test_storage_operations(self):
        """
        Test the behavior of the FileSystemStorage class.

        This test verifies that the FileSystemStorage class can successfully write and read data to and from the filesystem.
        """
        root = "tests"
        strategy = SerializeStrategyRegistry.get_strategy_for_extension("xml")
        self.file_storage = address_app.storage.DbFileSystemStorage(strategy, root)
        self.assertTrue(
            self.file_storage.is_initialized(), "Storage should be initialized"
        )
        self.assertTrue(
            self.file_storage.filepath_as_str()
            == str(
                Path(f"{root}/{RELATIVE_STORAGE_PATH}.{strategy.format()}").resolve()
            ),
            "File path should match",
        )

        db_contents = self.file_storage.read()
        self.assertTrue(isinstance(db_contents, DbSchema), "Database should be empty")

    def tearDown(self) -> None:
        self.file_storage.delete()


if __name__ == "__main__":
    unittest.main()
