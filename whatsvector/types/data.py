"""Module defining data types for WhatsApp data processing."""

import re
from datetime import datetime
from functools import cached_property
from typing import Literal

from pydantic import BaseModel, Field

from whatsvector.exceptions.data import InvalidRowError

KNOWN_NOT_FOUND_PLACEHOLDERS = {
    "it": {
        "immagine omessa",
        "video omesso",
        "audio omesso",
        "documento omesso",
    },
    "en": {"image omitted", "video omitted", "audio omitted", "document omitted"},
}


class WhatsappMessage(BaseModel):
    """
    Class representing a WhatsApp message.
    Attributes:
        timestamp (str): The timestamp of the message.
        sender (str): The sender of the message.
        content (str): The content of the message.
    """

    timestamp: str = Field(
        ..., description="The timestamp of the message in the format [DD/MM/YY, HH:MM:SS]"
    )
    sender: str = Field(..., description="The sender of the message")
    content: str = Field(..., description="The content of the message")

    @cached_property
    def message_date(self) -> datetime:
        """
        Get the date part of the timestamp.
        Returns:
            datetime: The date of the message.
        """
        date_str = getattr(self, "timestamp").split(",")[0].strip("[] ")
        return datetime.strptime(date_str, "%d/%m/%y")

    @property
    def rich_content(self) -> str:
        """
        Get the rich content of the message, combining sender, timestamp, and content.
        Returns:
            str: The rich content of the message.
        """

        # when must contains also the weekday name for better context in the vectorization
        date_str = self.message_date.strftime("%A, %d %B %Y")
        return f"Sender: {self.sender}\nWhen: {date_str}\nMessage: {self.content}" ""

    @classmethod
    def from_raw(cls, raw_message: str) -> "WhatsappMessage":
        """
        Create a WhatsappMessage instance from a raw message string.
        Args:
            raw_message (str): The raw message string.
        Returns:
            WhatsappMessage: The created WhatsappMessage instance.
        Raises:
            InvalidRowError: If the raw message does not match the expected format.
        """
        pattern = r"^\[(\d{2}/\d{2}/\d{2}), (\d{2}:\d{2}:\d{2})\] (.*?): (.*)$"
        match = re.match(pattern, raw_message)
        if not match:
            raise InvalidRowError(
                row=raw_message, reason="Message does not match expected format."
            )
        date, time, sender, content = match.groups()
        timestamp = f"{date}, {time}"
        return cls(timestamp=timestamp, sender=sender, content=content)


class WhatsappData:
    """Class representing WhatsApp data."""

    def __init__(
        self,
        messages: list[WhatsappMessage],
        app_language: Literal["en", "it"] = "en",
        not_found_placeholders: list[str] | None = None,
    ) -> None:
        """
        Initialize the WhatsappData.
        Args:
            messages (list[dict]): List of WhatsApp messages.
            app_language (Literal["en", "it"]): Language of the WhatsApp application,
                the not found placeholders depend on it.
            not_found_placeholders (list[str]): List of placeholders for omitted media.
        """
        self.messages = messages
        self.not_found_placeholders = (
            not_found_placeholders
            if not_found_placeholders is not None
            else KNOWN_NOT_FOUND_PLACEHOLDERS[app_language].copy()
        )

    @classmethod
    def from_txt_file(
        cls,
        file_path: str,
        app_language: Literal["en", "it"] = "en",
    ):
        """
        Create a WhatsappData instance from a text file.
        Args:
            file_path (str): Path to the WhatsApp chat export text file.
            app_language (Literal["en", "it"]): Language of the WhatsApp application.
        Returns:
            WhatsappData: The created WhatsappData instance.
        """
        not_found_placeholders = (
            [
                "immagine omessa",
                "video omesso",
                "audio omesso",
                "documento omesso",
            ]
            if app_language == "it"
            else [
                "image omitted",
                "video omitted",
                "audio omitted",
                "document omitted",
            ]
        )

        messages = []
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    try:
                        message = WhatsappMessage.from_raw(line)
                        messages.append(message)
                    except InvalidRowError:
                        continue  # Skip invalid rows
        return cls(
            messages=messages,
            app_language=app_language,
            not_found_placeholders=not_found_placeholders,
        )

    @property
    def clean_messages(self) -> list[WhatsappMessage]:
        """
        Get a list of messages excluding those with content in not_found_placeholders.
        Returns:
            list[WhatsappMessage]: A list of clean WhatsApp messages.
        """
        return [
            message
            for message in self.messages
            if message.content not in self.not_found_placeholders
        ]

    @property
    def senders(self) -> set[str]:
        """
        Get a set of unique senders from the messages.
        Returns:
            set[str]: A set of unique senders.
        """
        return set(message.sender for message in self.messages)

    @property
    def total_messages(self) -> int:
        """
        Get the total number of messages.
        Returns:
            int: The total number of messages.
        """
        return len(self.messages)

    @property
    def total_clean_messages(self) -> int:
        """
        Get the total number of clean messages.
        Returns:
            int: The total number of clean messages.
        """
        return len(self.clean_messages)

    def __iter__(self):
        return iter(self.messages)

    def __len__(self):
        return len(self.messages)

    def __getitem__(self, index: int) -> WhatsappMessage:
        return self.messages[index]

    def __repr__(self) -> str:
        return f"WhatsappData(total_messages={self.total_messages}, total_clean_messages={self.total_clean_messages})"
