---
name: verify
description: Multi-chain verification with consensus. Use when user wants to verify a claim, validate information, or get high-confidence answers.
argument-hint: <claim-to-verify>
---

# Multi-Chain Verification

Verify claim: $ARGUMENTS

## Execution

```
mcp__omega-nexus__omega_verify(
    claim="$ARGUMENTS",
    chain_count=3,
    early_exit_threshold=0.85
)
```

For maximum precision (PL5):
```
mcp__omega-nexus__omega_verify(
    claim="$ARGUMENTS",
    chain_count=5,
    early_exit_threshold=0.95
)
```

Then aggregate:
```
mcp__omega-nexus__omega_aggregate(
    outputs=<chain_results>,
    method="majority_vote"
)
```

## Output

Report:
- Each chain's verdict and confidence
- Aggregated consensus
- Any dissenting views
