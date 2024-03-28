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
    def deserialize(cls, schema_json: str) -> DbSchema:
        # Convert the JSON string back to a dictionary and then to a DbSchema object
        schema_dict = json.loads(schema_json)
        return DbSchema(**schema_dict)
