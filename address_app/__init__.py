__app_name__ = "address_app"
__version__ = "0.2.3"

# initialize logger
from .base import get_logger, consts, exceptions

__all__ = ["AdbDatabase", "__app_name__", "__version__"]

from .database import AdbDatabase
from .view import ViewManager
from .serialize import SerializationManager
