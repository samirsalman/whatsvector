"""CLI for chat with WhatsApp data."""

import asyncio

import typer
from agent.state import AgentState
from langchain.chat_models import init_chat_model
from langchain.messages import AIMessage, AIMessageChunk, HumanMessage
from qdrant_client import AsyncQdrantClient

from whatsvector.agent.agent import create_whatsvector_agent
from whatsvector.agent.context import WhatsVectorContext
from whatsvector.common.language import SupportedLanguages
from whatsvector.config.config_file import Config, ConfigFile

app = typer.Typer(
    add_completion=True,
)


async def invoke(agent, input_state: AgentState, context: WhatsVectorContext) -> None:
    """Process a chunk of AIMessageChunk and return its content."""
    ai_message = ""
    async for _, data in agent.astream(
        input=input_state, context=context, stream_mode=["messages"]
    ):
        chunk, _ = data
        if isinstance(chunk, AIMessageChunk):
            typer.echo(f"{chunk.content}", nl=False)
            ai_message += chunk.content
    return ai_message


@app.command("chat")
def run(
    profile: str = typer.Argument(
        ...,
        help="Profile name, used to save/load the configuration for chat runs.",
    ),
    username: str = typer.Option(
        None,
        "--username",
        "-u",
        help="The name of the user the chat is extracted from.",
    ),
    language: SupportedLanguages = typer.Option(
        "en",
        "--language",
        "-l",
        help="The language to use for the chat.",
    ),
    llm_model: str = typer.Option(
        "openai/gpt-4o-mini",
        "--llm-model",
        "-m",
        help="""
        The language model to use for the chat. The format is <provider>/<model-name>.
        Currently supported providers are 'openai' and 'groq'.
        """,
    ),
) -> None:
    """Run the WhatsVector chat agent."""
    config: Config = ConfigFile(f".whatsvector/{profile}.yaml").load()

    qdrant_client = AsyncQdrantClient(
        host=config.qdrant_host,
        port=config.qdrant_port,
        https=config.qdrant_https,
        api_key=config.qdrant_api_key,
        path=config.qdrant_local_path,
    )
    qdrant_client.set_model(embedding_model_name=config.embedding_model)

    splitted = llm_model.split("/")
    provider = splitted[0]
    model_name = "/".join(splitted[1:])
    chat_model = init_chat_model(model=model_name, model_provider=provider)

    context = WhatsVectorContext(
        qdrant_client=qdrant_client, collection_name=config.collection_name
    )
    agent = create_whatsvector_agent(
        language=language,
        llm=chat_model,
        username=username,
    )

    history = []

    typer.echo("Welcome to WhatsVector chat! Type 'exit' to quit.")
    while True:
        user_input = typer.prompt("You")
        if user_input.lower() in ["exit", "quit"]:
            typer.echo("Goodbye!")
            break
        history.append(HumanMessage(content=user_input))
        input_state = AgentState(
            messages=history,
            language=language,
            username=username,
        )
        typer.echo("WhatsVector Agent: ", nl=False)
        ai_message = asyncio.run(invoke(agent, input_state, context))
        typer.echo("")  # New line after the AI message
        history.append(AIMessage(content=ai_message))


if __name__ == "__main__":
    app()  # pragma: no cover
