from langchain_core.prompts import ChatPromptTemplate
from ..llm import get_llm
from ..schemas import ResearchTask


def plan_question(question: str) -> list[ResearchTask]:
    llm = get_llm()
    if llm is None:
        return [
            ResearchTask(id="r1", role="research", question=f"What evidence directly answers: {question}"),
            ResearchTask(id="r2", role="technical", question=f"What technical details or mechanisms matter for: {question}"),
            ResearchTask(id="r3", role="counterpoint", question=f"What limitations or counterarguments should qualify the answer to: {question}"),
        ]

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Break a research question into exactly three focused tasks: general evidence, technical detail, and counterpoint. Return structured output."),
        ("human", "{question}"),
    ])
    class PlanOutput(__import__("pydantic").BaseModel):
        tasks: list[ResearchTask]
    result = (prompt | llm.with_structured_output(PlanOutput)).invoke({"question": question})
    return result.tasks
