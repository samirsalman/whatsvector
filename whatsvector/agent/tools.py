from typing import Optional

from langchain.tools import ToolRuntime, tool

from whatsvector.agent.context import WhatsVectorContext


@tool
async def qdrant_search(
    runtime: ToolRuntime[WhatsVectorContext],
    query: str,
    top_k: int = 5,
    filter_by_username: Optional[str] = None,
    before_date: Optional[str] = None,
    after_date: Optional[str] = None,
) -> list[dict]:
    """Searches a Qdrant collection for the most relevant documents to the query.

    Args:
        runtime (ToolRuntime[WhatsVectorContext]): The tool runtime with context.
        query (str): The search query.
        top_k (int, optional): The number of top results to return. Defaults to 5.
        filter_by_username (Optional[str], optional): Filter results by username. Defaults to None.
        before_date (Optional[str], optional): Filter results created before this date (ISO format).
        after_date (Optional[str], optional): Filter results created after this date (ISO format).

    Returns:
        list[dict]: A list of the most relevant documents as dictionaries.
    """
    import qdrant_client.models as models

    # Build the filter conditions
    must_conditions = []
    if filter_by_username:
        must_conditions.append(
            models.FieldCondition(
                key="sender",
                match=models.MatchValue(value=filter_by_username),
            )
        )
    if before_date:
        must_conditions.append(
            models.FieldCondition(
                key="when",
                range=models.Range(lt=before_date),
            )
        )
    if after_date:
        must_conditions.append(
            models.FieldCondition(
                key="when",
                range=models.Range(gt=after_date),
            )
        )

    query_filter = models.Filter(must=must_conditions) if must_conditions else None

    # Perform the search
    search_result = await runtime.context.qdrant_client.query_points(
        collection_name=runtime.context.collection_name,
        query=models.Document(
            text=query,
            model=runtime.context.qdrant_client.embedding_model_name,
        ),
        limit=top_k,
        query_filter=query_filter,
    )
    return [
        {
            "id": point.id,
            "sender": point.payload.get("sender"),
            "when": point.payload.get("when"),
            "content": point.payload.get("content"),
        }
        for point in search_result.points
    ]
