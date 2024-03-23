__version__ = "0.2.0"
__app_name__ = "address_app"

# initialize logger
from .logger import logger

__all__ = ["AdbDatabase", "__app_name__", "__version__"]

from .database import AdbDatabase
