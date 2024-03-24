from .strategies.json_serialization import JSONStrategy
from .strategies.xml_serialization import XMLStrategy
from .strategies.yaml_serialization import YAMLStrategy
from .strategies.csv_serialization import CSVStrategy

from ..base.exceptions import NoAvailableSerializationException


class SerializeStrategyRegistry:
    _strategies = {}

    @classmethod
    def register_strategy(cls, strategy):
        for ext in strategy.get_supported_extensions():
            if ext in cls._strategies:
                raise ValueError(f"Duplicate extension found: {ext}")
            cls._strategies[ext] = strategy

    @classmethod
    def get_supported_extensions(cls) -> list[str]:
        return list(cls._strategies.keys())

    @classmethod
    def get_strategy_for_extension(cls, ext: str):
        strategy = cls._strategies.get(ext)
        if not strategy:
            raise NoAvailableSerializationException(ext.capitalize())
        return strategy


SerializeStrategyRegistry.register_strategy(JSONStrategy)
SerializeStrategyRegistry.register_strategy(XMLStrategy)
SerializeStrategyRegistry.register_strategy(YAMLStrategy)
SerializeStrategyRegistry.register_strategy(CSVStrategy)
