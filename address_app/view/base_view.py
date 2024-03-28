from ..database.db_schema import DbSchema
from abc import ABC, abstractmethod


class IViewer(ABC):
    @classmethod
    @abstractmethod
    def name(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def render(cls, db: DbSchema):
        pass
