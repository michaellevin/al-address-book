from abc import ABC, abstractmethod


class IStorage(ABC):
    @abstractmethod
    def save(self, data: dict):
        pass

    @abstractmethod
    def read(self) -> dict:
        pass

    @abstractmethod
    def delete(self):
        pass
