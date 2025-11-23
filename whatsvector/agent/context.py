from dataclasses import dataclass

try:
    from qdrant_client import AsyncQdrantClient
except ImportError as e:
    raise ImportError(
        "qdrant-client is not installed. Please install it with `pip install qdrant-client`."
    ) from e


@dataclass
class WhatsVectorContext:
    """
    Context for WhatsVector agent including Qdrant client and collection name.
    Attributes:
        qdrant_client (AsyncQdrantClient): The Qdrant client instance.
        collection_name (str): The name of the Qdrant collection to search.
    """

    qdrant_client: AsyncQdrantClient
    collection_name: str = "whatsvector_collection"
