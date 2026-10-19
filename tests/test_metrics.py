from sift.evals.metrics import citation_presence, keyword_recall, unsupported_citation_rate


def test_keyword_recall():
    assert keyword_recall("RAG uses retrieval and external knowledge", ["retrieval", "knowledge"]) == 1.0


def test_citation_metrics():
    answer = "A claim [rag:1] and another [fake:2]."
    assert citation_presence(answer) == 1.0
    assert unsupported_citation_rate(answer, ["rag"]) == 0.5
