from abc import ABC, abstractmethod


class IBaseFormatter(ABC):
    @abstractmethod
    def format(self, address_book) -> str:
        pass
