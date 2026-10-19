# Evaluating retrieval and agent systems

Agent evaluation should separate end-to-end quality from component behavior. Useful checks include whether the right tool was called, whether retrieval returned relevant evidence, whether factual claims are supported by that evidence, and whether the final answer satisfies the task.

A baseline matters because a more complicated architecture can increase latency and cost without improving quality. A simple single-pass RAG answer is a useful comparison for a multi-agent research workflow.

Evaluation sets should include representative normal cases and difficult cases. Regression tests are useful after prompt, model, retrieval, or graph changes because they show whether an improvement on one case causes failures elsewhere.
