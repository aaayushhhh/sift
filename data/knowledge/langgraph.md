# Graph-based orchestration

Graph-based orchestration represents an agent workflow as explicit nodes, shared state, and transitions. Conditional routing can choose which work happens next while parallel branches can handle independent tasks.

Explicit workflow state is useful for debugging because intermediate plans, findings, evidence, and verification results can be inspected. It also makes termination behavior clearer than an open-ended loop of autonomous agents.

Subgraphs are useful when a specialist workflow has its own internal steps but should appear as one component in a larger graph. They can help keep a growing agent system modular.
