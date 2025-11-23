"""Exceptions related to data processing in WhatsVector."""

from whatsvector.exceptions.base import WhatsVectorException


class InvalidRowError(WhatsVectorException):
    """Raised when a row in the data is invalid or malformed."""

    def __init__(self, row: str, reason: str) -> None:
        """
        Initialize the InvalidRowError.
        Args:
            row (str): The invalid row.
            reason (str): Description of why the row is invalid.
        """
        self.row = row
        super().__init__(f"Invalid row: {reason}")
