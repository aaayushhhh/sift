from dataclasses import dataclass
from pathlib import Path
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from langchain_core.documents import Document
from ..config import settings
from ..schemas import Evidence


@dataclass
class IndexedChunk:
    source_id: str
    title: str
    text: str


class LocalResearchStore:
    """Small local retriever for the demo corpus. Easy to inspect and deterministic in tests."""

    def __init__(self, knowledge_dir: Path | None = None):
        self.knowledge_dir = knowledge_dir or settings.knowledge_dir
        self.chunks = self._load()
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.matrix = self.vectorizer.fit_transform([chunk.text for chunk in self.chunks])

    def _load(self) -> list[IndexedChunk]:
        chunks: list[IndexedChunk] = []
        for path in sorted(self.knowledge_dir.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            title = text.splitlines()[0].lstrip("# ").strip() or path.stem
            paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
            for i, paragraph in enumerate(paragraphs):
                chunks.append(IndexedChunk(f"{path.stem}:{i}", title, paragraph))
        if not chunks:
            raise RuntimeError(f"No knowledge documents found in {self.knowledge_dir}")
        return chunks

    def search(self, query: str, k: int | None = None) -> list[Evidence]:
        k = k or settings.top_k
        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.matrix)[0]
        ranked = scores.argsort()[::-1][:k]
        return [
            Evidence(
                source_id=self.chunks[i].source_id,
                title=self.chunks[i].title,
                excerpt=self.chunks[i].text,
                score=float(scores[i]),
            )
            for i in ranked
            if scores[i] > 0
        ]

    def as_documents(self) -> list[Document]:
        return [Document(page_content=c.text, metadata={"source_id": c.source_id, "title": c.title}) for c in self.chunks]
