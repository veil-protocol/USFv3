# USF 4.0: Precision Levels

> **Version**: 4.1.1 (See VERSION.yaml)
> **Component**: Core / Precision Levels
> **Status**: Specification
> **Dependencies**: DOMAIN-TAXONOMY.md, EXPERT-ARCHETYPES.md, MASTER-SPECIFICATION.md
> **Last Updated**: 2025-12-10
> **SKYNET Integration**: Think command escalation mapping

---

## 1. Overview

USF 4.0 Precision Levels ensure that analysis rigor matches task requirements. Under-analysis wastes opportunity; over-analysis wastes resources. The Precision Calibration Engine automatically determines the appropriate rigor level and adapts execution accordingly.

```
PRECISION LEVEL SPECTRUM
═══════════════════════════════════════════════════════════════════════════════

    RIGOR LEVEL
         ▲
    100% │                                            ┌─────────┐
         │                                            │   PL5   │
         │                                            │ IT-GUAR │
     99% │                              ┌─────────┐   └────┬────┘
         │                              │   PL4   │        │
         │                              │ VERIFIED│   Information-
     95% │                ┌─────────┐   └────┬────┘   Theoretic
         │                │   PL3   │        │        Proofs
         │                │ FORMAL  │   Machine
     90% │  ┌─────────┐   └────┬────┘   Verification
         │  │   PL2   │        │
         │  │DETAILED │   Formal
     80% │  └────┬────┘   Methods
         │       │
         │  Behavioral
    ─────┼───────────────────────────────────────────────────────────────────►
         │   PL1          Analysis Depth
         │  OVERVIEW
         │
         └───────────────────────────────────────────────────────────────────

    CONFIDENCE GUARANTEE: 80% ──────► 90% ──────► 95% ──────► 99% ──────► 100%

═══════════════════════════════════════════════════════════════════════════════
```

---

## 2. Precision Level Definitions

### 2.1 PL1: Overview (80% Confidence)

**Purpose**: Rapid assessment, high-level understanding, preliminary scoping

```yaml
precision_level:
  id: PL1
  name: "Overview"
  confidence_target: 80%
  alias: ["Quick", "Preliminary", "Scoping"]

  characteristics:
    depth: "Surface-level analysis"
    breadth: "Wide coverage, shallow depth"
    rigor: "Heuristic-based"
    time_factor: 0.2  # 20% of full analysis time

  methods:
    primary:
      - "Structural analysis"
      - "Pattern recognition"
      - "Heuristic application"
      - "Known issue checking"
    excluded:
      - "Formal verification"
      - "Exhaustive enumeration"
      - "Mathematical proofs"

  expert_configuration:
    panel_size: 5-7
    iteration_depth: 1-2 cycles
    archetype_emphasis: [ARC-ST, ARC-IM]  # Strategic, practical

  outputs:
    - "High-level assessment"
    - "Major issue identification"
    - "Preliminary recommendations"
    - "Scope for deeper analysis"

  appropriate_for:
    - "Initial project scoping"
    - "Go/no-go decisions"
    - "Resource estimation"
    - "Preliminary risk assessment"
    - "Time-critical situations"

  not_appropriate_for:
    - "Safety-critical systems"
    - "Legal/regulatory compliance"
    - "Cryptographic security"
    - "High-stakes decisions"

  convergence_criteria:
    chains_required: "2/3 agree"
    minimum_coverage: 60%
    maximum_uncertainty: 20%
```

---

### 2.2 PL2: Detailed (90% Confidence)

**Purpose**: Thorough analysis with behavioral examination, standard professional work

```yaml
precision_level:
  id: PL2
  name: "Detailed"
  confidence_target: 90%
  alias: ["Standard", "Professional", "Comprehensive"]

  characteristics:
    depth: "Behavioral analysis"
    breadth: "Good coverage with moderate depth"
    rigor: "Evidence-based with structured methodology"
    time_factor: 0.5  # 50% of full analysis time

  methods:
    primary:
      - "Behavioral analysis"
      - "State machine modeling"
      - "Timing analysis"
      - "Interface testing"
      - "Scenario walkthrough"
    enhanced:
      - "Static analysis (automated)"
      - "Dynamic testing"
      - "Expert review"
    excluded:
      - "Formal proofs"
      - "Theorem proving"
      - "Information-theoretic analysis"

  expert_configuration:
    panel_size: 7-11
    iteration_depth: 2-3 cycles
    archetype_emphasis: [ARC-IM, ARC-AD, ARC-QA]  # Implementation, adversarial, quality

  outputs:
    - "Detailed assessment report"
    - "Issue catalog with severity"
    - "Behavioral models"
    - "Test coverage analysis"
    - "Actionable recommendations"

  appropriate_for:
    - "Standard software development"
    - "Business process analysis"
    - "Most engineering projects"
    - "Risk assessment (non-critical)"
    - "Due diligence (standard)"

  not_appropriate_for:
    - "Life-safety systems"
    - "Cryptographic primitives"
    - "Regulatory certification"
    - "Nation-state threat models"

  convergence_criteria:
    chains_required: "3/4 agree"
    minimum_coverage: 80%
    maximum_uncertainty: 10%
```

---

### 2.3 PL3: Formal (95% Confidence)

**Purpose**: Rigorous analysis with formal methods, high-assurance work

```yaml
precision_level:
  id: PL3
  name: "Formal"
  confidence_target: 95%
  alias: ["Rigorous", "High-Assurance", "Formal Methods"]

  characteristics:
    depth: "Formal reasoning with proof sketches"
    breadth: "Complete coverage of critical paths"
    rigor: "Mathematical with formal notation"
    time_factor: 0.8  # 80% of full analysis time

  methods:
    primary:
      - "Formal specification"
      - "Invariant identification"
      - "Pre/post condition analysis"
      - "Proof sketches"
      - "Model checking (bounded)"
    enhanced:
      - "Type system analysis"
      - "Abstract interpretation"
      - "Symbolic execution"
    required:
      - "Formal notation for claims"
      - "Explicit assumption documentation"
      - "Logical argument structure"

  expert_configuration:
    panel_size: 11-15
    iteration_depth: 3-5 cycles
    archetype_emphasis: [ARC-TH, ARC-AD, ARC-QA]  # Theoretical, adversarial, quality

  outputs:
    - "Formal specification"
    - "Proof sketches"
    - "Invariant documentation"
    - "Model checking results"
    - "Verified claims list"
    - "Assumption register"

  appropriate_for:
    - "Security protocol design"
    - "Financial system components"
    - "Medical device software"
    - "Aerospace components"
    - "Regulatory certification"

  not_appropriate_for:
    - "Rapid prototyping"
    - "Low-risk applications"
    - "Exploratory projects"

  convergence_criteria:
    chains_required: "4/5 agree"
    minimum_coverage: 95%
    maximum_uncertainty: 5%
    formal_requirements:
      - "All critical claims have proof sketches"
      - "All assumptions explicitly documented"
      - "Model checking completes without counterexamples"
```

---

### 2.4 PL4: Verified (99% Confidence)

**Purpose**: Machine-verified analysis, highest practical assurance

```yaml
precision_level:
  id: PL4
  name: "Verified"
  confidence_target: 99%
  alias: ["Machine-Verified", "Certified", "Provably Correct"]

  characteristics:
    depth: "Machine-checked proofs"
    breadth: "Complete formal coverage"
    rigor: "Mechanically verified"
    time_factor: 1.5  # 150% of standard analysis time

  methods:
    primary:
      - "Theorem prover encoding"
      - "Model checking (exhaustive)"
      - "Proof assistant verification"
      - "Certified compilation"
    required:
      - "Machine-checkable proofs"
      - "Formal semantics"
      - "Verified toolchain"
    tools:
      - "Coq/Lean/Isabelle (theorem provers)"
      - "TLA+/Alloy (model checkers)"
      - "SPIN/NuSMV (protocol verification)"
      - "CompCert/seL4 (verified systems)"

  expert_configuration:
    panel_size: 15-21
    iteration_depth: 5+ cycles
    archetype_emphasis: [ARC-TH, ARC-QA]  # Heavy theoretical, quality
    special_requirements:
      - "Formal methods specialist required"
      - "Tool expert for each verification tool"

  outputs:
    - "Machine-checkable proofs"
    - "Verification tool output logs"
    - "Formal specification (verified)"
    - "Assumption minimization"
    - "Certified components"

  appropriate_for:
    - "Cryptographic implementations"
    - "Safety-critical systems"
    - "High-value targets"
    - "Long-lifecycle systems"
    - "Regulatory highest tier"

  limitations:
    - "Trusted computing base still exists"
    - "Proofs may not cover implementation"
    - "Assumptions must still be validated"
    - "High resource requirements"

  convergence_criteria:
    chains_required: "5/5 agree"
    minimum_coverage: 99%
    maximum_uncertainty: 1%
    formal_requirements:
      - "All proofs machine-checked"
      - "No unverified assumptions in critical path"
      - "Verification tools complete without errors"
```

---

### 2.5 PL5: Information-Theoretic (100% Confidence)

**Purpose**: Unconditional security guarantees, theoretical maximum assurance

```yaml
precision_level:
  id: PL5
  name: "Information-Theoretic"
  confidence_target: 100%
  alias: ["Unconditional", "IT-Secure", "Perfect"]

  characteristics:
    depth: "Information-theoretic proofs"
    breadth: "Complete adversarial model"
    rigor: "Mathematical certainty"
    time_factor: 3.0+  # 300%+ of standard analysis time

  methods:
    primary:
      - "Shannon entropy analysis"
      - "Perfect secrecy proofs"
      - "Unconditional security arguments"
      - "Information-theoretic reductions"
    required:
      - "Formal adversary model (unbounded)"
      - "Information-theoretic definitions"
      - "Entropy calculations"
      - "Security game formalization"
    constraints:
      - "No computational assumptions"
      - "Security against unbounded adversary"
      - "Mathematical certainty"

  expert_configuration:
    panel_size: 21 (maximum)
    iteration_depth: Unbounded (until proof complete)
    archetype_emphasis: [ARC-TH]  # Heavily theoretical
    special_requirements:
      - "Information theory specialist"
      - "Cryptography theorist"
      - "External peer review"

  outputs:
    - "Information-theoretic security proof"
    - "Formal adversary model"
    - "Security game definition"
    - "Entropy bounds"
    - "Unconditional guarantees"

  appropriate_for:
    - "One-time pad security"
    - "Quantum key distribution"
    - "Secret sharing schemes"
    - "Certain secure computation protocols"
    - "Theoretical foundations"

  limitations:
    - "Few practical systems achieve PL5"
    - "Often requires idealized assumptions"
    - "May not be achievable for given problem"
    - "Resource intensive"

  special_considerations:
    - "PL5 may be impossible for computational problems"
    - "Acknowledge when PL5 is unattainable"
    - "Document gap between PL4 and theoretical PL5"

  convergence_criteria:
    chains_required: "5/5 agree + external review"
    minimum_coverage: 100%
    maximum_uncertainty: 0%
    formal_requirements:
      - "Complete information-theoretic proof"
      - "Peer-reviewed by external experts"
      - "Published or publishable quality"
```

---

## 3. Precision Level Calculation

### 3.1 Input Factors

```yaml
precision_factors:
  consequence_severity:
    id: CS
    range: [1, 5]
    description: "Impact of errors or failures"
    values:
      1: "Minimal impact, easily reversed"
      2: "Minor impact, some cost to fix"
      3: "Moderate impact, significant cost"
      4: "Major impact, substantial harm"
      5: "Catastrophic, irreversible harm"

  domain_complexity:
    id: DC
    range: [1, 5]
    description: "Inherent complexity of the domain"
    values:
      1: "Well-understood, few variables"
      2: "Moderately complex, known patterns"
      3: "Complex, multiple interacting systems"
      4: "Highly complex, emergent behaviors"
      5: "Extreme complexity, novel territory"

  adversarial_exposure:
    id: AE
    range: [1, 5]
    description: "Degree of adversarial threat"
    values:
      1: "No adversary expected"
      2: "Opportunistic adversaries"
      3: "Motivated adversaries"
      4: "Well-resourced adversaries"
      5: "Nation-state adversaries"

  verification_availability:
    id: VA
    range: [1, 5]
    description: "Ability to verify correctness"
    values:
      1: "No verification possible"
      2: "Limited testing only"
      3: "Comprehensive testing available"
      4: "Formal methods applicable"
      5: "Full formal verification possible"

  time_criticality:
    id: TC
    range: [1, 5]
    description: "Urgency (inverse factor)"
    values:
      1: "No time pressure"
      2: "Flexible timeline"
      3: "Moderate deadline"
      4: "Tight deadline"
      5: "Immediate response required"
```

### 3.2 Calculation Algorithm

```
PRECISION LEVEL CALCULATION
═══════════════════════════════════════════════════════════════════════════════

INPUT: CS, DC, AE, VA, TC ∈ [1, 5]

FORMULA:
  raw_score = (CS + DC + AE + VA - TC)

  // Normalize to [0, 4] range
  // Minimum: 1+1+1+1-5 = -1
  // Maximum: 5+5+5+5-1 = 19
  // Range: 20

  normalized = (raw_score + 1) / 5  // Maps to [0, 4]

  precision_level = floor(normalized) + 1  // Maps to [1, 5]

  // Clamp to valid range
  precision_level = max(1, min(5, precision_level))

OUTPUT: PL{precision_level}

═══════════════════════════════════════════════════════════════════════════════

EXAMPLES:

  Example 1: Low-risk internal tool
    CS=1, DC=2, AE=1, VA=3, TC=3
    raw_score = 1+2+1+3-3 = 4
    normalized = 5/5 = 1.0
    PL = floor(1.0) + 1 = 2 → PL2

  Example 2: Cryptographic protocol
    CS=5, DC=4, AE=5, VA=4, TC=2
    raw_score = 5+4+5+4-2 = 16
    normalized = 17/5 = 3.4
    PL = floor(3.4) + 1 = 4 → PL4

  Example 3: Emergency patch
    CS=4, DC=3, AE=4, VA=2, TC=5
    raw_score = 4+3+4+2-5 = 8
    normalized = 9/5 = 1.8
    PL = floor(1.8) + 1 = 2 → PL2

═══════════════════════════════════════════════════════════════════════════════
```

### 3.3 Override Rules

```yaml
precision_overrides:
  mandatory_upgrades:
    - condition: "Domain is T.SEC.CRY.*"
      minimum_level: PL3
      reason: "Cryptographic security requires formal methods"

    - condition: "Domain is S.MED.* AND CS >= 4"
      minimum_level: PL3
      reason: "Medical safety requires formal rigor"

    - condition: "Regulatory certification required"
      minimum_level: PL3
      reason: "Compliance requires documented rigor"

    - condition: "AE == 5 (Nation-state adversary)"
      minimum_level: PL4
      reason: "APT threat model requires verification"

  permitted_downgrades:
    - condition: "TC == 5 AND CS <= 2"
      maximum_level: PL1
      reason: "Emergency with low consequence allows quick assessment"

    - condition: "Explicitly requested by authorized user"
      any_level: true
      reason: "User override with documented acceptance"
      requires: "Documented risk acceptance"
```

---

## 4. Progressive Deepening Protocol

### 4.1 Level Transition Rules

```
PROGRESSIVE DEEPENING FLOW
═══════════════════════════════════════════════════════════════════════════════

START: Initial precision level from calculation

┌─────────────────────────────────────────────────────────────────────────────┐
│ Execute at current precision level                                          │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────┐          │
│   │ Check for deepening triggers:                                │          │
│   │                                                              │          │
│   │   □ Unexpected complexity discovered                         │          │
│   │   □ Critical vulnerability found                             │          │
│   │   □ Confidence threshold not met                             │          │
│   │   □ Expert disagreement exceeds threshold                    │          │
│   │   □ Coverage gaps identified                                 │          │
│   └─────────────────────────────────────────────────────────────┘          │
│                            │                                                │
│                            ▼                                                │
│              ┌──────────────────────────┐                                  │
│              │  Triggers present?        │                                  │
│              └────────────┬─────────────┘                                  │
│                          │                                                  │
│          NO              │              YES                                 │
│           │              │               │                                  │
│           ▼              │               ▼                                  │
│   ┌───────────────┐      │      ┌───────────────────┐                      │
│   │ Complete at   │      │      │ Upgrade precision │                      │
│   │ current level │      │      │ level (PL → PL+1) │                      │
│   └───────────────┘      │      └─────────┬─────────┘                      │
│                          │                │                                 │
│                          │                │ IF PL < PL5                     │
│                          │                ▼                                 │
│                          │      ┌─────────────────────┐                    │
│                          └──────│ Re-execute with     │                    │
│                                 │ upgraded level      │                    │
│                                 └─────────────────────┘                    │
└─────────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════
```

### 4.2 Deepening Trigger Specifications

```yaml
deepening_triggers:
  unexpected_complexity:
    definition: "Domain complexity higher than initially assessed"
    detection:
      - "Component count exceeds estimate by >50%"
      - "Interaction patterns more complex than modeled"
      - "New domain areas discovered during analysis"
    action: "Increase DC factor, recalculate PL"

  critical_vulnerability:
    definition: "High-severity issue found requiring deeper analysis"
    detection:
      - "CRITICAL/HIGH severity vulnerability identified"
      - "Attack chain to high-value asset discovered"
      - "Previously unknown vulnerability class found"
    action: "Increase CS and AE factors, upgrade PL"

  confidence_gap:
    definition: "Unable to achieve confidence target at current level"
    detection:
      - "Confidence < target - 5%"
      - "Multiple unresolved uncertainties"
      - "Key claims unverifiable at current level"
    action: "Upgrade PL to access stronger methods"

  expert_disagreement:
    definition: "Experts cannot reach consensus"
    detection:
      - "Disagreement persists after 3 iterations"
      - ">30% of experts dissent on critical claim"
      - "Fundamental assumption contested"
    action: "Upgrade PL for more rigorous resolution"

  coverage_gap:
    definition: "Unable to achieve coverage target"
    detection:
      - "Coverage < level requirement"
      - "Significant components unanalyzed"
      - "Attack surfaces unexplored"
    action: "Upgrade PL or extend scope"
```

### 4.3 Level Transition Protocol

```
LEVEL TRANSITION PROTOCOL
═══════════════════════════════════════════════════════════════════════════════

UPGRADE (PL_n → PL_n+1):

  1. Document upgrade justification
     - Trigger condition(s) met
     - Expected benefit from upgrade
     - Resource implications

  2. Reconfigure analysis
     - Expand expert panel
     - Activate additional methods
     - Increase iteration depth
     - Update convergence criteria

  3. Carry forward partial results
     - Previous findings remain valid
     - Upgrade adds depth, doesn't restart
     - Track which findings are level-specific

  4. Resume analysis at new level
     - Apply stricter methods
     - Re-examine uncertain claims
     - Fill coverage gaps

DOWNGRADE (PL_n → PL_n-1):

  Note: Downgrades are rare and require justification

  1. Verify downgrade is appropriate
     - Time criticality increased
     - Consequence severity reassessed
     - User-requested with risk acceptance

  2. Document downgrade decision
     - Explicit rationale
     - Risk acceptance if applicable
     - Residual uncertainty documentation

  3. Reconfigure analysis
     - Reduce expert panel (optional)
     - Relax convergence criteria
     - Accept lower coverage

═══════════════════════════════════════════════════════════════════════════════
```

---

## 5. Level-Specific Method Matrix

### 5.1 Analysis Methods by Level

```
METHOD AVAILABILITY MATRIX
═══════════════════════════════════════════════════════════════════════════════

Method                          │ PL1 │ PL2 │ PL3 │ PL4 │ PL5 │
────────────────────────────────┼─────┼─────┼─────┼─────┼─────┤
Heuristic analysis              │  ●  │  ●  │  ○  │  ○  │  ○  │
Pattern matching                │  ●  │  ●  │  ●  │  ○  │  ○  │
Structural analysis             │  ●  │  ●  │  ●  │  ●  │  ●  │
Behavioral analysis             │  ○  │  ●  │  ●  │  ●  │  ●  │
State machine modeling          │  ○  │  ●  │  ●  │  ●  │  ●  │
Static analysis (automated)     │  ○  │  ●  │  ●  │  ●  │  ●  │
Dynamic testing                 │  ○  │  ●  │  ●  │  ●  │  ●  │
Formal specification            │  ○  │  ○  │  ●  │  ●  │  ●  │
Proof sketches                  │  ○  │  ○  │  ●  │  ●  │  ●  │
Bounded model checking          │  ○  │  ○  │  ●  │  ●  │  ●  │
Invariant verification          │  ○  │  ○  │  ●  │  ●  │  ●  │
Theorem prover encoding         │  ○  │  ○  │  ○  │  ●  │  ●  │
Exhaustive model checking       │  ○  │  ○  │  ○  │  ●  │  ●  │
Machine-checked proofs          │  ○  │  ○  │  ○  │  ●  │  ●  │
Information-theoretic analysis  │  ○  │  ○  │  ○  │  ○  │  ●  │
Shannon entropy proofs          │  ○  │  ○  │  ○  │  ○  │  ●  │
Perfect secrecy proofs          │  ○  │  ○  │  ○  │  ○  │  ●  │

Legend: ● = Primary method, ○ = Available if needed, (blank) = Not applicable

═══════════════════════════════════════════════════════════════════════════════
```

### 5.2 Verification Chain Requirements by Level

```
VERIFICATION CHAIN REQUIREMENTS
═══════════════════════════════════════════════════════════════════════════════

Level │ Chains │ Agreement │ Independence │ Description
──────┼────────┼───────────┼──────────────┼─────────────────────────────────
PL1   │   3    │   2/3     │   Basic      │ Multiple perspectives, majority
PL2   │   4    │   3/4     │   Moderate   │ Different methods, supermajority
PL3   │   5    │   4/5     │   Strong     │ Formal separation, near-consensus
PL4   │   5    │   5/5     │   Full       │ Complete independence, unanimity
PL5   │   5+1  │   5/5+ext │   Full+Ext   │ External review required

Chain Types:
  Chain A: Static analysis
  Chain B: Dynamic analysis
  Chain C: Formal methods
  Chain D: Empirical testing
  Chain E: Expert review
  Chain F: External peer review (PL5 only)

═══════════════════════════════════════════════════════════════════════════════
```

---

## 6. Domain-Specific Precision Profiles

### 6.1 Default Precision by Domain

```yaml
domain_precision_defaults:
  T.SEC:
    default_level: PL3
    minimum_level: PL2
    rationale: "Security requires formal rigor"
    special_rules:
      - domain: "T.SEC.CRY.*"
        minimum_level: PL3
        recommended_level: PL4
      - domain: "T.SEC.OFF.*"
        minimum_level: PL2
        recommended_level: PL3

  T.DEV:
    default_level: PL2
    minimum_level: PL1
    rationale: "Standard development work"
    special_rules:
      - domain: "T.DEV.SYS.EMB"
        minimum_level: PL3
        recommended_level: PL4
        rationale: "Embedded systems safety"

  S.MED:
    default_level: PL3
    minimum_level: PL2
    rationale: "Medical safety requirements"
    special_rules:
      - domain: "S.MED.DIA.*"
        minimum_level: PL3
        rationale: "Diagnostic accuracy critical"
      - domain: "S.MED.SUR.*"
        minimum_level: PL3
        rationale: "Surgical safety"

  L.LEG:
    default_level: PL2
    minimum_level: PL2
    rationale: "Legal accuracy requirements"
    special_rules:
      - domain: "L.REG.*"
        minimum_level: PL3
        rationale: "Regulatory compliance"

  B:
    default_level: PL2
    minimum_level: PL1
    rationale: "Business decisions"
    special_rules:
      - domain: "B.FIN.TRD.*"
        minimum_level: PL3
        rationale: "Financial system criticality"

  E.ENG:
    default_level: PL2
    minimum_level: PL2
    rationale: "Engineering standards"
    special_rules:
      - domain: "E.ENG.AER.*"
        minimum_level: PL4
        rationale: "Aerospace safety"
      - domain: "E.ENG.NUC.*"
        minimum_level: PL4
        rationale: "Nuclear safety"
```

### 6.2 Precision Adjustment by Subdomain

```
PRECISION ADJUSTMENT MATRIX
═══════════════════════════════════════════════════════════════════════════════

When domain is X.Y.Z, apply:

  Base (X)     →  Default precision for category
  Subcategory (Y)  →  +/- adjustment based on specialization
  Specific (Z)     →  +/- adjustment based on application

Example: T.SEC.CRY.PQC (Post-Quantum Cryptography)

  T (Technology)        →  PL2 base
  SEC (Security)        →  +1 level (PL3)
  CRY (Cryptography)    →  +1 level (PL4)
  PQC (Post-Quantum)    →  +0 (already at practical max)

  Result: PL4 recommended

═══════════════════════════════════════════════════════════════════════════════
```

---

## 7. Precision Level Outputs

### 7.1 Output Requirements by Level

```yaml
output_requirements:
  PL1:
    mandatory:
      - "Executive summary"
      - "Major findings list"
      - "Preliminary recommendations"
      - "Confidence statement"
    optional:
      - "Detailed analysis"
      - "Supporting evidence"
    format: "Concise, action-oriented"

  PL2:
    mandatory:
      - "Comprehensive report"
      - "Categorized findings"
      - "Evidence documentation"
      - "Recommendations with rationale"
      - "Risk assessment"
      - "Confidence breakdown"
    optional:
      - "Formal models"
      - "Proof sketches"
    format: "Detailed, evidence-based"

  PL3:
    mandatory:
      - "Formal specification"
      - "Proof sketches for claims"
      - "Invariant documentation"
      - "Assumption register"
      - "Verification results"
      - "Uncertainty quantification"
    optional:
      - "Machine-checked proofs"
    format: "Rigorous, formally structured"

  PL4:
    mandatory:
      - "Machine-checked proofs"
      - "Formal verification logs"
      - "Certified specifications"
      - "Trusted computing base analysis"
      - "Complete assumption documentation"
    optional:
      - "Information-theoretic analysis"
    format: "Verified, mechanically checked"

  PL5:
    mandatory:
      - "Information-theoretic proofs"
      - "Security game definitions"
      - "Entropy calculations"
      - "Unconditional security statement"
      - "External review certification"
    format: "Publication-quality, peer-reviewed"
```

### 7.2 Confidence Reporting Format

```
CONFIDENCE REPORT FORMAT
═══════════════════════════════════════════════════════════════════════════════

PRECISION LEVEL: PL{n}
TARGET CONFIDENCE: {target}%
ACHIEVED CONFIDENCE: {achieved}%

CONFIDENCE BREAKDOWN:
┌─────────────────────────────────────────────────────────────────────────────┐
│ Component                        │ Confidence │ Method           │ Chain   │
├──────────────────────────────────┼────────────┼──────────────────┼─────────┤
│ [Component 1]                    │    XX%     │ [Method used]    │ A,B,C   │
│ [Component 2]                    │    XX%     │ [Method used]    │ A,C,D   │
│ ...                              │    ...     │ ...              │ ...     │
└─────────────────────────────────────────────────────────────────────────────┘

CHAIN AGREEMENT:
  Chain A (Static):    PASS/FAIL with confidence XX%
  Chain B (Dynamic):   PASS/FAIL with confidence XX%
  Chain C (Formal):    PASS/FAIL with confidence XX%
  Chain D (Empirical): PASS/FAIL with confidence XX%
  Chain E (Expert):    PASS/FAIL with confidence XX%

CONSENSUS: {chains_agreeing}/{chains_required}

RESIDUAL UNCERTAINTY:
  - [Uncertainty 1]: [Description] (Impact: HIGH/MEDIUM/LOW)
  - [Uncertainty 2]: [Description] (Impact: HIGH/MEDIUM/LOW)

ASSUMPTIONS:
  - [Assumption 1]: [Description] (Validated: YES/NO)
  - [Assumption 2]: [Description] (Validated: YES/NO)

═══════════════════════════════════════════════════════════════════════════════
```

---

## 8. Integration Points

### 8.1 Domain Taxonomy Integration

```
Domain Detection → Precision Default
  - Domain category provides base precision
  - Subdomains adjust precision
  - Task context modifies final level
```

### 8.2 Phase Templates Integration

```
Precision Level → Phase Adaptation
  - PL1-2: Condensed phases, relaxed gates
  - PL3: Standard phases, strict gates
  - PL4-5: Extended phases, formal verification added
```

### 8.3 Expert Archetypes Integration

```
Precision Level → Expert Configuration
  - Panel size scales with precision
  - Archetype ratios shift (more theoretical at higher levels)
  - Iteration depth increases with precision
```

---

## 9. Think Command Escalation (SKYNET Integration)

### 9.1 Think Command Mapping

```yaml
think_command_mapping:
  source: "SKYNET Integration - Anthropic Best Practices + PAL MCP ThinkDeep"
  purpose: "Map natural language think commands to precision levels"

  commands:
    think:
      precision_equivalent: "PL1-PL2"
      computational_effort: "Standard"
      use_case: "Quick analysis, straightforward problems"
      characteristics:
        - "Surface-level reasoning"
        - "Pattern matching"
        - "Heuristic application"
      typical_triggers:
        - "Simple questions"
        - "Familiar problem patterns"
        - "Time-pressured situations"

    think_hard:
      precision_equivalent: "PL2-PL3"
      computational_effort: "Increased"
      use_case: "Detailed analysis, moderately complex problems"
      characteristics:
        - "Deeper reasoning chains"
        - "Multiple perspective consideration"
        - "Evidence gathering"
      typical_triggers:
        - "Ambiguous requirements"
        - "Novel edge cases"
        - "Quality-critical outputs"

    think_harder:
      precision_equivalent: "PL3-PL4"
      computational_effort: "High"
      use_case: "Formal reasoning, complex analysis"
      characteristics:
        - "Formal method application"
        - "Proof sketch generation"
        - "Exhaustive case analysis"
      typical_triggers:
        - "Security-critical decisions"
        - "High-stakes recommendations"
        - "Contradictory evidence"

    ultrathink:
      precision_equivalent: "PL4-PL5"
      computational_effort: "Maximum"
      use_case: "Rigorous verification, highest assurance"
      characteristics:
        - "Machine-checkable reasoning"
        - "Information-theoretic analysis"
        - "Complete verification"
      typical_triggers:
        - "Cryptographic analysis"
        - "Safety-critical systems"
        - "Publication-quality rigor"

    thinkdeep:
      source: "PAL MCP Server"
      precision_equivalent: "PL3-PL4"
      computational_effort: "High + Extended"
      use_case: "Extended reasoning with edge case analysis"
      characteristics:
        - "Deep exploration of problem space"
        - "Systematic edge case identification"
        - "Comprehensive reasoning chains"
        - "Alternative hypothesis generation"
      typical_triggers:
        - "Complex debugging"
        - "Architecture decisions"
        - "Risk assessment"
```

### 9.2 Automatic Think Level Selection

```yaml
automatic_think_selection:
  principle: "Match computational effort to problem requirements"

  selection_algorithm:
    inputs:
      - task_complexity: "Assessed complexity score"
      - domain_criticality: "Domain-based minimum"
      - time_budget: "Available compute time"
      - user_signals: "Explicit user request"

    process:
      1: "Calculate base think level from precision level"
      2: "Apply domain criticality floor"
      3: "Adjust for time budget ceiling"
      4: "Apply user override if present"

  mapping_table:
    PL1: "think"
    PL2: "think / think_hard"
    PL3: "think_hard / think_harder"
    PL4: "think_harder / ultrathink"
    PL5: "ultrathink"

  escalation_triggers:
    - condition: "Confidence below target after initial analysis"
      action: "Escalate think level by 1"
    - condition: "Critical issue discovered"
      action: "Escalate to think_harder minimum"
    - condition: "Expert disagreement unresolved"
      action: "Escalate think level by 1"
```

### 9.3 Think Level Output Characteristics

```
THINK LEVEL OUTPUT MATRIX
═══════════════════════════════════════════════════════════════════════════════

Command        │ Reasoning │ Evidence  │ Alternatives │ Confidence │ Time
               │ Depth     │ Required  │ Considered   │ Range      │ Factor
───────────────┼───────────┼───────────┼──────────────┼────────────┼────────
think          │ Shallow   │ Optional  │ 1-2          │ 70-85%     │ 1x
think_hard     │ Moderate  │ Required  │ 2-3          │ 80-92%     │ 2-3x
think_harder   │ Deep      │ Extensive │ 3-5          │ 90-97%     │ 4-6x
ultrathink     │ Exhaustive│ Complete  │ All viable   │ 95-100%    │ 8-15x
thinkdeep      │ Deep+Wide │ Extensive │ 4-6 + edges  │ 92-98%     │ 5-8x

═══════════════════════════════════════════════════════════════════════════════
```

### 9.4 Think Command Feedback and Boundaries

```yaml
think_command_feedback:
  requirement: "System MUST report selected precision level after think command"
  format: "[Analyzing at PL{n}: {level_name}]"
  examples:
    - "[Analyzing at PL2: Operational]"
    - "[Analyzing at PL4: Rigorous]"

  boundary_clarification:
    think: "PL1-PL2 (caps at PL2)"
    think_hard: "PL2-PL3 (PL2 default, PL3 if complexity warrants)"
    think_harder: "PL3-PL4 (PL3 default, PL4 for high-stakes)"
    ultrathink: "PL4-PL5 (minimum PL4)"
    thinkdeep: "PL3 extended (depth over breadth, edge case focus)"
```

---

## Appendix A: Precision Level Quick Reference

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                     USF 4.0 PRECISION LEVEL QUICK REFERENCE                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  PL1 │ Overview        │ 80%  │ Heuristic        │ 2/3 chains │ Scoping    ║
║  PL2 │ Detailed        │ 90%  │ Behavioral       │ 3/4 chains │ Standard   ║
║  PL3 │ Formal          │ 95%  │ Proof Sketches   │ 4/5 chains │ High-Assur ║
║  PL4 │ Verified        │ 99%  │ Machine-Checked  │ 5/5 chains │ Certified  ║
║  PL5 │ IT-Guaranteed   │ 100% │ Info-Theoretic   │ 5/5+ext    │ Uncondit.  ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Calculation: PL = f(CS + DC + AE + VA - TC)                                 ║
║  Progressive deepening: Upgrade on trigger, carry forward results            ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## Appendix B: Change Log

| Version | Date | Changes |
|---------|------|---------|
| 4.0.0 | 2025-12-10 | Initial USF 4.0 precision levels specification |
| 4.1.0 | 2025-12-10 | SKYNET Integration: Added Section 9 - Think command escalation mapping (think, think_hard, think_harder, ultrathink, thinkdeep) |
| 4.1.1 | 2025-12-10 | Fixed HIGH-010: Added think command feedback requirements and boundary clarifications (9.4) |

---

*This document is part of the USF 4.0 specification suite. See MASTER-SPECIFICATION.md for framework overview.*
