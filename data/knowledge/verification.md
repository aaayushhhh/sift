# Claim and evidence verification

A generated statement should not be treated as supported merely because a retrieved document exists. Verification should compare the specific claim with the specific evidence used to justify it.

Separating generation from verification reduces the risk of asking the same reasoning step to both propose and approve its own conclusion. The verifier can mark a claim as supported, weakly supported, or unsupported and prevent unsupported claims from reaching the final report.

Verification adds another model call or deterministic check, so it increases latency and sometimes cost. The tradeoff is useful when traceability and groundedness matter more than minimum response time.
