# Evaluation

Sift includes two paths:

- `baseline`: one retrieval pass followed by one answer
- `sift`: planning, parallel research, verification, then writing

The local evaluation set lives in `data/evals/questions.json`. It currently measures:

- expected-keyword recall
- whether the answer includes source citations
- unsupported citation rate
- wall-clock latency

These are intentionally simple code evaluators. They are useful for regression tests and architecture comparisons, but they are not a substitute for human review.

Run both experiments:

```bash
python -m sift.evals.run --mode baseline --out results/baseline.json
python -m sift.evals.run --mode sift --out results/sift.json
```

Do not put performance numbers in the README until they come from an actual run with the configuration you intend to discuss.

## LangSmith

With tracing enabled, model calls made through LangChain can be inspected in LangSmith. `sift/evals/langsmith_eval.py` also contains a small experiment runner for a LangSmith dataset. The project keeps local evaluation available because it is useful in CI and does not require an external account.

A stronger second evaluation pass would add an LLM judge for claim groundedness and report completeness, then compare that score with the deterministic metrics above.
