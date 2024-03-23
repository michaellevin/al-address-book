from abc import ABC, abstractmethod


class SerializeStrategy(ABC):
    @abstractmethod
    def serialize(self, data: dict):
        pass
