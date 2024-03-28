from dataclasses import asdict
import json

from ..database.db_schema import DbSchema

from .base_serialization import ISerializeStrategy


class JSONStrategy(ISerializeStrategy):

    @classmethod
    def format(cls) -> str:
        return "json"

    @classmethod
    def serialize(cls, data: DbSchema) -> str:
        # Convert the DbSchema object to a dictionary and then to a JSON string
        schema_dict = asdict(data)
        return json.dumps(schema_dict)

    @classmethod
    def deserialize(cls, data: str) -> DbSchema:
        # Convert the JSON string back to a dictionary and then to a DbSchema object
        # schema_dict = json.loads(data)
        # return DbSchema(**schema_dict)

        schema_dict = json.loads(data)

        # Convert contact IDs in 'contacts' back to integers
        contacts_converted = {int(k): v for k, v in schema_dict["contacts"].items()}

        # Convert contact IDs in 'books' back to integers
        books_converted = {}
        for book_name, ids in schema_dict["books"].items():
            books_converted[book_name] = [int(id_) for id_ in ids]

        return DbSchema(contacts=contacts_converted, books=books_converted)
