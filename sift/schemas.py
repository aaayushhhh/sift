from typing import Annotated, Literal
from operator import add
from pydantic import BaseModel, Field
from typing_extensions import TypedDict


class ResearchTask(BaseModel):
    id: str
    question: str
    role: Literal["research", "technical", "counterpoint"]


class Evidence(BaseModel):
    source_id: str
    title: str
    excerpt: str
    score: float = 0.0


class Finding(BaseModel):
    task_id: str
    role: str
    claim: str
    evidence_ids: list[str] = Field(default_factory=list)


class VerifiedClaim(BaseModel):
    claim: str
    evidence_ids: list[str]
    status: Literal["supported", "weak", "unsupported"]
    note: str = ""


class SiftState(TypedDict, total=False):
    question: str
    plan: list[ResearchTask]
    findings: Annotated[list[Finding], add]
    evidence: Annotated[list[Evidence], add]
    synthesis: str
    verified_claims: list[VerifiedClaim]
    report: str
