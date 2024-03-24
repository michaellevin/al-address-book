from ..base.logger import logger
from ..model import AddressBook
from ..base.exceptions import UnknownFormatterException

from .formatter_registry import FormatterRegistry


class ViewManager:
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
