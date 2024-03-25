import pickle
import tempfile
from typing import Optional
from pathlib import Path
from threading import Lock

from .storage_interface import StorageInterface
from ..base.consts import RELATIVE_STORAGE_PATH


class FileSystemStorage(StorageInterface):
    def __init__(self, root: Optional[Path] = None):
        if root is None:
            root = tempfile.gettempdir()
        self.root = Path(root)
        self.storage_filepath = self.root / RELATIVE_STORAGE_PATH
        self.storage_filepath.parent.mkdir(parents=True, exist_ok=True)

        self._lock = Lock()

    def save(self, data: dict):
        with self._lock:
            self._save(data)

    def _save(self, data: dict):
        with open(self.storage_filepath, "wb") as file:
            pickle.dump(data, file)

    def read(self) -> dict:
        if not self.storage_filepath.exists():
            return {}
        with open(self.storage_filepath, "rb") as file:
            return pickle.load(file)

    def delete(self):
        try:
            self.storage_filepath.parent.rmdir()
            # self.storage_filepath.unlink()
            # if not any(self.root.iterdir()):
            #     self.root.rmdir()

        except FileNotFoundError:
            # TODO fix print statement -> exception

            print(f"File {self.storage_filepath} not found for deletion")
            # raise

    def get_root_as_str(self) -> str:
        return str(self.root.resolve())

    def get_filepath_as_str(self) -> str:
        return str(self.storage_filepath.resolve())
