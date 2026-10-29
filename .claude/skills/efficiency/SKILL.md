---
name: efficiency
description: Optimize token usage and context loading. Use when working with large datasets or long sessions.
argument-hint: <operation>
---

# Token Efficiency

Optimize: $ARGUMENTS

## Strategies

1. **Context Tiering**
- Tier 1: Critical (always loaded)
- Tier 2: Active (load on demand)
- Tier 3: Archive (summarized)

2. **Deduplication**
- Hash-based content dedup
- Reference previous results
- Compress verbose outputs

3. **Lazy Loading**
- Load summaries first
- Expand details on request
- Prune stale context

## Execution

For vault queries, use targeted searches:
```
mcp__omega-nexus__omega_vault_query(
    query="$ARGUMENTS",
    limit=5,  # Start small
    search_type="semantic"
)
```

## Output

Efficiency recommendations and optimized query patterns.
