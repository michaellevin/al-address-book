from abc import ABC, abstractmethod


class FormatterStrategy(ABC):
    @abstractmethod
    def format(self, address_book) -> str:
        pass
