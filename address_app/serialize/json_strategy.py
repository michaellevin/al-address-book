from ._strategy import SerializeStrategy


class JSONStrategy(SerializeStrategy):
    def serialize(self, data: dict): ...
