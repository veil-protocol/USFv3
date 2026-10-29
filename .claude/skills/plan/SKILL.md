---
name: plan
description: Decompose a goal into actionable tasks with dependencies. Use for planning complex multi-step tasks.
argument-hint: <goal>
---

# Goal Decomposition

Plan: $ARGUMENTS

## Execution

1. **Decompose goal**
```
mcp__omega-nexus__omega_decompose(
    goal="$ARGUMENTS",
    max_depth=3
)
```

2. **Validate plan**
```
mcp__omega-nexus__omega_triage(task="Execute plan: <summary>")
```

## Output

Report:
- Subtasks with dependencies
- Execution order
- Estimated complexity
- Recommended compute type (parallel/sequential/hivemind)
