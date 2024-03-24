from .base_serialization import SerializeStrategy
from ...base.exceptions import NotImplementerSerializationException


class CSVStrategy(SerializeStrategy):
    @classmethod
    def get_supported_extensions(cls) -> str:
        return ("csv",)

    @classmethod
    def serialize(cls, data: dict, url: str):
        raise NotImplementerSerializationException("CSV")
