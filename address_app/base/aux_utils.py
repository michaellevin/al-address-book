import hashlib
import importlib
from types import ModuleType
from typing import Union
from pathlib import Path
from .logger import get_logger

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


def try_import(module_name: str) -> Union[ModuleType, None]:
    """Try to import a module and return True if successful."""
    try:
        return importlib.import_module(module_name)
    except ImportError:
        return None


def hash_input(input: str) -> int:
    """Generate a unique identifier from the input string."""
    url_hash = hashlib.sha256(input.encode()).hexdigest()
    unique_id = int(url_hash[:8], 16)
    return unique_id
