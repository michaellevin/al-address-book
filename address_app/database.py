import tempfile
import pickle
import typing
import logging
from pathlib import Path
from threading import Lock

from address_app import __app_name__

logger = logging.getLogger(__app_name__)
# print(__name__)

from ._singleton import SingletonMeta
from .address_book import AddressBook
from .exceptions import AddressBookExistsException


class AdbDatabase(metaclass=SingletonMeta):
    def __init__(self):
        self._lock = Lock()
        self.init()

    def init(self) -> None:
        """Create a db.adb file in Temp where all address books will be stored."""
        logger.info("Initializing database")

        self._db_folder = Path(tempfile.gettempdir()) / "adb"
        self._db_file = self._db_folder / "db.adb"
        self._db_folder.mkdir(parents=True, exist_ok=True)
        if not self._db_file.exists():
            self._address_books = {}
            self.save()
        else:
            self.read()

    @property
    def db_file(self):
        return self._db_file

    def create_address_book(self, name: str, exists_ok: bool = True) -> AddressBook:
        book = self.get_address_book(name)
        if book is not None:
            if exists_ok:
                logger.error(f"Address book {name} already exists")
                return book
            else:
                raise AddressBookExistsException(name)

        logger.info(f"Creating address book {name}")
        self._address_books[name] = AddressBook(name)
        self.save()
        return self._address_books[name]

    def get_address_book(self, name: str) -> AddressBook:
        logger.info(f"Getting address book {name}")
        return self._address_books.get(name)

    def delete_address_book(self, name: str) -> None:
        logger.info(f"Deleting address book {name}")
        if name in self._address_books:
            del self._address_books[name]
            self.save()

    def get_address_books(self) -> typing.Dict[str, AddressBook]:
        logger.info("Getting address books")
        return self._address_books

    def clear(self, book_name: str) -> None:
        logger.info(f"Clearing address book {book_name}")
        if book_name in self._address_books:
            self._address_books[book_name].clear()
            self.save()

    def clear_all(self) -> None:
        logger.info("Clearing all databases")
        self._address_books = {}
        self.save()

    def save(self) -> bool:
        logger.info("Saving database")
        with self._lock:
            with open(self._db_file, "wb") as f:
                pickle.dump(self._address_books, f)
        return True

    def read(self) -> bool:
        logger.info("Reading database")
        with open(self._db_file, "rb") as f:
            self._address_books = pickle.load(f)
        return True

    def enrich(self):
        logger.info("Enriching database")
        ...

    def deinit(self) -> None:
        logger.info("Deinitializing database")
        with self._lock:
            # Delete the database file if it exists
            if self._db_file.exists():
                self._db_file.unlink()
                logger.info(f"Deleted database file at {self._db_file}")

            # Remove the database folder if it's empty
            if not any(self._db_folder.iterdir()):
                self._db_folder.rmdir()
                logger.info(f"Removed empty database folder at {self._db_folder}")

            # Clear in-memory data
            self._address_books = {}
            logger.info("Cleared in-memory address book data.")
