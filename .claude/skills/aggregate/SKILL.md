---
name: aggregate
description: Combine outputs from multiple agents or searches into unified results. Use after parallel operations.
argument-hint: <result-type>
---

# Result Aggregation

Aggregate and synthesize: $ARGUMENTS

## Execution

1. **Collect parallel results**
```
# Gather outputs from multiple vault queries or agent runs
results = [query1_output, query2_output, query3_output]
```

2. **Cross-reference findings**
```
mcp__omega-nexus__omega_vault_query(
    query="$ARGUMENTS synthesis correlation",
    context="security",
    limit=15
)
```

3. **Deduplicate and rank**
- Remove duplicate findings
- Rank by relevance/severity
- Highlight consensus points

## Output

Synthesized report with ranked findings and confidence levels.
