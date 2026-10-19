import re
from ..agents.verifier import citation_ids


def keyword_recall(answer: str, expected_keywords: list[str]) -> float:
    if not expected_keywords:
        return 1.0
    text = answer.lower()
    hits = sum(1 for keyword in expected_keywords if keyword.lower() in text)
    return hits / len(expected_keywords)


def citation_presence(answer: str) -> float:
    return 1.0 if citation_ids(answer) else 0.0


def unsupported_citation_rate(answer: str, allowed_source_prefixes: list[str]) -> float:
    ids = citation_ids(answer)
    if not ids:
        return 0.0
    invalid = [sid for sid in ids if not any(sid.startswith(prefix) for prefix in allowed_source_prefixes)]
    return len(invalid) / len(ids)


def word_count(answer: str) -> int:
    return len(re.findall(r"\b\w+\b", answer))
