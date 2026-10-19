"""Optional LangSmith experiment runner.

Create a dataset in LangSmith with `question` inputs, then point DATASET_NAME at it.
The local evaluator stays deliberately simple so experiment results are easy to inspect.
"""
import os
from langsmith import evaluate
from ..graph import run_sift


def target(inputs: dict) -> dict:
    result = run_sift(inputs["question"])
    return {"answer": result["report"]}


def has_citation(outputs: dict, reference_outputs: dict | None = None) -> bool:
    return "[" in outputs["answer"] and "]" in outputs["answer"]


def main():
    dataset = os.environ["DATASET_NAME"]
    evaluate(target, data=dataset, evaluators=[has_citation], experiment_prefix="sift")


if __name__ == "__main__":
    main()
