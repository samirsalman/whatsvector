"""
This module contains the base exception class for WhatsVector.
"""


class WhatsVectorException(Exception):
    """
    Base exception for WhatsVector errors.

    Attributes:
        reason (str): Description of the error.
    """

    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(self.reason)
