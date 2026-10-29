---
name: archetype
description: Select agent persona for specialized operations. Use to configure agent behavior and expertise.
argument-hint: <persona>
---

# Agent Archetype Selection

Activate archetype: $ARGUMENTS

## Available Archetypes

| Archetype | Expertise | Use Case |
|-----------|-----------|----------|
| red-team | Offensive security | Full attack chains |
| blue-team | Defensive security | Detection, hardening |
| forensics | Digital forensics | Incident response |
| researcher | Security research | CVE analysis, techniques |
| auditor | Compliance | Security assessments |

## Execution

1. **Load archetype context**
```
mcp__omega-nexus__omega_vault_query(
    query="$ARGUMENTS methodology framework",
    context="security",
    limit=10
)
```

2. **Configure behavior**
- Adjust risk tolerance
- Set output verbosity
- Enable/disable automation

## Output

Archetype activation confirmation with configured behaviors.
