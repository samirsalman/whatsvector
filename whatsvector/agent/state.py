"""Defines the state structure for the agent."""

from typing import Annotated, Optional, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

from whatsvector.common.language import SupportedLanguages


class AgentState(TypedDict):
    """
    Represents the state of the agent with input, output, messages, language, and username.

    Attributes:
        messages (list[AnyMessage]): A list of messages associated with the agent.
        language (SupportedLanguages): The preferred language of the agent.
        username (Optional[str]): The username associated with the agent, if any.
        collection_name (str): The name of the Qdrant collection to search.
    """

    messages: Annotated[list[AnyMessage], add_messages]
    language: SupportedLanguages
    username: Optional[str]
