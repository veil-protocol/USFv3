---
name: precision
description: Set verification depth for operations. Higher precision = more parallel verification chains.
argument-hint: <level-1-5>
---

# Precision Level Control

Set precision level: $ARGUMENTS

## Precision Levels

| Level | Chains | Speed | Use Case |
|-------|--------|-------|----------|
| PL1 | 1 | Fastest | Quick lookups, low-risk |
| PL2 | 2 | Fast | Standard research |
| PL3 | 3 | Balanced | Important decisions |
| PL4 | 5 | Thorough | Security-critical |
| PL5 | 9 | Maximum | Adversarial review |

## Execution

1. **Validate level** (1-5)
2. **Configure verification chains**
3. **Enable early-exit consensus** (PL3+)

## Output

Confirmation of precision level and verification chain count.
