from ._strategy import SerializeStrategy
from ..exceptions import NotImplementerSerializationException


class CSVStrategy(SerializeStrategy):
    @classmethod
    def get_supported_extensions(cls) -> str:
        return ("csv",)

    @classmethod
    def serialize(cls, data: dict, url: str):
        raise NotImplementerSerializationException("CSV")
