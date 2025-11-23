from langchain.agents import create_agent
from langchain.chat_models import BaseChatModel

from whatsvector.agent.context import WhatsVectorContext
from whatsvector.agent.state import AgentState
from whatsvector.agent.tools import qdrant_search
from whatsvector.common.language import SupportedLanguages, language_code_to_name


def build_system_prompt(
    custom_system_prompt: str | None, username: str, language: SupportedLanguages
) -> str:
    """
    Builds the system prompt for the agent.
    Args:
        custom_system_prompt (str | None): Custom system prompt provided by the user.
        username (str): The username of the user.
        language (SupportedLanguages): The preferred language of the user.
    Returns:
        str: The final system prompt.
    """

    _prompt_instance = ""
    if username:
        _prompt_instance += f" The user's name is {username}."
    if language:
        _prompt_instance += (
            f" The user prefers to communicate in {language_code_to_name(language)}."
        )
    if custom_system_prompt:
        system_prompt = custom_system_prompt + _prompt_instance
    else:
        system_prompt = (
            "# Personality and Role"
            "You are a helpful assistant that provides information based on WhatsApp chat data."
            "You have access to a vector database containing WhatsApp messages, "
            "and you can use this data to answer user queries."
            "In the database each message has metadata including the sender's "
            "name and the date the message was sent."
            " Always refer to the messages in the database to provide accurate and "
            "relevant answers to the user's questions."
            "Use filters when necessary to narrow down search results based "
            "on the sender's name or date ranges."
            "If you cannot find the answer in the database, "
            "respond with 'I could not find any relevant information in your WhatsApp data,'"
            "and ask the user if they would like to provide more context or "
            "rephrase their question."
            " Do not apply filters unless explicitly instructed by the user."
            "## Output format"
            " When providing answers, always include a 'Sources' "
            "section at the end of your response."
            " Answer in a conversational and coincise manner."
            " Do not provide all the retrieved messages, instead synthesize "
            "the information to directly address the user's query."
            " The 'Sources' section should list the messages you referenced "
            "to formulate your answer." + _prompt_instance
        )
    return system_prompt


def create_whatsvector_agent(
    llm: BaseChatModel,
    custom_system_prompt: str | None = None,
    username: str = None,
    language: SupportedLanguages = "en",
):
    """
    Creates a WhatsVector agent with the specified configuration.
    Args:
        llm (BaseChatModel): The language model to use for the agent.
        custom_system_prompt (str | None): Custom system prompt for the agent.
        username (str): The username of the user.
        language (SupportedLanguages): The preferred language of the user.
    Returns:
        An instance of the WhatsVector agent.
    """
    system_prompt = build_system_prompt(custom_system_prompt, username, language)
    agent = create_agent(
        model=llm,
        context_schema=WhatsVectorContext,
        name="WhatsVector Agent",
        state_schema=AgentState,
        tools=[qdrant_search],
        system_prompt=system_prompt,
    )
    return agent
