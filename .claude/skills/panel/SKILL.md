---
name: panel
description: Create an expert panel using USF archetypes to analyze a task from multiple perspectives. Use when user needs multi-expert analysis, diverse perspectives, or thorough review of a complex topic.
argument-hint: <task-description>
---

# Expert Panel Analysis

Create a panel of domain experts to analyze: $ARGUMENTS

## The 5 Universal Archetypes

| ID | Name | Perspective |
|----|------|-------------|
| ARC-TH | Theoretical | Formal analysis, proofs, invariants |
| ARC-AD | Adversarial | Attack surface, red team thinking |
| ARC-IM | Implementation | Engineering, optimization, scaling |
| ARC-ST | Strategic | Big picture, trade-offs, planning |
| ARC-QA | Quality | Testing, compliance, verification |

## Execution

1. Synthesize expert panel:
```
mcp__omega-nexus__omega_archetype(
    action="synthesize_panel",
    task="$ARGUMENTS",
    panel_size=5
)
```

2. Spawn agents for parallel analysis:
```
mcp__omega-nexus__omega_spawn(agents=<panel_experts>, task="$ARGUMENTS")
```

3. Aggregate results:
```
mcp__omega-nexus__omega_aggregate(outputs=<results>, method="confidence_weighted_average")
```

## Output

Report each expert's perspective and the aggregated consensus with confidence score.
