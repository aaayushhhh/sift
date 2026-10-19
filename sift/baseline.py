from langchain_core.prompts import ChatPromptTemplate
from .llm import get_llm
from .rag import LocalResearchStore


def run_baseline(question: str) -> str:
    store = LocalResearchStore()
    evidence = store.search(question, k=5)
    if not evidence:
        return "I could not find relevant evidence in the local corpus."
    llm = get_llm()
    context = "\n\n".join(f"[{e.source_id}] {e.excerpt}" for e in evidence)
    if llm is None:
        return evidence[0].excerpt + f" [{evidence[0].source_id}]"
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer the question from the supplied context. Cite source ids inline."),
        ("human", "Question: {question}\n\nContext:\n{context}"),
    ])
    return (prompt | llm).invoke({"question": question, "context": context}).content
