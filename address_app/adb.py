from typing import Optional, Union, Dict
from pathlib import Path

from .base import get_logger
from .serialize import SerializeStrategyRegistry, get_supported_formats
from .storage import DbFileSystemStorage
from .database import DatabaseManager
from .view import ViewerRegistry

logger = get_logger()


class _SingletonRootMeta(type):
    """
    A metaclass for creating singleton instances based on a root path.
    Singleton instances are created once per root path. If an instance with
    the same root path (specified in any way) is requested again, the original instance is returned.

    Attributes:
        _instances (dict): A dictionary holding instances, keyed by root path.
        _default_key (str): The default key used when no root path is specified.

    Usage example:
        class RootPathSingleton(metaclass=_SingletonRootMeta):
            def __init__(self, root=None):
                self.root = root or "default_path"

        # Creating instances
        instance_a = RootPathSingleton("/path/to/root")
        instance_b = RootPathSingleton("/path/to/root")  # This will return the same instance as instance_a
        instance_c = RootPathSingleton()  # This will create a new instance with the default path

        assert instance_a is instance_b  # True, because they refer to the same instance
        assert instance_a is not instance_c  # True, because they are different instances
    """

    _instances = {}
    _default_key = "default"

    def __call__(cls, *args, **kwargs):
        key = cls._default_key
        try:
            if args:
                root_arg = args[0]
                key = str(Path(root_arg).resolve(strict=False))
            elif "root" in kwargs and kwargs["root"] is not None:
                root_arg = kwargs["root"]
                key = str(Path(root_arg).resolve(strict=False))
        except Exception as e:
            logger.error(f"Invalid root path provided: {root_arg}. Using default.")

        if key not in cls._instances:
            cls._instances[key] = super().__call__(*args, **kwargs)
        return cls._instances[key]

    @classmethod
    def clear_instances(cls):
        """Utility method to clear instances, mainly for testing purposes."""
        cls._instances.clear()


class AdbConnector(metaclass=_SingletonRootMeta):
    """
    Provides functionality for managing address books with persistent storage.

    Each database instance is associated with a root storage path. This class
    allows for creating, retrieving, and managing address books.

    Args:
        root (Optional[str]): The root directory for database storage. If not specified, a default location is used.

    Methods are documented with their functionality.
    """

    def __init__(self, root: Optional[str] = None, format: Optional[str] = "json"):
        if format and format not in get_supported_formats():
            logger.warning(
                f"Unsupported serialization format: {format}. Using default: json"
            )
        strategy = SerializeStrategyRegistry.get_strategy_for_extension(format)
        self._storage = DbFileSystemStorage(strategy, root)
        self._db_manager = DatabaseManager(self._storage)

    @property
    def db_manager(self) -> DatabaseManager:
        """
        Returns the database manager instance associated with the database.

        Returns:
            DatabaseManager: The database manager instance.
        """
        return self._db_manager

    @property
    def root(self) -> str:
        """
        Returns the root path for the database storage.

        Returns:
            str: The root path for the database storage.
        """
        return self._storage.root_as_str()

    @property
    def storage_filepath(self) -> str:
        """
        Returns the file path for the database storage.
        The actual database is stored in a file within the root directory: `<root>/adb/adb.pickle`.

        Returns:
            str: The file path for the database storage.
        """
        return self._storage.filepath_as_str()

    def change_strategy(self, format: str) -> None:
        """
        Changes the serialization strategy for the database storage.

        Args:
            format (str): The format of the serialization strategy to use.
        """
        if format not in get_supported_formats():
            logger.warning(
                f"Unsupported serialization format: {format}. Using default: json"
            )
        self._storage.set_strategy(
            SerializeStrategyRegistry.get_strategy_for_extension(format)
        )

    def render(self, format: str = "html") -> Union[str, None]:
        """
        Renders the database contents using the specified format.

        Args:
            format (str): The format to render the database contents in.

        Returns:
            Union[str, None]: The rendered database contents as a string, or None if rendering failed.
        """
        return ViewerRegistry.render(self._storage.read(), format)

    def delete(self) -> None:
        """Deletes the database storage file and its parent directory if it is empty."""
        self._storage.delete()
