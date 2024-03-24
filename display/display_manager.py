from ..address_app.base.logger import logger
from ..address_app.model.address_book import AddressBook
from .strategies.formatter import FormatterRegistry
from ..address_app.base.exceptions import UnknownFormatterException


class DisplayManager:
    def __init__(self, address_book: AddressBook):
        self.address_book = address_book
        self.formatter = FormatterRegistry.get_formatter("text")

    def set_formatter(self, name: str):
        try:
            self.formatter = FormatterRegistry.get_formatter(name)
        except UnknownFormatterException as e:
            logger.error(e.message)

    def display(self):
        output = self.formatter.format(self.address_book)
        print(output)
        return output
