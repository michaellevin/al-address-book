from typing import Tuple


from .base_serialization import ISerializeStrategy


class JSONStrategy(ISerializeStrategy):

    @classmethod
    def format(cls) -> str:
        return "JSON"

    @classmethod
    def get_supported_extensions(cls) -> Tuple[str]:
        return ("json",)

    @classmethod
    def serialize(cls, data: dict, url: str):
        import json
        import os

        os.makedirs(os.path.dirname(url), exist_ok=True)
        with open(url, "w") as file:
            json.dump(data, file)
