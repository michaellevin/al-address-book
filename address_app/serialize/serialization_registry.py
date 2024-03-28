from typing import List

from .json_serialization import JSONStrategy
from .xml_serialization import XMLStrategy
from .yaml_serialization import YAMLStrategy

# from .strategies.csv_serialization import CSVStrategy

from ..base.exceptions import NoAvailableSerializationException


class SerializeStrategyRegistry:

    _strategies = {}

    @classmethod
    def register_strategy(cls, strategy):
        cls._strategies[strategy.format()] = strategy

    @classmethod
    def get_supported_formats(cls) -> List[str]:
        return cls._strategies.keys()

    @classmethod
    def get_strategy_for_extension(cls, format: str = "json"):
        strategy = cls._strategies.get(format)
        if not strategy:
            raise NoAvailableSerializationException(format.capitalize())
        return strategy


def get_supported_formats() -> List[str]:
    """Return a list of supported serialization formats.

    Example:
    >>> get_supported_serialization_formats()
    ['JSON', 'XML', 'YAML']
    """
    return SerializeStrategyRegistry.get_supported_formats()


SerializeStrategyRegistry.register_strategy(JSONStrategy)
SerializeStrategyRegistry.register_strategy(XMLStrategy)
SerializeStrategyRegistry.register_strategy(YAMLStrategy)
# SerializeStrategyRegistry.register_strategy(CSVStrategy)
