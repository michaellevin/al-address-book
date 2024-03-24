from .json_strategy import JSONStrategy
from .xml_strategy import XMLStrategy
from .yaml_strategy import YAMLStrategy
from .csv_strategy import CSVStrategy


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
            raise ValueError(f"No strategy found for extension: {ext}")
        return strategy


SerializeStrategyRegistry.register_strategy(JSONStrategy)
SerializeStrategyRegistry.register_strategy(XMLStrategy)
SerializeStrategyRegistry.register_strategy(YAMLStrategy)
SerializeStrategyRegistry.register_strategy(CSVStrategy)
