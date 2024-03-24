from ._strategy import SerializeStrategy


class YAMLStrategy(SerializeStrategy):
    @classmethod
    def get_supported_extensions(cls) -> str:
        return ("yml", "yaml")

    @classmethod
    def serialize(cls, data: dict, url: str):
        """Serialize the given data to YAML."""
        import yaml

        with open(url, "w") as file:
            yaml.dump(data, file)
