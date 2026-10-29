---
name: research
description: Deep multi-source research with verification. Use for thorough research on any topic.
argument-hint: <topic>
---

# Deep Research

Research: $ARGUMENTS

## Execution

1. **Primary search**
```
mcp__omega-nexus__omega_vault_query(
    query="$ARGUMENTS",
    context="security",
    limit=25,
    search_type="semantic"
)
```

2. **Keyword search**
```
mcp__omega-nexus__omega_vault_query(
    query="$ARGUMENTS",
    search_type="fulltext",
    limit=15
)
```

3. **Verify findings**
```
mcp__omega-nexus__omega_verify(
    claim="Research findings on $ARGUMENTS",
    chain_count=3
)
```

4. **Aggregate results**
```
mcp__omega-nexus__omega_aggregate(
    outputs=[primary, keyword, related],
    method="weighted_combination"
)
```

## Output

Comprehensive research report with verified findings.
