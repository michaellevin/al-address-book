from abc import ABC, abstractmethod


class ISerializeStrategy(ABC):
    @classmethod
    @abstractmethod
    def serialize(cls, data: dict, url: str):
        pass

    @classmethod
    @abstractmethod
    def get_supported_extensions(cls) -> tuple[str]:
        pass

    @classmethod
    def supports_url_extension(cls, url: str) -> bool:
        url_lower = url.lower()
        return any(
            url_lower.endswith(f".{ext.lower()}")
            for ext in cls.get_supported_extensions()
        )
