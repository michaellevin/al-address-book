import pickle
from pathlib import Path
from threading import Lock

from .storage_interface import StorageInterface


class FileSystemStorage(StorageInterface):
    def __init__(self, file_path: Path):
        self._lock = Lock()
        self.file_path = file_path
        self.root = file_path.parent
        self.root.mkdir(parents=True, exist_ok=True)

    def save(self, data: dict):
        with self._lock:
            self._save(data)

    def _save(self, data: dict):
        with open(self.file_path, "wb") as file:
            pickle.dump(data, file)

    def read(self) -> dict:
        if not self.file_path.exists():
            return {}
        with open(self.file_path, "rb") as file:
            return pickle.load(file)

    def delete(self):
        try:
            self.file_path.unlink()
            if not any(self.root.iterdir()):
                self.root.rmdir()

        except FileNotFoundError:
            # TODO fix print statement -> exception

            print(f"File {self.file_path} not found for deletion")
            # raise
