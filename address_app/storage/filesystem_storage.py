from typing import Optional
from pathlib import Path
from threading import Lock
from shutil import rmtree

from .base_storage import IStorage
from ..base import get_logger
from ..base.consts import DEFAULT_ROOT_PATH, RELATIVE_STORAGE_PATH
from ..database.db_schema import DbSchema
from ..serialize.base_serialization import ISerializeStrategy


class DbFileSystemStorage(IStorage):
    """File system storage implementation for the database."""

    def __init__(self, strategy: ISerializeStrategy, root: Optional[Path]):
        if root is None:
            root = DEFAULT_ROOT_PATH
        self._root = Path(root)
        self._storage_filepath = None
        self._lock = Lock()
        self.set_strategy(strategy)

    def set_strategy(self, strategy: ISerializeStrategy):
        db_schema = self.read()
        self._strategy = strategy
        self._storage_filepath = (
            self._root / f"{RELATIVE_STORAGE_PATH}.{self._strategy.format()}"
        )
        self._create_storage_file(db_schema)

    def _create_storage_file(self, db_schema: DbSchema):
        self._storage_filepath.parent.mkdir(parents=True, exist_ok=True)
        if not self._storage_filepath.exists():
            self.write(db_schema)

    def is_initialized(self) -> bool:
        return self._storage_filepath.exists()

    def write(self, data: DbSchema):
        with self._lock:
            data_serialized = self._strategy.serialize(data=data)
            with open(self._storage_filepath, "w") as file:
                file.write(data_serialized)

    def read(self) -> DbSchema:
        if not self._storage_filepath or not self._storage_filepath.exists():
            # get_logger().error(f"File {self._storage_filepath} not found for reading")
            return DbSchema()

        with open(self._storage_filepath, "r") as file:
            return self._strategy.deserialize(data=file.read())

    def delete(self):
        """Delete the storage file and its parent directory if it is empty"""
        try:
            self._storage_filepath.unlink()

            rmtree(self._storage_filepath.parent)
            # self._storage_filepath.parent.rmdir()

        except FileNotFoundError:
            get_logger().error(f"File {self._storage_filepath} not found for deletion")

    def root_as_str(self) -> str:
        return str(self._root.resolve())

    def filepath_as_str(self) -> str:
        return str(self._storage_filepath.resolve())
