"""Main CLI entry point for WhatsVector."""

import typer

try:
    from cli.chat import app as chat_app
    from cli.load import app as load_app
except ImportError:
    # When installed as a package, use absolute imports
    import sys
    from pathlib import Path

    # Add the parent directory to the path
    cli_dir = Path(__file__).parent
    sys.path.insert(0, str(cli_dir))

    from chat import app as chat_app
    from load import app as load_app

app = typer.Typer(
    name="whatsvector",
    help="Vectorize your WhatsApp conversations and chat with them.",
    add_completion=True,
)

# Add subcommands
app.add_typer(chat_app, name="chat", help="Chat with your WhatsApp data.")
app.add_typer(load_app, name="load", help="Load WhatsApp data into Qdrant.")


def main():
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
