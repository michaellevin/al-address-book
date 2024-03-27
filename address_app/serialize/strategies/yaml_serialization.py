import os
from .base_serialization import ISerializeStrategy
from ...base.aux_utils import try_import

# from ...base.exceptions import SerializationException


class YAMLStrategy(ISerializeStrategy):
    @classmethod
    def format(cls) -> str:
        return "YAML"

    @classmethod
    def get_supported_extensions(cls) -> str:
        return ("yml", "yaml")

    @classmethod
    def serialize(cls, data: dict, url: str):
        """Serialize the given data to YAML."""
        yaml_module = try_import("yaml")
        if yaml_module is None:
            raise ModuleNotFoundError("pyyaml")
            # raise FormatModuleNotInstalledException("pyyaml")
        os.makedirs(os.path.dirname(url), exist_ok=True)
        with open(url, "w") as file:
            yaml_module.dump(data, file, sort_keys=False)
