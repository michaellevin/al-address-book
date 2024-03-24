from ..base.logger import logger

from ..model import AddressBook
from . import SerializeStrategyFactory
from ..base.exceptions import SerializationException


class SerializationManager:
    def __init__(self, address_book: AddressBook):
        self.address_book = address_book

    def serialize(self, url: str) -> bool:
        # Determine the appropriate serialization strategy based on the URL or file extension
        try:
            strategy = SerializeStrategyFactory.get_strategy(url)
            data = self.address_book.to_dict()
            strategy.serialize(data, url)
            return True
        except SerializationException as e:
            logger.error(e.message)
            return False
