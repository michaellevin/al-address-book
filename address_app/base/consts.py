import re
import tempfile

#: Default root path
DEFAULT_ROOT_PATH = tempfile.gettempdir()

#: Relative path to the storage file for database from the root path
RELATIVE_STORAGE_PATH = "adb/adb"

#: Default storage file path
DEFAULT_STORAGE_FULL_PATH = f"{DEFAULT_ROOT_PATH}/{RELATIVE_STORAGE_PATH}"

#: Validation regex for phone number: 0-9, (), +, -, space and empty string
VALIDATE_PHONE_NO_REGEX = re.compile(
    r"^(?:[0-9()\+\-\s]*|[\s]*)$"
)  # re.compile(r"^[0-9()\+\-\s]+$")
