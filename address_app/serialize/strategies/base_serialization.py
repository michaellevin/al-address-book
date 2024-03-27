from abc import ABC, abstractmethod
from typing import Tuple


class ISerializeStrategy(ABC):
    @classmethod
    @abstractmethod
    def format(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def serialize(cls, data: dict, url: str):
        pass

    @classmethod
    @abstractmethod
    def get_supported_extensions(cls) -> Tuple[str]:
        pass

    @classmethod
    def supports_url_extension(cls, url: str) -> bool:
        url_lower = url.lower()
        return any(
            url_lower.endswith(f".{ext.lower()}")
            for ext in cls.get_supported_extensions()
        )
