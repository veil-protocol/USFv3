---
name: verified
description: Execute with multi-chain verification. Use for high-stakes operations requiring consensus.
argument-hint: <operation>
---

# Verified Execution

Execute with verification: $ARGUMENTS

## Execution

1. **Primary execution**
- Execute the requested operation
- Capture output and results

2. **Verification chain**
```
mcp__omega-nexus__omega_vault_query(
    query="$ARGUMENTS verification validation",
    context="security",
    limit=10
)
```

3. **Cross-reference**
- Compare against known-good patterns
- Validate output format
- Check for anomalies

4. **Consensus**
- Require agreement across checks
- Flag discrepancies
- Report confidence level

## Output

Verified results with confidence score and validation details.
