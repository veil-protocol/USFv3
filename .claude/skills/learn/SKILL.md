---
name: learn
description: Cross-session learning and technique recommendations. Use to record successes or get recommendations based on history.
argument-hint: [record|recommend|history|weights]
---

# Learning System

Action: $ARGUMENTS

## Actions

- `record` - Record a successful technique
- `recommend` - Get recommendations for target type
- `history` - View learning history
- `weights` - View technique weights

## Execution

```
mcp__omega-nexus__omega_learn(
    action="$ARGUMENTS",
    target_type="<linux|windows|web|ad|cloud>",
    technique="<technique-name>",
    success=true
)
```

## Example: Get Recommendations

```
mcp__omega-nexus__omega_learn(
    action="recommend",
    target_type="linux"
)
```

## Output

Display recommendations ranked by historical success rate.
