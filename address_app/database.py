import tempfile
import typing
from pathlib import Path

from .base import get_logger, SingletonMeta
from .model import AddressBook
from .storage import FileSystemStorage

logger = get_logger()


class AdbDatabase(metaclass=SingletonMeta):
    def __init__(self):

        self.init()

    def init(self) -> None:
        logger.info("Initializing database")
        storage_path = Path(tempfile.gettempdir()) / "adb" / "adb.pickle"
        self.storage = FileSystemStorage(storage_path)
        self.read()

    def create_address_book(self, name: str) -> AddressBook:
        book = self.get_address_book(name)
        if book is not None:
            logger.warning(f"Address Book {name} already exists")
            return book

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

    def clear_book(self, book_name: str) -> None:
        logger.info(f"Clearing address book {book_name}")
        if book_name in self._address_books:
            self._address_books[book_name].clear()
            self.save()

    def remove_book(self, book_name: str) -> None:
        logger.info(f"Removing address book {book_name}")
        if book_name in self._address_books:
            del self._address_books[book_name]
            self.save()

    def clear(self) -> None:
        logger.info("Clearing all databases")
        self._address_books = {}
        self.save()

    def save(self) -> bool:
        self.storage.save(self._address_books)
        return True

    def read(self) -> bool:
        self._address_books = self.storage.read() or {}
        return True

    def enrich(self): ...

    def deinit(self) -> None:
        logger.info("Deinitializing database")
        self.storage.delete()

        # Clear in-memory data
        self._address_books = {}
        logger.info("Cleared in-memory address book data.")
