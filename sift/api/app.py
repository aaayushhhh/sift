from fastapi import FastAPI
from pydantic import BaseModel
from ..graph import run_sift

app = FastAPI(title="Sift", version="0.1.0")


class ResearchRequest(BaseModel):
    question: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/research")
def research(request: ResearchRequest):
    result = run_sift(request.question)
    return {
        "question": request.question,
        "report": result["report"],
        "verified_claims": result.get("verified_claims", []),
    }
