from typing import List

from .strategies.json_serialization import JSONStrategy
from .strategies.xml_serialization import XMLStrategy
from .strategies.yaml_serialization import YAMLStrategy
from .strategies.csv_serialization import CSVStrategy

from ..base.exceptions import NoAvailableSerializationException


class SerializeStrategyRegistry:
    """
    A registry for serialization strategies, allowing dynamic registration and retrieval
    of strategies based on file extensions.

    This class maintains a registry of available serialization strategies (like JSON, XML, YAML, CSV)
    and provides class methods to register new strategies, list supported extensions, and retrieve
    a strategy for a given extension.

    Attributes:
        _strategies (dict): A private dictionary mapping file extensions to their respective
                            serialization strategy classes.

    Examples:
        Registering a new strategy:

        >>> SerializeStrategyRegistry.register_strategy(JSONStrategy)

        Getting a strategy for a specific extension:

        >>> json_strategy = SerializeStrategyRegistry.get_strategy_for_extension('json')
        >>> print(json_strategy.__name__)
        JSONStrategy
    """

    _strategies = {}

    @classmethod
    def register_strategy(cls, strategy):
        """
        Registers a new serialization strategy.

        Args:
            strategy: The serialization strategy class to register. It must have a
                      `get_supported_extensions` class method that returns a list of supported file extensions.

        Raises:
            ValueError: If a duplicate file extension is found in the registry.

        Examples:
            >>> SerializeStrategyRegistry.register_strategy(XMLStrategy)
        """
        for ext in strategy.get_supported_extensions():
            if ext in cls._strategies:
                raise ValueError(f"Duplicate extension found: {ext}")
            cls._strategies[ext] = strategy

    @classmethod
    def get_supported_formats(cls) -> List[str]:
        """Returns a list of supported serialization formats.

        Returns:
            A list of strings representing the serialization formats supported by the registered
            serialization strategies.


        Example:
            >>> SerializeStrategyRegistry.get_supported_formats()
            ['JSON', 'XML', 'YAML']

        """
        return list(set(strategy.format() for strategy in cls._strategies.values()))

    @classmethod
    def get_supported_extensions(cls) -> List[str]:
        """
        Returns a list of supported file extensions for serialization.

        Returns:
            A list of strings representing the file extensions supported by the registered
            serialization strategies.

        Examples:
            >>> SerializeStrategyRegistry.get_supported_extensions()
            ['json', 'xml', 'yaml', 'csv']
        """
        return list(cls._strategies.keys())

    @classmethod
    def get_strategy_for_extension(cls, ext: str):
        """
        Retrieves the serialization strategy class for a given file extension.

        Args:
            ext (str): The file extension for which to retrieve the serialization strategy.

        Returns:
            The serialization strategy class associated with the provided file extension.

        Raises:
            NoAvailableSerializationException: If no strategy is found for the given extension.

        Examples:
            >>> yaml_strategy = SerializeStrategyRegistry.get_strategy_for_extension('yaml')
            >>> print(yaml_strategy.__name__)
            YAMLStrategy
        """
        strategy = cls._strategies.get(ext)
        if not strategy:
            raise NoAvailableSerializationException(ext.capitalize())
        return strategy


def get_supported_serialization_formats() -> List[str]:
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
