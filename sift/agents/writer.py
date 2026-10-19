from langchain_core.prompts import ChatPromptTemplate
from ..llm import get_llm
from ..schemas import Evidence, VerifiedClaim


def write_report(question: str, claims: list[VerifiedClaim], evidence: list[Evidence]) -> str:
    usable = [c for c in claims if c.status != "unsupported"]
    by_id = {e.source_id: e for e in evidence}
    llm = get_llm()

    if llm is None:
        lines = [f"# Research note\n\n**Question:** {question}\n", "## Findings"]
        for claim in usable:
            refs = " ".join(f"[{sid}]" for sid in claim.evidence_ids)
            lines.append(f"- {claim.claim} {refs}".strip())
        lines.append("\n## Sources")
        used = {sid for c in usable for sid in c.evidence_ids}
        for sid in sorted(used):
            if sid in by_id:
                lines.append(f"- [{sid}] {by_id[sid].title}")
        return "\n".join(lines)

    claim_text = "\n".join(
        f"- {c.claim} | status={c.status} | evidence={','.join(c.evidence_ids)}" for c in usable
    )
    evidence_text = "\n\n".join(f"[{e.source_id}] {e.title}\n{e.excerpt}" for e in evidence)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Write a concise research report. Use only verified claims and supplied evidence. Cite factual claims inline with source ids exactly like [source:0]. Include a short limitations section. Do not cite unsupported claims."),
        ("human", "Question: {question}\n\nVerified claims:\n{claims}\n\nEvidence:\n{evidence}"),
    ])
    return (prompt | llm).invoke({"question": question, "claims": claim_text, "evidence": evidence_text}).content
