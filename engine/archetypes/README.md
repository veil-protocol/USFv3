# USF 7.0 Archetype Templates

**Version**: 7.0
**Total Archetypes**: 5

---

## Overview

These archetype templates define the 5 universal expert personas used by USF's persona synthesis system. Each archetype includes:

1. **Reasoning Protocol**: 5-phase `<thinking>` block pattern for structured reasoning
2. **Output Markers**: Structured output format (`[FINDING]`, `[STAT:*]`, `[DATA]`, `[LIMITATION]`)
3. **Domain Synthesis**: How the archetype adapts to different domain contexts
4. **Quality Criteria**: Standards for output validation

---

## Archetypes

| ID | Name | Mode | Primary Focus |
|----|------|------|---------------|
| **ARC-TH** | Domain Theorist | Theoretical Analysis | Formal reasoning, proofs, invariants |
| **ARC-AD** | Adversarial Analyst | Attack Surface | Red team, exploits, vulnerabilities |
| **ARC-IM** | Implementation Expert | Engineering | Building, optimizing, scaling |
| **ARC-ST** | Strategic Planner | Holistic Synthesis | Big picture, trade-offs, roadmaps |
| **ARC-QA** | Quality Analyst | Verification | Testing, compliance, coverage |

---

## 5-Phase Reasoning Protocol

All archetypes use this thinking pattern within `<thinking>` tags:

1. **Initial Engagement**: Rephrase the problem, map key components
2. **Problem Analysis**: Break down into sub-components
3. **Multiple Hypotheses**: Explore different interpretations
4. **Natural Discovery**: Build insights progressively
5. **Verification**: Cross-check conclusions against evidence

---

## Structured Output Markers

| Marker | Purpose | Example |
|--------|---------|---------|
| `[FINDING]` | Key discoveries | `[FINDING] SQL injection in /api/users` |
| `[STAT:CONFIDENCE]` | Confidence level (0.0-1.0) | `[STAT:CONFIDENCE] 0.92` |
| `[STAT:SEVERITY]` | Severity rating | `[STAT:SEVERITY] Critical (CVSS 9.8)` |
| `[STAT:COVERAGE]` | Test coverage | `[STAT:COVERAGE] 78%` |
| `[STAT:COMPLEXITY]` | Implementation effort | `[STAT:COMPLEXITY] Medium (~40h)` |
| `[STAT:IMPACT]` | Expected impact | `[STAT:IMPACT] High` |
| `[STAT:COMPLETENESS]` | Theoretical completeness | `[STAT:COMPLETENESS] 0.72` |
| `[DATA]` | Supporting evidence | `[DATA] Payload: admin' OR '1'='1'` |
| `[LIMITATION]` | Scope constraints | `[LIMITATION] Only tested unauthenticated` |

---

## Domain Synthesis Matrix

When archetypes are synthesized with domain context, they produce specialized experts:

| Archetype | Security | Legal | Medical | Engineering | Business |
|-----------|----------|-------|---------|-------------|----------|
| ARC-TH | Security Researcher | Legal Theorist | Clinical Researcher | Systems Theorist | Strategy Theorist |
| ARC-AD | Red Team Operator | Litigation Adversary | Clinical Risk Analyst | Failure Analyst | Competitive Analyst |
| ARC-IM | Security Engineer | Legal Tech Specialist | Clinical Informaticist | Design Engineer | Operations Expert |
| ARC-ST | Security Architect | Managing Partner | Medical Director | Chief Engineer | Strategy Director |
| ARC-QA | Security Auditor | Compliance Officer | Quality Officer | V&V Engineer | Quality Manager |

---

## Usage

### In Python (USF Executor)
```python
from usf_executor import USFExecutor

executor = USFExecutor()

# Synthesize a persona
persona = executor.archetype_loader.synthesize_persona(
    archetype_id="ARC-AD",
    domain="security",
    task_context="penetration test of web application"
)

print(persona.expertise_prompt)  # Full persona with thinking protocol
```

### In Agent Registry (registry.yaml)
```yaml
prompt_template: |
  {{archetype:ARC-AD}}

  Task: {task}

  Apply adversarial analysis methodology.
```

---

## Pattern Parsing

The structured markers can be parsed with regex:

```python
import re

def parse_findings(output: str) -> list[dict]:
    findings = []
    pattern = r'\[FINDING\] (.+?)(?=\[|$)'
    for match in re.finditer(pattern, output, re.DOTALL):
        findings.append({"content": match.group(1).strip()})
    return findings

def parse_stats(output: str) -> dict[str, str]:
    stats = {}
    pattern = r'\[STAT:(\w+)\] (.+?)(?=\[|$)'
    for match in re.finditer(pattern, output, re.DOTALL):
        stats[match.group(1).lower()] = match.group(2).strip()
    return stats
```

---

## Changelog

- **7.0**: Added 5-phase `<thinking>` protocol, structured output markers
- **6.5**: Initial archetype system with persona synthesis
