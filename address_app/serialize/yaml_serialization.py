from ..database.db_schema import DbSchema
from .base_serialization import ISerializeStrategy
import yaml
from dataclasses import asdict


class YAMLStrategy(ISerializeStrategy):
    @classmethod
    def format(cls) -> str:
        return "yaml"

    @classmethod
    def serialize(cls, data: DbSchema) -> str:
        """Serialize the DbSchema object to a YAML string."""
        # Convert the DbSchema object to a dictionary before serialization
        schema_dict = asdict(data)
        return yaml.dump(schema_dict)

    @classmethod
    def deserialize(cls, schema_yaml: str) -> DbSchema:
        """Deserialize the YAML string back to a DbSchema object."""
        # Convert the YAML string to a dictionary and then to a DbSchema object
        schema_dict = yaml.safe_load(schema_yaml)
        return DbSchema(**schema_dict)
