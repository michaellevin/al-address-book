from ._strategy import SerializeStrategy


class JSONStrategy(SerializeStrategy):
    @classmethod
    def get_supported_extensions(cls) -> tuple[str]:
        return ("json",)

    @classmethod
    def serialize(cls, data: dict, url: str):
        import json

        with open(url, "w") as file:
            json.dump(data, file)
