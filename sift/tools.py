from langchain_core.tools import tool
from .rag import LocalResearchStore

_store: LocalResearchStore | None = None


def _store_instance() -> LocalResearchStore:
    global _store
    if _store is None:
        _store = LocalResearchStore()
    return _store


@tool
def search_knowledge(query: str, k: int = 4) -> list[dict]:
    """Search the research corpus for evidence relevant to a question."""
    return [item.model_dump() for item in _store_instance().search(query, k=k)]
