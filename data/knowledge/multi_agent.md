# Multi-agent research workflows

A multi-agent workflow divides a larger task into narrower responsibilities. Research systems can separate planning, evidence gathering, technical analysis, counterargument search, verification, and writing.

Parallel work is most useful when tasks are independent. Running independent research branches concurrently can reduce wall-clock time compared with executing each branch sequentially, although total model usage may still increase.

More agents do not automatically improve a system. Additional handoffs create more places for context loss, inconsistent assumptions, latency, and cost. Explicit state and constrained transitions make the workflow easier to inspect than unrestricted agent-to-agent conversation.
