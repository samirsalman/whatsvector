"""CLI for loading WhatsApp data into Qdrant."""

import asyncio

import typer

from whatsvector.config.config_file import Config, ConfigFile
from whatsvector.data.loaders.loader import DEFAULT_EMBEDDING_MODEL, QdrantDataLoader

app = typer.Typer(
    add_completion=True,
)


@app.command("load")
def run(
    profile: str = typer.Argument(
        ...,
        help="Profile name, used to save/load the configuration for chat runs.",
    ),
    whatsapp_files: list[str] = typer.Argument(
        ...,
        help="List of WhatsApp data file paths.",
    ),
    qdrant_host: str = typer.Option(
        None,
        "--qdrant-host",
        "-h",
        help="The Qdrant host address.",
    ),
    qdrant_port: int = typer.Option(
        6333,
        "--qdrant-port",
        "-p",
        help="The Qdrant port number.",
    ),
    qdrant_api_key: str = typer.Option(
        None,
        "--qdrant-api-key",
        "-a",
        help="The Qdrant API key, if required.",
    ),
    qdrant_https: bool = typer.Option(
        False,
        "--qdrant-https/--no-qdrant-https",
        help="Whether to use HTTPS for Qdrant connection.",
    ),
    qdrant_local_path: str = typer.Option(
        None,
        "--local-path",
        "-l",
        help="Local path for Qdrant, if provided a local instance will be used.",
    ),
    embedding_model: str = typer.Option(
        DEFAULT_EMBEDDING_MODEL,
        "--embedding-model",
        "-e",
        help="The embedding model to use.",
    ),
    progress: bool = typer.Option(
        True,
        "--progress/--no-progress",
        help="Whether to show a progress bar during data loading.",
    ),
):
    """
    Run the Qdrant data loader to load WhatsApp data into Qdrant.
    Args:
        profile (str): Profile name, used to save/load the configuration for chat runs.
        whatsapp_files (list[str]): List of WhatsApp data file paths.
        qdrant_host (str): The Qdrant host address.
        qdrant_port (int): The Qdrant port number.
        qdrant_api_key (str): The Qdrant API key, if required.
        qdrant_https (bool): Whether to use HTTPS for Qdrant connection.
        qdrant_local_path (str): Local path for Qdrant, if provided a
            local instance will be used.
        embedding_model (str): The embedding model to use.
        progress (bool): Whether to show a progress bar during data loading.
    """
    if ConfigFile.exists(profile):
        config = ConfigFile(f".whatsvector/{profile}.yaml").load()
        qdrant_host = config.qdrant_host
        qdrant_port = config.qdrant_port
        qdrant_api_key = config.qdrant_api_key
        qdrant_https = config.qdrant_https
        qdrant_local_path = config.qdrant_local_path
        embedding_model = config.embedding_model

    loader = QdrantDataLoader(
        whatsapp_files,
        local_path=qdrant_local_path,
        host=qdrant_host,
        port=qdrant_port,
        https=qdrant_https,
        api_key=qdrant_api_key,
        embedding_model=embedding_model,
    )
    asyncio.run(loader.load_data(progress=progress))

    if not ConfigFile.exists(profile):
        config = ConfigFile(f".whatsvector/{profile}.yaml")
        config.save(
            config=Config(
                qdrant_host=qdrant_host,
                qdrant_port=qdrant_port,
                qdrant_api_key=qdrant_api_key,
                qdrant_https=qdrant_https,
                qdrant_local_path=qdrant_local_path,
                embedding_model=embedding_model,
            )
        )


if __name__ == "__main__":
    app()  # pragma: no cover
