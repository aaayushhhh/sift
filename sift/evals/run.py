import argparse
import json
import time
from pathlib import Path
from statistics import mean
from ..baseline import run_baseline
from ..graph import run_sift
from .metrics import citation_presence, keyword_recall, unsupported_citation_rate, word_count


def load_cases(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate(mode: str, cases: list[dict]):
    rows = []
    for case in cases:
        start = time.perf_counter()
        if mode == "baseline":
            answer = run_baseline(case["question"])
        else:
            answer = run_sift(case["question"])["report"]
        latency = time.perf_counter() - start
        rows.append({
            "id": case["id"],
            "keyword_recall": keyword_recall(answer, case["expected_keywords"]),
            "citation_presence": citation_presence(answer),
            "unsupported_citation_rate": unsupported_citation_rate(answer, case["allowed_source_prefixes"]),
            "latency_seconds": round(latency, 4),
            "word_count": word_count(answer),
            "answer": answer,
        })
    return {
        "mode": mode,
        "summary": {
            "keyword_recall": mean(r["keyword_recall"] for r in rows),
            "citation_presence": mean(r["citation_presence"] for r in rows),
            "unsupported_citation_rate": mean(r["unsupported_citation_rate"] for r in rows),
            "latency_seconds": mean(r["latency_seconds"] for r in rows),
        },
        "cases": rows,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["baseline", "sift"], default="sift")
    parser.add_argument("--dataset", default="data/evals/questions.json")
    parser.add_argument("--out")
    args = parser.parse_args()
    result = evaluate(args.mode, load_cases(Path(args.dataset)))
    text = json.dumps(result, indent=2)
    print(text)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
