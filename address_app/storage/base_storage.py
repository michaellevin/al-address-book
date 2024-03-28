from abc import ABC, abstractmethod

# TODO: Implement the Factory pattern for creating different storage objects


class IStorage(ABC):
    @abstractmethod
    def write(self, data):
        pass

    @abstractmethod
    def read(self):
        pass
