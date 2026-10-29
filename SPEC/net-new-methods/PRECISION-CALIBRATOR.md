# USF 4.0: Precision Calibrator

> **Version**: 4.0.0
> **Component**: Precision / Precision Calibrator
> **Status**: Specification
> **Dependencies**: core/PRECISION-LEVELS.md, domain-adaptation/DOMAIN-DETECTOR.md

---

## 1. Overview

The Precision Calibrator determines the appropriate rigor level for each task, balancing thoroughness against efficiency. It analyzes task characteristics, domain requirements, and contextual factors to assign precision levels that ensure adequate quality without unnecessary overhead.

```
PRECISION CALIBRATION FLOW
═══════════════════════════════════════════════════════════════════════════════

    INPUTS                      CALIBRATION                     OUTPUT
    ──────                      ───────────                     ──────

    ┌─────────────┐
    │   TASK      │───┐
    │  CONTEXT    │   │
    └─────────────┘   │         ┌─────────────────────┐
                      │         │                     │         ┌──────────┐
    ┌─────────────┐   ├────────►│  PRECISION ENGINE   │────────►│   PL3    │
    │   DOMAIN    │───┤         │                     │         │          │
    │  PROFILE    │   │         │  • Factor Analysis  │         │ + Config │
    └─────────────┘   │         │  • Override Rules   │         │ + Methods│
                      │         │  • Calibration Adj  │         └──────────┘
    ┌─────────────┐   │         │                     │
    │   USER      │───┘         └─────────────────────┘
    │  CONTEXT    │
    └─────────────┘

═══════════════════════════════════════════════════════════════════════════════
```

---

## 2. Input Analysis

### 2.1 Task Context Extraction

```yaml
task_context_extraction:
  explicit_signals:
    stated_requirements:
      detection: "User explicitly states precision needs"
      examples:
        - "Need formal proof" → PL4+
        - "Quick overview" → PL1
        - "Rigorous analysis" → PL3+
        - "High-level assessment" → PL1-2

    criticality_indicators:
      detection: "Language indicating importance"
      examples:
        high: ["critical", "essential", "must be correct", "life-safety"]
        medium: ["important", "significant", "thorough"]
        low: ["preliminary", "initial", "rough estimate"]

    timeline_indicators:
      detection: "Time pressure signals"
      examples:
        urgent: ["ASAP", "immediately", "urgent", "by EOD"]
        normal: ["when possible", "soon"]
        relaxed: ["no rush", "when convenient", "thorough > fast"]

  implicit_signals:
    task_complexity:
      indicators:
        - "Number of components mentioned"
        - "Depth of technical requirements"
        - "Number of constraints"
        - "Interdependencies described"
      scoring: "1-5 based on complexity indicators"

    novelty:
      indicators:
        - "New/unfamiliar domain aspects"
        - "Unusual requirements"
        - "Edge cases mentioned"
      impact: "Higher novelty → higher precision"

    reversibility:
      indicators:
        - "Deployment implications"
        - "Permanence of decisions"
        - "Rollback capability"
      impact: "Less reversible → higher precision"
```

### 2.2 Domain-Based Defaults

```yaml
domain_defaults:
  lookup_table:
    T.SEC:
      default: PL3
      minimum: PL2
      rationale: "Security errors have high impact"

    T.SEC.CRY:
      default: PL4
      minimum: PL3
      rationale: "Cryptographic errors catastrophic"

    T.DEV:
      default: PL2
      minimum: PL1
      rationale: "Standard development work"

    S.MED:
      default: PL3
      minimum: PL2
      rationale: "Patient safety concerns"

    L.REG:
      default: PL3
      minimum: PL2
      rationale: "Compliance accuracy required"

    B.STR:
      default: PL2
      minimum: PL1
      rationale: "Business decisions"

    E.ENG.AER:
      default: PL4
      minimum: PL4
      rationale: "Aerospace safety critical"

  application:
    process:
      1: "Get primary domain from Domain Detector"
      2: "Look up domain defaults"
      3: "Use as starting point for calibration"
```

### 2.3 User Context Factors

```yaml
user_context:
  user_expertise:
    detection: "User's apparent expertise level"
    impact:
      expert_user: "May need less explanation, same rigor"
      novice_user: "May need more explanation, same rigor"

  user_trust_profile:
    detection: "Historical accuracy of user's precision requests"
    impact:
      calibrated_user: "Trust user's precision requests"
      uncalibrated_user: "May override unrealistic requests"

  organizational_context:
    detection: "Industry, regulatory environment"
    impact:
      regulated_industry: "Minimum precision for compliance"
      startup_environment: "May accept lower precision for speed"
```

---

## 3. Calibration Algorithm

### 3.1 Factor Scoring

```yaml
factor_scoring:
  factors:
    consequence_severity:
      id: CS
      range: [1, 5]
      assessment:
        - "What is the impact of errors?"
        - "Who/what is affected?"
        - "How permanent is the damage?"
      scoring_guide:
        1: "Minimal impact, easily fixed"
        2: "Minor impact, some effort to fix"
        3: "Moderate impact, significant effort"
        4: "Major impact, substantial harm"
        5: "Catastrophic, irreversible harm"

    domain_complexity:
      id: DC
      range: [1, 5]
      assessment:
        - "How complex is the domain?"
        - "How many interacting components?"
        - "How well understood is the space?"
      scoring_guide:
        1: "Simple, well-understood"
        2: "Moderate complexity"
        3: "Complex, multiple subsystems"
        4: "Highly complex, emergent behavior"
        5: "Extreme complexity, novel territory"

    adversarial_exposure:
      id: AE
      range: [1, 5]
      assessment:
        - "Is there an adversary?"
        - "How capable is the adversary?"
        - "What are their resources?"
      scoring_guide:
        1: "No adversary"
        2: "Opportunistic adversary"
        3: "Motivated adversary"
        4: "Well-resourced adversary"
        5: "Nation-state adversary"

    verification_availability:
      id: VA
      range: [1, 5]
      assessment:
        - "Can we verify correctness?"
        - "What verification methods available?"
        - "How complete can verification be?"
      scoring_guide:
        1: "No verification possible"
        2: "Limited testing only"
        3: "Comprehensive testing"
        4: "Formal methods applicable"
        5: "Full formal verification possible"

    time_criticality:
      id: TC
      range: [1, 5]
      assessment:
        - "How urgent is the task?"
        - "What are the deadline constraints?"
        - "Is speed more important than depth?"
      scoring_guide:
        1: "No time pressure"
        2: "Flexible timeline"
        3: "Moderate deadline"
        4: "Tight deadline"
        5: "Immediate response required"
      note: "This is an inverse factor - higher TC reduces precision"
```

### 3.2 Precision Calculation

```yaml
precision_calculation:
  formula: |
    raw_score = CS + DC + AE + VA - TC

    // Normalize to [0, 4] range
    // Minimum: 1+1+1+1-5 = -1
    // Maximum: 5+5+5+5-1 = 19
    normalized = (raw_score + 1) / 5

    // Map to precision level
    precision_level = floor(normalized) + 1
    precision_level = clamp(precision_level, 1, 5)

  example_calculations:
    low_stakes_quick:
      CS: 1
      DC: 2
      AE: 1
      VA: 3
      TC: 4
      raw: "1+2+1+3-4 = 3"
      normalized: "4/5 = 0.8"
      result: "PL1"

    security_analysis:
      CS: 4
      DC: 4
      AE: 4
      VA: 4
      TC: 2
      raw: "4+4+4+4-2 = 14"
      normalized: "15/5 = 3.0"
      result: "PL4"

    emergency_triage:
      CS: 4
      DC: 3
      AE: 2
      VA: 2
      TC: 5
      raw: "4+3+2+2-5 = 6"
      normalized: "7/5 = 1.4"
      result: "PL2"
```

### 3.3 Override Rules

```yaml
override_rules:
  mandatory_upgrades:
    - rule: "Cryptography always PL3+"
      condition: "domain MATCHES T.SEC.CRY.*"
      action: "precision = max(precision, PL3)"
      rationale: "Crypto errors are catastrophic"

    - rule: "Safety-critical always PL4+"
      condition: "domain IN [E.ENG.AER, E.ENG.NUC, S.MED.SUR]"
      action: "precision = max(precision, PL4)"
      rationale: "Life-safety requires highest assurance"

    - rule: "Nation-state adversary PL4+"
      condition: "AE == 5"
      action: "precision = max(precision, PL4)"
      rationale: "APT threats require verification"

    - rule: "Regulatory compliance PL3+"
      condition: "task requires regulatory certification"
      action: "precision = max(precision, PL3)"
      rationale: "Compliance requires documented rigor"

  permitted_downgrades:
    - rule: "Emergency with low consequence"
      condition: "TC == 5 AND CS <= 2"
      action: "precision = min(precision, PL1)"
      rationale: "Emergency response accepts lower rigor"

    - rule: "User explicit override"
      condition: "user_requests_override AND user_authorized"
      action: "accept user's precision level"
      requirement: "Document risk acceptance"
```

---

## 4. Calibration Outputs

### 4.1 Precision Configuration

```yaml
precision_configuration:
  output_structure:
    precision_level: "PL1-PL5"

    configuration:
      methods_enabled: ["List of analysis methods"]
      chains_required: "N chains with M agreement"
      iteration_depth: "Expected iteration count"
      convergence_criteria: "How to determine completion"
      confidence_target: "Target confidence percentage"

    panel_impact:
      size_factor: "Panel size multiplier"
      archetype_shift: "Archetype balance adjustments"
      expert_depth: "Expert specialization level"

    resource_estimate:
      time_factor: "Relative to baseline"
      complexity_factor: "Expected compute load"

  example_output:
    precision_level: "PL3"
    configuration:
      methods_enabled:
        - "Formal specification"
        - "Proof sketches"
        - "Bounded model checking"
        - "Invariant verification"
      chains_required: "4/5 agree"
      iteration_depth: 3-5
      convergence_criteria: "All critical claims have proof sketches"
      confidence_target: 95%
    panel_impact:
      size_factor: 1.5
      archetype_shift: "Increase ARC-TH by 10%"
      expert_depth: "Specialist level"
    resource_estimate:
      time_factor: 0.8
      complexity_factor: 1.2
```

### 4.2 Calibration Rationale

```yaml
calibration_rationale:
  purpose: "Explain why precision level was selected"

  rationale_structure:
    calculated_level: "Base level from formula"
    factor_contributions:
      - factor: "CS"
        score: 4
        contribution: "High consequence severity"
      - factor: "DC"
        score: 3
        contribution: "Moderate complexity"
      # ... for each factor

    overrides_applied:
      - override: "Cryptography minimum PL3"
        effect: "Upgraded from PL2 to PL3"

    final_level: "Result after overrides"

    confidence_in_calibration:
      score: 0.85
      basis: "Clear signals, no ambiguity"
```

---

## 5. Dynamic Recalibration

### 5.1 Recalibration Triggers

```yaml
recalibration_triggers:
  discovery_based:
    complexity_increase:
      trigger: "Discovered complexity exceeds initial estimate"
      detection: "More components, deeper dependencies found"
      response: "Recalculate with updated DC"

    criticality_increase:
      trigger: "Discovered higher stakes than anticipated"
      detection: "Critical assets or dependencies found"
      response: "Recalculate with updated CS"

    adversary_upgrade:
      trigger: "Stronger adversary than anticipated"
      detection: "Threat model reveals sophisticated attacker"
      response: "Recalculate with updated AE"

  confidence_based:
    confidence_gap:
      trigger: "Cannot achieve confidence target at current level"
      detection: "Convergence stalled, uncertainty high"
      response: "Upgrade precision level"

    verification_blocked:
      trigger: "Required verification not possible at current level"
      detection: "Methods insufficient for claims"
      response: "Upgrade to access stronger methods"

  external:
    user_request:
      trigger: "User requests precision change"
      validation: "Check if request is reasonable"
      response: "Recalibrate if valid"

    timeline_change:
      trigger: "Deadline extended or accelerated"
      impact: "Adjust TC factor"
      response: "Recalculate precision"
```

### 5.2 Recalibration Protocol

```yaml
recalibration_protocol:
  upgrade_path:
    steps:
      1: "Identify upgrade trigger"
      2: "Recalculate precision with new factors"
      3: "Identify delta from current level"
      4: "Expand methods and resources"
      5: "Notify panel of new requirements"
      6: "Continue from current progress"

    preservation:
      - "Prior analysis remains valid"
      - "Upgrade adds depth, doesn't restart"
      - "Track which findings are level-specific"

  downgrade_path:
    permitted: "Only with explicit justification"
    steps:
      1: "Verify downgrade is appropriate"
      2: "Document risk acceptance"
      3: "Reduce methods and resources"
      4: "Note reduced confidence in outputs"

    restrictions:
      - "Cannot downgrade below domain minimum"
      - "Cannot downgrade after high-severity finding"
      - "Requires documentation"
```

---

## 6. Calibration Quality

### 6.1 Calibration Accuracy Tracking

```yaml
calibration_accuracy:
  purpose: "Measure how well calibration predicts needed precision"

  metrics:
    upgrade_rate:
      definition: "How often mid-task upgrades needed"
      target: "< 10%"
      interpretation: "High rate = undercalibrating"

    overspec_rate:
      definition: "How often task could have used less precision"
      target: "< 20%"
      interpretation: "High rate = overcalibrating"
      detection: "Minimal use of advanced methods"

    confidence_achievement:
      definition: "Did we achieve target confidence?"
      target: "> 95%"
      interpretation: "Low rate = miscalibration"

  tracking:
    per_task: "Record calibration decision and outcome"
    aggregate: "Weekly analysis of calibration accuracy"
    by_domain: "Accuracy per domain category"
```

### 6.2 Calibration Improvement

```yaml
calibration_improvement:
  feedback_loop:
    data_collection:
      - "Initial calibration decision"
      - "Mid-task adjustments"
      - "Final precision actually needed"
      - "Quality metrics achieved"

    analysis:
      - "Identify systematic miscalibration"
      - "Find factor scoring errors"
      - "Detect missing override rules"

    improvement:
      - "Adjust factor weights"
      - "Refine scoring guides"
      - "Add new override rules"
      - "Update domain defaults"

  meta_analysis_integration:
    agent: "MAL-QUALITY"
    reports: "Calibration accuracy metrics"
    proposes: "Calibration parameter updates"
```

---

## 7. Integration Points

### 7.1 Domain Detector Integration

```yaml
domain_detector:
  receives: "DomainProfile"
  uses:
    - "Primary domain for defaults"
    - "Secondary domains for complexity"
    - "Domain confidence for uncertainty"
```

### 7.2 Phase Template Integration

```yaml
phase_template:
  provides: "Precision level to template selector"
  impact:
    - "Template depth selection"
    - "Gate criteria strictness"
    - "Iteration limits"
```

### 7.3 Expert Generator Integration

```yaml
expert_generator:
  provides: "Precision level for panel sizing"
  impact:
    - "Panel size"
    - "Expert depth"
    - "Archetype balance shifts"
```

---

## Appendix A: Precision Calibrator Quick Reference

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                   USF 4.0 PRECISION CALIBRATOR REFERENCE                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  FACTORS: CS (consequence) + DC (complexity) + AE (adversary) +             ║
║           VA (verification) - TC (time)                                      ║
║                                                                              ║
║  FORMULA: PL = floor((raw + 1) / 5) + 1, clamped to [1,5]                   ║
║                                                                              ║
║  OVERRIDES:                                                                  ║
║    Crypto → PL3+, Safety-critical → PL4+, Nation-state → PL4+               ║
║                                                                              ║
║  RECALIBRATION: On discovery, confidence gap, or user request               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## Appendix B: Change Log

| Version | Date | Changes |
|---------|------|---------|
| 4.0.0 | 2025-12-10 | Initial USF 4.0 precision calibrator specification |

---

*This document is part of the USF 4.0 specification suite. See MASTER-SPECIFICATION.md for framework overview.*
