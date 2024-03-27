from enum import Enum, auto


class Status(Enum):
    """Enumeration of possible statuses for job operations.

    Attributes:
        SUCCESS: Indicates the operation completed successfully.
        ERROR: Indicates the operation encountered an error.
        CANCELLED: Indicates the operation was cancelled for some reason.
    """

    SUCCESS = auto()
    ERROR = auto()
    CANCELLED = auto()
