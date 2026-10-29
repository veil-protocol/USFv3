---
name: decompose
description: Break complex goals into actionable subtasks. Use for multi-step operations requiring planning.
argument-hint: <complex-goal>
---

# Goal Decomposition

Decompose goal: $ARGUMENTS

## Execution

1. **Analyze goal complexity**
```
mcp__omega-nexus__omega_vault_query(
    query="$ARGUMENTS methodology steps phases",
    context="security",
    limit=10
)
```

2. **Identify dependencies**
- What must complete before what?
- Parallel vs sequential tasks
- Resource requirements

3. **Create execution DAG**
- Root: Original goal
- Nodes: Subtasks
- Edges: Dependencies

## Output Format

```
Goal: $ARGUMENTS
├── Phase 1: [subtask]
│   ├── Step 1.1: [action]
│   └── Step 1.2: [action]
├── Phase 2: [subtask] (depends on Phase 1)
└── Phase 3: [subtask] (parallel with Phase 2)
```

## Output

Hierarchical task breakdown with dependencies and execution order.
