from langchain_core.prompts import ChatPromptTemplate
from ..llm import get_llm
from ..rag import LocalResearchStore
from ..tools import search_knowledge
from ..schemas import Evidence, Finding, ResearchTask


def investigate(task: ResearchTask, store: LocalResearchStore) -> tuple[Finding, list[Evidence]]:
    raw = search_knowledge.invoke({"query": task.question, "k": 4})
    evidence = [Evidence.model_validate(item) for item in raw]
    llm = get_llm()
    if not evidence:
        return Finding(task_id=task.id, role=task.role, claim="No relevant evidence found."), []

    if llm is None:
        excerpt = evidence[0].excerpt.replace("\n", " ")
        claim = excerpt[:360].rstrip()
        return Finding(task_id=task.id, role=task.role, claim=claim, evidence_ids=[e.source_id for e in evidence[:2]]), evidence

    context = "\n\n".join(f"[{e.source_id}] {e.excerpt}" for e in evidence)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are one researcher in a larger workflow. Make one useful, cautious finding using only the supplied evidence. Cite source ids in the evidence_ids field."),
        ("human", "Task: {task}\n\nEvidence:\n{context}"),
    ])
    finding = (prompt | llm.with_structured_output(Finding)).invoke({"task": task.question, "context": context})
    finding.task_id = task.id
    finding.role = task.role
    return finding, evidence
