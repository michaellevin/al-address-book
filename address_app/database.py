from typing import Optional, Union, Dict
from pathlib import Path

from .base import get_logger
from .model import AddressBook
from .storage import FileSystemStorage

logger = get_logger()


class _SingletonRootMeta(type):
    """
    A metaclass for creating singleton instances based on a root path.
    Singleton instances are created once per root path. If an instance with
    the same root path (specified in any way) is requested again, the original instance is returned.

    Attributes:
        _instances (dict): A dictionary holding instances, keyed by root path.
        _default_key (str): The default key used when no root path is specified.
    """

    _instances = {}
    _default_key = "default"

    def __call__(cls, *args, **kwargs):
        key = cls._default_key
        try:
            if args:
                root_arg = args[0]
                key = str(Path(root_arg).resolve(strict=False))
            elif "root" in kwargs and (root_arg := kwargs["root"]) is not None:
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
        self.storage = FileSystemStorage(root)
        self._read()

    @property
    def root(self) -> str:
        """
        Returns the root path for the database storage.

        Returns:
            str: The root path for the database storage.
        """
        return self.storage.get_root_as_str()

    @property
    def storage_filepath(self) -> str:
        """
        Returns the file path for the database storage.
        The actual database is stored in a file within the root directory: `<root>/adb/adb.pickle`.

        Returns:
            str: The file path for the database storage.
        """
        return self.storage.get_filepath_as_str()

    def create_address_book(self, name: str) -> AddressBook:
        """
        Creates and returns a new address book with the given name.

        Args:
            name (str): The name of the address book to create.

        Returns:
            AddressBook: The newly created address book.
        """
        book = self.get_address_book(name)
        if book is not None:
            logger.warning(f"Address Book {name} already exists")
            return book

        logger.debug(f"Creating address book {name}")
        self._address_books[name] = AddressBook(name)
        self._save()
        return self._address_books[name]

    def get_address_book(self, name: Optional[str] = None) -> Union[AddressBook, None]:
        """
        Retrieves an address book by name or the first available one if no name is provided.

        Args:
            name (Optional[str]): The name of the address book to retrieve. If None, returns the first address book.

        Returns:
            AddressBook or None: The requested address book, or None if not found.
        """
        if name is None:
            all_books = self.get_address_books()
            if all_books:
                return list(all_books.values())[0]
            return None

        return self._address_books.get(name)

    def delete_address_book(self, name: str) -> None:
        """
        Deletes an address book by name.

        Args:
            name (str): The name of the address book to delete.
        """
        if name in self._address_books:
            logger.debug(f"Deleting address book {name}")
            del self._address_books[name]
            self._save()
        else:
            logger.warning(f"Address Book {name} does not exist")

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

    def _save(self) -> bool:
        """
        Saves the current state of the database to persistent storage.

        Returns:
            bool: True if the save operation was successful, False otherwise.
        """
        self.storage.save(self._address_books)
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

        Args:
            root (Optional[str]): The root directory of the database to deinitialize.
        """

        # TODO check deinitialization logic

        logger.debug("Deinitializing database")
        self.clear()
        self.storage.delete()
        self.storage = None
        logger.debug("Cleared in-memory address book data.")
