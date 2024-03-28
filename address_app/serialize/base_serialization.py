from abc import ABC, abstractmethod
from ..database.db_schema import DbSchema


class ISerializeStrategy(ABC):
    @classmethod
    @abstractmethod
    def format(cls) -> str:
        """Return the format of the serialization strategy, e.g., "JSON", "XML", "YAML" """
        pass

    @classmethod
    @abstractmethod
    def serialize(cls, data: DbSchema) -> str:
        """Takes DbSchema object and serializes it."""
        pass

    @classmethod
    @abstractmethod
    def deserialize(cls, data: str) -> DbSchema:
        """Takes a string and deserializes it into a DbSchema object."""
        pass
