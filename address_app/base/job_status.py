from typing import Any
from .enums import Status


class JobStatus:
    """Encapsulates the status, return value, and description of a job operation.

    This class is used to convey the outcome of an operation, including whether
    it succeeded, failed, or was cancelled, alongside any relevant return values
    and a descriptive message detailing the outcome.

    Attributes:
        status (Status): The status of the operation.
        return_value (Any): The return value of the operation, if any.
        message (str): A descriptive message about the operation's outcome.

    """

    def __init__(self, status: Status, return_value: Any, message: str):
        self.status = status
        self.return_value = return_value
        self.message = message

    def __repr__(self):
        return f"JobStatus(status={self.status}, return_value={self.return_value}, description='{self.message}'"
