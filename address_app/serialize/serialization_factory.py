from .serialization_registry import SerializeStrategyRegistry
from .strategies.base_serialization import ISerializeStrategy


class SerializeStrategyFactory:
    @staticmethod
    def get_strategy(url: str) -> ISerializeStrategy:
        """Get the appropriate serialization strategy for the given URL."""
        # Extract the file extension from the URL
        extension = url.rsplit(".", 1)[-1].lower()

        # Use the registry to find and instantiate the appropriate strategy
        return SerializeStrategyRegistry.get_strategy_for_extension(extension)
