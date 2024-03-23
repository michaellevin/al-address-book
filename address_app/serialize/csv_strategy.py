from ._strategy import SerializeStrategy


class CSVStrategy(SerializeStrategy):
    def serialize(self, data: dict):
        raise NotImplementedError("Not implemented yet")
