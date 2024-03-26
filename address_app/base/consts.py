import re

#: Relative path to the storage file for database
RELATIVE_STORAGE_PATH = "adb/adb.pickle"

#: Validation regex for phone number
VALIDATE_PHONE_NO_REGEX = re.compile(r"^[0-9()\+\-\s]+$")
