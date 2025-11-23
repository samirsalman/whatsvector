"""Configuration file handling for WhatsVector application."""

from pathlib import Path

import yaml
from pydantic import BaseModel

from whatsvector.data.loaders.loader import (
    DEFAULT_COLLECTION_NAME,
    DEFAULT_EMBEDDING_MODEL,
)


class Config(BaseModel):
    """
    Configuration model for WhatsVector application.
    Attributes:
        qdrant_host (str): The Qdrant host address.
        qdrant_port (int): The Qdrant port number.
        qdrant_api_key (str): The Qdrant API key.
        embedding_model (str): The embedding model to use.
        collection_name (str): The name of the Qdrant collection.
    """

    qdrant_host: str | None = None
    qdrant_port: int | None = 6333
    qdrant_api_key: str | None = None
    qdrant_https: bool = False
    qdrant_local_path: str | None = None
    embedding_model: str = DEFAULT_EMBEDDING_MODEL
    collection_name: str = DEFAULT_COLLECTION_NAME


class ConfigFile:
    """Handles loading and saving configuration to a YAML file."""

    def __init__(self, file_path: str = ".whatsvector/default.yaml") -> None:
        self.file_path = file_path

    @staticmethod
    def exists(profile: str) -> bool:
        """
        Check if the configuration file exists.
        Args:
            profile (str): Profile name.
        Returns:
            bool: True if the configuration file exists, False otherwise.
        """
        config_path = Path(f".whatsvector/{profile}.yaml")
        return config_path.exists()

    def load(self) -> Config:
        """
        Load configuration from a YAML file.
        Returns:
            Config: The loaded configuration object.
        """

        if not Path(self.file_path).exists():
            raise FileNotFoundError(f"Config file {self.file_path} not found.")

        with open(self.file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        return Config(**data)

    def save(self, config: Config) -> None:
        """
        Save configuration to a YAML file.
        Args:
            config (Config): The configuration object to save.
        """
        Path(self.file_path).parent.mkdir(parents=True, exist_ok=True)

        with open(self.file_path, "w", encoding="utf-8") as f:
            yaml.dump(config.model_dump(), f)
