---
name: status
description: Check OMEGA-NEXUS MCP server health and available tools. Use to verify the system is working correctly.
---

# OMEGA Status Check

Check system health and available tools.

## Execution

```
mcp__omega-nexus__omega_status()
```

## Checks Performed

- MCP server initialization
- SSH connectivity to Kali box
- Environment configuration
- Available tools (19 total)
- Security module status

## Output

Report overall health status and any issues detected.
