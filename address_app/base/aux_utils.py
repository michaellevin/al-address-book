import hashlib
import importlib
from types import ModuleType
from typing import Union


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
