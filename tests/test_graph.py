from sift.graph import run_sift


def test_offline_graph_returns_cited_report(monkeypatch):
    monkeypatch.setenv("SIFT_MODE", "offline")
    result = run_sift("When is RAG useful?")
    assert result["report"]
    assert "[" in result["report"]
    assert result["verified_claims"]
