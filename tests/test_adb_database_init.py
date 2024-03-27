import unittest
import os
from shutil import rmtree
import address_app
from address_app.base.job_status import Status

TEST_ROOT = "tests/test_adbdatabase_base"  # This is the root path for the test database


class TestAdbBase(unittest.TestCase):
    """
    TestAdbBase class tests the initialization and basic functionality of the AdbDatabase class
    from the address_app package. It checks for the correct instantiation of the database with
    various root paths, verifies the singleton nature of the database instances, and ensures
    that the database paths are correctly set and handled.
    """

    def setUp(self):
        self.root = TEST_ROOT
        self.adb = address_app.AdbDatabase(self.root)

    def test_init(self):
        """
        Test the initialization of the AdbDatabase instances.

        Verifies that the AdbDatabase can be correctly instantiated with no root path, a string
        root path, an integer (which is an unconventional usage), and None as a root path. This
        test ensures that AdbDatabase is robust to various types of root path inputs.
        """
        self.assertIsNotNone(
            address_app.AdbDatabase(),
            "AdbDatabase instance should be created without a root path",
        )

        self.assertIsNotNone(
            address_app.AdbDatabase("tests"),
            "AdbDatabase instance should be created with a root path",
        )

        self.assertIsNotNone(
            address_app.AdbDatabase(123),
            "AdbDatabase instance should be created with a root path",
        )

        self.assertIsNotNone(
            address_app.AdbDatabase(None),
            "AdbDatabase instance should be created with a root path",
        )

    def test_singleton(self):
        """
        Test that the AdbDatabase behaves as a singleton.

        Verifies that multiple invocations of AdbDatabase with the same root path result in the
        same instance (demonstrating the singleton pattern), and that different root paths result
        in different instances.
        """
        same_path = os.path.abspath(self.root)
        same_adb = address_app.AdbDatabase(same_path)

        self.assertIs(
            self.adb,
            same_adb,
            "AdbDatabase instances with different roots should not be the same (singleton)",
        )

        other_adb = address_app.AdbDatabase()
        self.assertIsNot(
            self.adb,
            other_adb,
            "AdbDatabase instances with the same root should be the same (singleton)",
        )

    def test_database_paths(self):
        """
        Test that the database paths are set correctly.

        Ensures that the database root and storage file path are correctly determined and that
        the storage file exists within the filesystem. This test checks the integrity of the
        database's path handling functionalities.
        """
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
                    os.path.abspath(self.root),
                    address_app.base.consts.RELATIVE_STORAGE_PATH,
                )
            ),
            "Root path should match the provided path",
        )

    def tearDown(self):
        self.adb.clear()

    @classmethod
    def tearDownClass(cls):
        """
        Clean up after all tests in the class have been run.

        Specifically, deinitializes and removes leftover files for databases created with various
        root paths during testing. This comprehensive cleanup helps ensure that no artifacts remain
        that could affect other tests or the environment.
        """
        adb = address_app.AdbDatabase(TEST_ROOT)
        adb.deinit()
        adb_def = address_app.AdbDatabase("tests")
        adb_def.deinit()
        adb_def = address_app.AdbDatabase()
        adb_def.deinit()
        rmtree(TEST_ROOT)


if __name__ == "__main__":
    unittest.main()
