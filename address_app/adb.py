from typing import Optional, Union, Dict
from pathlib import Path

from .base import get_logger
from .base.job_status import JobStatus, Status
from .model import AddressBook
from .storage import DbFileSystemStorage

logger = get_logger()


class _SingletonRootMeta(type):
    """
    A metaclass for creating singleton instances based on a root path.
    Singleton instances are created once per root path. If an instance with
    the same root path (specified in any way) is requested again, the original instance is returned.

    Attributes:
        _instances (dict): A dictionary holding instances, keyed by root path.
        _default_key (str): The default key used when no root path is specified.

    Usage example:
        class RootPathSingleton(metaclass=_SingletonRootMeta):
            def __init__(self, root=None):
                self.root = root or "default_path"

        # Creating instances
        instance_a = RootPathSingleton("/path/to/root")
        instance_b = RootPathSingleton("/path/to/root")  # This will return the same instance as instance_a
        instance_c = RootPathSingleton()  # This will create a new instance with the default path

        assert instance_a is instance_b  # True, because they refer to the same instance
        assert instance_a is not instance_c  # True, because they are different instances
    """

    _instances = {}
    _default_key = "default"

    def __call__(cls, *args, **kwargs):
        key = cls._default_key
        try:
            if args:
                root_arg = args[0]
                key = str(Path(root_arg).resolve(strict=False))
            elif "root" in kwargs and kwargs["root"] is not None:
                root_arg = kwargs["root"]
                key = str(Path(root_arg).resolve(strict=False))
        except Exception as e:
            logger.error(f"Invalid root path provided: {root_arg}. Using default.")

        if key not in cls._instances:
            cls._instances[key] = super().__call__(*args, **kwargs)
        return cls._instances[key]

    @classmethod
    def clear_instances(cls):
        """Utility method to clear instances, mainly for testing purposes."""
        cls._instances.clear()


class AdbDatabase(metaclass=_SingletonRootMeta):
    """
    Provides functionality for managing address books with persistent storage.

    Each database instance is associated with a root storage path. This class
    allows for creating, retrieving, and managing address books.

    Args:
        root (Optional[str]): The root directory for database storage. If not specified, a default location is used.

    Methods are documented with their functionality.
    """

    def __init__(self, root: Optional[str] = None):
        self.init(root)

    def init(self, root: Optional[Path] = None) -> None:
        """
        Sets up the database storage and reads the existing data from storage.

        Args:
            root (Path): The root path for the database storage.
        """
        logger.debug("Initializing database")
        self.storage = DbFileSystemStorage(root)
        self._read()

    @property
    def root(self) -> str:
        """
        Returns the root path for the database storage.

        Returns:
            str: The root path for the database storage.
        """
        return self.storage.root_as_str()

    @property
    def storage_filepath(self) -> str:
        """
        Returns the file path for the database storage.
        The actual database is stored in a file within the root directory: `<root>/adb/adb.pickle`.

        Returns:
            str: The file path for the database storage.
        """
        return self.storage.filepath_as_str()

    def create_address_book(self, name: str) -> JobStatus:
        """
        Creates and returns a new address book with the given name.
        If an address book with the same name already exists, returns the existing address book.

        Args:
            name (str): The name of the address book to create.

        Returns:
            JobStatus: An object indicating the success or failure of the
            operation, including the created address book on success or if it already exists.
        """
        book = self.get_address_book(name)
        if book is not None:
            message = f"Address Book '{name}' already exists."
            logger.warning(message)
            # If returning the book is essential, consider including it in the return_value of JobStatus
            return JobStatus(Status.CANCELLED, book, message)

        try:
            logger.debug(f"Creating address book '{name}'")
            self._address_books[name] = AddressBook(name)
            self._save()
            message = f"Address book '{name}' created successfully."
            return JobStatus(Status.SUCCESS, self._address_books[name], message)
        except Exception as e:
            logger.error(f"Failed to create address book '{name}': {e}")
            return JobStatus(
                Status.ERROR,
                None,
                f"Failed to create address book '{name}'. Error: {e}",
            )

    def get_address_book(self, name: Optional[str]) -> Union[AddressBook, None]:
        """
        Retrieves an address book by name or the first available one if no name is provided.

        Args:
            name (Optional[str]): The name of the address book to retrieve. If None, returns the first address book.

        Returns:
            AddressBook or None: The requested address book, or None if not found.
        """
        all_books = self._address_books
        if name is None and all_books:
            return list(all_books.values())[0]
        return all_books.get(name)

    def delete_address_book(self, name: str) -> JobStatus:
        """
        Deletes an address book by name.

        Args:
            name (str): The name of the address book to delete.

        Returns:
            JobStatus: An object indicating the success or failure of the operation.

        """
        if name in self._address_books:
            logger.debug(f"Deleting address book {name}")
            del self._address_books[name]
            self._save()
            return JobStatus(Status.SUCCESS, None, f"Address book '{name}' deleted.")
        else:
            logger.warning(f"Address Book {name} does not exist")
            return JobStatus(
                Status.CANCELLED, None, f"Address book '{name}' does not exist."
            )

    def get_address_books(self) -> Dict[str, AddressBook]:
        """
        Retrieves all address books in the database.

        Returns:
            Dict[str, AddressBook]: A dictionary of all address books, keyed by their name.
        """
        logger.debug("Getting address books")
        return self._address_books

    def clear(self) -> None:
        """
        Clears all data from the database, removing all address books.
        """
        logger.debug("Clearing Database: Remove all the address books")
        self._address_books = {}
        self._save()

    def add_contact(
        self, book_name: str, name: str, address: str, phone_no: Optional[str]
    ) -> JobStatus:
        """
        Adds a new contact to the specified address book.

        Args:
            book_name (str): The name of the address book to add the contact to.
            name (str): The name of the contact.
            address (str): The address of the contact.
            phone_no (Optional[str]): The phone number of the contact.

        Returns:
            JobStatus: An object indicating the success or failure of the operation.
        """
        book = self.get_address_book(book_name)
        if book is None:
            message = f"Address book '{book_name}' not found."
            logger.warning(message)
            return JobStatus(Status.ERROR, None, message)

        job_output = book.add_record(name, address, phone_no)
        self._save()
        return job_output

    def find_contacts(self, book_name: str, **criteria) -> list:
        """
        Finds contacts in the specified address book based on the provided criteria.

        Args:
            book_name (str): The name of the address book to search in.
            **criteria: The search criteria to match contacts against.

        Returns:
            list: A list of contacts that match the search criteria.
        """
        book = self.get_address_book(book_name)
        if book is None:
            logger.warning(f"Address book '{book_name}' not found.")
            return []

        return book.find_contacts(**criteria)

    def clear_book_contents(self, book_name: str) -> None:
        """
        Clears all contacts from the specified address book.

        Args:
            book_name (str): The name of the address book to clear.
        """
        logger.debug(f"Clearing address book {book_name}: Remove all contacts")
        if book_name in self._address_books:
            self._address_books[book_name].clear()
            self._save()

    def _save(self) -> bool:
        """
        Saves the current state of the database to persistent storage.

        Returns:
            bool: True if the save operation was successful, False otherwise.
        """
        self.storage.write(self._address_books)
        return True

    def _read(self) -> bool:
        """
        Loads the database state from persistent storage.

        Returns:
            bool: True if the read operation was successful, False otherwise.
        """
        self._address_books = self.storage.read() or {}
        return True

    def deinit(self) -> None:
        """
        Deinitializes the database and optionally clears the storage.
        """

        logger.debug("Deinitializing database")
        self.clear()
        self.storage.delete()
        self.storage = None
        logger.debug("Cleared in-memory address book data.")
