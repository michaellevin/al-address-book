from .base_serialization import ISerializeStrategy
from address_app.database.db_schema import DbSchema
from ..base.exceptions import NotImplementerSerializationException


class CSVStrategy(ISerializeStrategy):
    @classmethod
    def format(cls) -> str:
        return "csv"

    @classmethod
    def serialize(cls, data: DbSchema) -> str:
        # TODO here we should use two files, one for contacts and one for books
        raise NotImplementerSerializationException("CSV")

    @classmethod
    def deserialize(cls, data: str) -> DbSchema:
        # TODO here we should use two files, one for contacts and one for books
        raise NotImplementerSerializationException("CSV")
