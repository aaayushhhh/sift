from sift.rag import LocalResearchStore


def test_retrieval_finds_rag_document():
    store = LocalResearchStore()
    results = store.search("keeping knowledge current with retrieval")
    assert results
    assert any(item.source_id.startswith("rag:") for item in results)
