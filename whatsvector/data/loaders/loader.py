"""Data loader classes."""

import logging
from abc import ABC, abstractmethod

from tqdm import tqdm

from whatsvector.exceptions.data import InvalidRowError
from whatsvector.types.data import WhatsappData

# The default embedding model is jinaai/jina-embeddings-v3 because it's good for multilingual data.
DEFAULT_EMBEDDING_MODEL = "jinaai/jina-embeddings-v3"
DEFAULT_COLLECTION_NAME = "whatsvector_collection"


class DataLoader(ABC):
    """Abstract base class for data loaders."""

    def __init__(
        self, wa_files: list[str], *args, raise_errors: bool = False, **kwargs
    ) -> None:
        """
        Abstract base class for data loaders.
        Args:
            wa_files (list[str]): List of WhatsApp data file paths.
            raise_errors (bool): Whether to raise errors during loading.
        """
        self.wa_files = wa_files
        self.raise_errors = raise_errors

    @abstractmethod
    async def _load(self, wa_data: WhatsappData) -> None:
        """
        Abstract method to load data.
        Specific implementations should override this method.
        For example, qdrant loader will implement its own logic here,
            or in-memory loader will implement its own logic.
        Args:
            wa_data (WhatsappData): The WhatsApp data to load.
        """
        ...

    async def load_data(
        self,
        progress: bool = False,
    ) -> None:
        """
        Load data using the specific implementation.
        Args:
            progress (bool): Whether to show a progress bar during loading.
        Raises:
            InvalidRowError: If a row in the data is invalid and raise_errors is True.
        """
        iterator = self.wa_files
        if progress:
            iterator = tqdm(
                self.wa_files,
                desc="Loading WhatsApp data files",
                unit="file",
                total=len(self.wa_files),
            )
        for wa_file in iterator:
            try:
                data = WhatsappData.from_txt_file(wa_file)
                await self._load(data)
            except InvalidRowError as e:
                if self.raise_errors:
                    raise e
                else:
                    continue


class InMemoryDataLoader(DataLoader):
    """In-memory data loader implementation."""

    def __init__(
        self, wa_files: list[str], *args, raise_errors: bool = False, **kwargs
    ) -> None:
        """
        In-memory data loader implementation.
        Args:
            wa_files (list[str]): List of WhatsApp data file paths.
            raise_errors (bool): Whether to raise errors during loading.
        """
        super().__init__(wa_files, raise_errors, *args, **kwargs)
        self.data_storage: list[WhatsappData] = []

    async def _load(self, wa_data: WhatsappData) -> None:
        """
        Load data into in-memory storage.
        Args:
            wa_data (WhatsappData): The WhatsApp data to load.
        """
        self.data_storage.append(wa_data)


class QdrantDataLoader(DataLoader):
    """Qdrant data loader implementation."""

    def __init__(
        self,
        wa_files: list[str],
        *args,
        raise_errors: bool = False,
        host: str = "localhost",
        port: int = 6333,
        https: bool = False,
        api_key: str | None = None,
        local_path: str | None = None,
        embedding_model: str = DEFAULT_EMBEDDING_MODEL,
        collection_name: str = DEFAULT_COLLECTION_NAME,
        **kwargs,
    ) -> None:
        """
        Qdrant data loader implementation.
        Args:
            wa_files (list[str]): List of WhatsApp data file paths.
            raise_errors (bool): Whether to raise errors during loading.
            host (str): Qdrant host.
            port (int): Qdrant port.
            https (bool): Whether to use HTTPS.
            api_key (str | None): Qdrant API key.
            local_path (str | None): Local path for Qdrant, if provided a local instance will be used.
            embedding_model (str): The embedding model to use.
            collection_name (str): The name of the Qdrant collection.
        """
        super().__init__(wa_files, raise_errors, *args, **kwargs)
        try:
            from qdrant_client import AsyncQdrantClient
        except ImportError as e:
            raise ImportError(
                "qdrant-client is not installed. Please install it with 'pip install qdrant-client'"
            ) from e
        self.collection_name = collection_name
        self.embedding_model = embedding_model
        if local_path is not None:
            logging.warning(
                "Local path provided, using local Qdrant instance. Host, port, https, and api_key parameters will be ignored."
            )
            host = None
            port = 6333
            https = False
            api_key = None

        self._client = AsyncQdrantClient(
            host=host,
            port=port,
            https=https,
            api_key=api_key,
            path=local_path,
        )

        self._client.set_model(embedding_model_name=embedding_model)

    async def _load(self, wa_data: WhatsappData) -> None:
        """
        Load data into Qdrant.
        Args:
            wa_data (WhatsappData): The WhatsApp data to load.
        """
        import qdrant_client.models as models

        if not await self._client.collection_exists(self.collection_name):
            logging.info(
                f"Collection {self.collection_name} does not exist. Creating a new collection."
            )
            await self._client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=self._client.get_embedding_size(model_name=self.embedding_model),
                    distance=models.Distance.COSINE,
                ),
            )

        metadata = [
            {
                "sender": msg.sender,
                "when": msg.message_date.strftime("%A, %d %B %Y"),
                "content": msg.content,
                "document": msg.rich_content,
            }
            for msg in wa_data.clean_messages
        ]

        await self._client.upload_collection(
            collection_name=self.collection_name,
            vectors=[
                models.Document(text=msg.rich_content, model=self.embedding_model)
                for msg in wa_data.clean_messages
            ],
            payload=metadata,
            wait=True,
        )
        logging.info(
            f"Loaded {len(wa_data.messages)} messages into collection {self.collection_name}."
        )
