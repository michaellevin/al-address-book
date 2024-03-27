from .base_serialization import ISerializeStrategy
from ...base.exceptions import NotImplementerSerializationException


class CSVStrategy(ISerializeStrategy):
    @classmethod
    def format(cls) -> str:
        return "CSV"

    @classmethod
    def get_supported_extensions(cls) -> str:
        return ("csv",)

    @classmethod
    def serialize(cls, data: dict, url: str):
        raise NotImplementerSerializationException("CSV")
