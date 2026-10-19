from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from .agents.planner import plan_question
from .agents.researcher import investigate
from .agents.verifier import verify
from .agents.writer import write_report
from .rag import LocalResearchStore
from .schemas import SiftState, ResearchTask

_store: LocalResearchStore | None = None


def get_store() -> LocalResearchStore:
    global _store
    if _store is None:
        _store = LocalResearchStore()
    return _store


def planner_node(state: SiftState):
    return {"plan": plan_question(state["question"])}


def dispatch_research(state: SiftState):
    return [Send("researcher", {"task": task}) for task in state["plan"]]


def researcher_node(state: dict):
    task = state["task"]
    if isinstance(task, dict):
        task = ResearchTask.model_validate(task)
    finding, evidence = investigate(task, get_store())
    return {"findings": [finding], "evidence": evidence}


def verifier_node(state: SiftState):
    # Parallel branches can retrieve the same chunk, so collapse duplicates here.
    unique = {e.source_id: e for e in state.get("evidence", [])}
    claims = verify(state.get("findings", []), list(unique.values()))
    return {"verified_claims": claims, "evidence": []}


def writer_node(state: SiftState):
    unique = {e.source_id: e for e in state.get("evidence", [])}
    # verifier_node clears evidence because reducers append; recover from findings with a fresh search if needed.
    evidence = list(unique.values())
    if not evidence:
        store = get_store()
        seen = {}
        for task in state.get("plan", []):
            for item in store.search(task.question):
                seen[item.source_id] = item
        evidence = list(seen.values())
    report = write_report(state["question"], state.get("verified_claims", []), evidence)
    return {"report": report}


def build_graph():
    builder = StateGraph(SiftState)
    builder.add_node("planner", planner_node)
    builder.add_node("researcher", researcher_node)
    builder.add_node("verifier", verifier_node)
    builder.add_node("writer", writer_node)
    builder.add_edge(START, "planner")
    builder.add_conditional_edges("planner", dispatch_research, ["researcher"])
    builder.add_edge("researcher", "verifier")
    builder.add_edge("verifier", "writer")
    builder.add_edge("writer", END)
    return builder.compile()


graph = build_graph()


def run_sift(question: str) -> dict:
    return graph.invoke({"question": question, "findings": [], "evidence": []})
