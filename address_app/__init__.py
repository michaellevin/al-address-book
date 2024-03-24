__version__ = "0.2.2"
__app_name__ = "address_app"

# initialize logger
from .base import logger, consts, exceptions

__all__ = ["AdbDatabase", "__app_name__", "__version__"]

from .database import AdbDatabase
from .view import ViewManager
from .serialize import SerializationManager
