import re
from langchain_core.prompts import ChatPromptTemplate
from ..llm import get_llm
from ..schemas import Evidence, Finding, VerifiedClaim


def verify(findings: list[Finding], evidence: list[Evidence]) -> list[VerifiedClaim]:
    by_id = {e.source_id: e for e in evidence}
    llm = get_llm()
    if llm is None:
        verified = []
        for finding in findings:
            valid_ids = [sid for sid in finding.evidence_ids if sid in by_id]
            status = "supported" if valid_ids else "unsupported"
            verified.append(VerifiedClaim(claim=finding.claim, evidence_ids=valid_ids, status=status))
        return verified

    verified = []
    for finding in findings:
        context = "\n\n".join(f"[{sid}] {by_id[sid].excerpt}" for sid in finding.evidence_ids if sid in by_id)
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Check whether the claim is supported by the supplied evidence. Be conservative. 'supported' means the evidence directly supports it, 'weak' means partial support, and 'unsupported' means it is not established. Return structured output."),
            ("human", "Claim: {claim}\n\nEvidence:\n{context}"),
        ])
        item = (prompt | llm.with_structured_output(VerifiedClaim)).invoke({"claim": finding.claim, "context": context})
        item.claim = finding.claim
        item.evidence_ids = [sid for sid in item.evidence_ids if sid in by_id]
        verified.append(item)
    return verified


def citation_ids(text: str) -> set[str]:
    return set(re.findall(r"\[([^\]]+:\d+)\]", text))
