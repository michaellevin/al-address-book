__app_name__ = "address_app"
__version__ = "0.2.3"
__all__ = ["AdbDatabase", "__app_name__", "__version__"]

# initialize logger
from .base import get_logger, consts, exceptions


from .database import AdbDatabase
from .model import AddressBook
from .view import ViewManager
from .serialize import SerializationManager
