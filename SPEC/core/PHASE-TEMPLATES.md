# USF 4.0: Phase Templates

> **Version**: 4.0.0
> **Component**: Core / Phase Templates
> **Status**: Specification
> **Dependencies**: DOMAIN-TAXONOMY.md, EXPERT-ARCHETYPES.md, MASTER-SPECIFICATION.md

---

## 1. Overview

USF 4.0 phase templates define structured execution workflows that adapt to domain requirements. Each template encodes:
- Phase sequence and dependencies
- Expert roles per phase
- Expected inputs and outputs
- Quality gates and transition criteria
- Iteration and convergence rules

```
PHASE TEMPLATE ARCHITECTURE
═══════════════════════════════════════════════════════════════════════════════

                         ┌──────────────────────┐
                         │   DOMAIN DETECTION   │
                         │   (DOMAIN-TAXONOMY)  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │    TEMPLATE SELECTION ENGINE  │
                    │                               │
                    │  ┌─────────┐  ┌─────────┐    │
                    │  │ Primary │  │Secondary│    │
                    │  │ Domain  │  │ Domains │    │
                    │  └────┬────┘  └────┬────┘    │
                    │       │            │         │
                    │       ▼            ▼         │
                    │  ┌─────────────────────┐     │
                    │  │  TEMPLATE FUSION    │     │
                    │  └─────────────────────┘     │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
               ┌────────────────────────────────────────┐
               │         ADAPTED PHASE SEQUENCE         │
               │                                        │
               │  Phase 1 ──► Phase 2 ──► ... ──► Phase N  │
               │     │           │                 │     │
               │     ▼           ▼                 ▼     │
               │  [Gate 1]   [Gate 2]         [Gate N]  │
               └────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════
```

---

## 2. Universal Phase Structure

All templates share a common meta-structure with domain-specific instantiation:

```
UNIVERSAL PHASE META-STRUCTURE
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 0: INITIALIZATION                                                      │
│ ──────────────────────                                                       │
│ • Domain detection and classification                                        │
│ • Template selection and adaptation                                          │
│ • Expert panel construction                                                  │
│ • Precision level calibration                                                │
│ • Resource allocation                                                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 1: ANALYSIS (Domain-Specific)                                          │
│ ───────────────────────────────────                                          │
│ • Comprehensive input examination                                            │
│ • Scope determination                                                        │
│ • Constraint identification                                                  │
│ • Success criteria definition                                                │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASES 2-N: CORE EXECUTION (Template-Specific)                               │
│ ──────────────────────────────────────────────                               │
│ • Domain-specific phase sequence                                             │
│ • Attack-Fix-Verify cycles as appropriate                                    │
│ • Quality gates between phases                                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE N+1: SYNTHESIS                                                         │
│ ────────────────────                                                         │
│ • Integration of all phase outputs                                           │
│ • Cross-validation of findings                                               │
│ • Confidence aggregation                                                     │
│ • Final deliverable construction                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE N+2: META-ANALYSIS                                                     │
│ ────────────────────────                                                     │
│ • Process quality assessment                                                 │
│ • Improvement identification                                                 │
│ • Template refinement proposals                                              │
│ • Knowledge extraction for future use                                        │
└─────────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════
```

---

## 3. Primary Phase Templates

### 3.1 SECURITY_ANALYSIS Template

**Domain Match**: T.SEC.* (Security domains)
**Archetype Weight**: Heavy adversarial (35%)

```yaml
template:
  id: TMPL-SEC
  name: "Security Analysis"
  version: "4.0.0"
  domain_match: "T.SEC.*"

  phases:
    - phase: 0
      name: "Initialization"
      duration_factor: 0.05
      activities:
        - "Threat model selection (STRIDE, PASTA, Attack Trees)"
        - "Adversary capability assessment"
        - "Asset criticality ranking"
        - "Security requirement extraction"
      outputs:
        - "Threat model framework"
        - "Adversary profiles"
        - "Asset inventory"
      gate:
        criteria: "All assets classified, threat model selected"
        confidence: 80%

    - phase: 1
      name: "Attack Surface Analysis"
      duration_factor: 0.15
      expert_focus:
        primary: [ARC-AD, ARC-IM]
        secondary: [ARC-TH]
      activities:
        - "Entry point enumeration"
        - "Trust boundary mapping"
        - "Data flow analysis"
        - "Component interaction mapping"
      outputs:
        - "Attack surface inventory"
        - "Trust boundary diagram"
        - "Data flow diagrams"
      gate:
        criteria: "Complete attack surface documented"
        confidence: 85%

    - phase: 2
      name: "Vulnerability Identification"
      duration_factor: 0.25
      expert_focus:
        primary: [ARC-AD]
        secondary: [ARC-TH, ARC-IM]
      activities:
        - "Known vulnerability mapping (CVE, CWE)"
        - "Implementation flaw analysis"
        - "Protocol weakness assessment"
        - "Cryptographic review"
        - "Side-channel analysis"
      outputs:
        - "Vulnerability catalog"
        - "Attack trees per vulnerability"
        - "Exploit feasibility assessment"
      iteration:
        type: "exhaustive"
        minimum_cycles: 3
        convergence: "No new HIGH/CRITICAL vulnerabilities for 2 cycles"
      gate:
        criteria: "All identified vulnerabilities documented with severity"
        confidence: 90%

    - phase: 3
      name: "Threat Scenario Construction"
      duration_factor: 0.15
      expert_focus:
        primary: [ARC-AD, ARC-ST]
        secondary: [ARC-TH]
      activities:
        - "Attack chain composition"
        - "Multi-stage attack scenarios"
        - "APT campaign modeling"
        - "Impact quantification"
      outputs:
        - "Threat scenarios (prioritized)"
        - "Attack chain diagrams"
        - "Impact assessments"
      gate:
        criteria: "All HIGH/CRITICAL vulnerabilities have exploit scenarios"
        confidence: 85%

    - phase: 4
      name: "Countermeasure Design"
      duration_factor: 0.20
      expert_focus:
        primary: [ARC-IM, ARC-ST]
        secondary: [ARC-TH, ARC-QA]
      activities:
        - "Mitigation strategy development"
        - "Defense-in-depth layering"
        - "Residual risk assessment"
        - "Implementation feasibility"
      outputs:
        - "Countermeasure recommendations"
        - "Implementation roadmap"
        - "Residual risk register"
      iteration:
        type: "adversarial_validation"
        process: "ARC-AD attempts to bypass proposed countermeasures"
        convergence: "No bypasses found for 2 cycles"
      gate:
        criteria: "All HIGH/CRITICAL risks have validated countermeasures"
        confidence: 90%

    - phase: 5
      name: "Verification & Synthesis"
      duration_factor: 0.15
      expert_focus:
        primary: [ARC-QA, ARC-TH]
        secondary: [ARC-AD]
      activities:
        - "Countermeasure verification"
        - "Coverage gap analysis"
        - "Formal verification (PL3+)"
        - "Final report construction"
      outputs:
        - "Security assessment report"
        - "Verified countermeasure list"
        - "Residual risk summary"
        - "Compliance mapping"
      gate:
        criteria: "All claims verified, report complete"
        confidence: 95%

    - phase: 6
      name: "Meta-Analysis"
      duration_factor: 0.05
      activities:
        - "Process effectiveness review"
        - "False positive/negative analysis"
        - "Template improvement proposals"
      outputs:
        - "Lessons learned"
        - "Template refinement suggestions"
```

---

### 3.2 DESIGN_REVIEW Template

**Domain Match**: T.DEV.*, E.ENG.* (Development, Engineering)
**Archetype Weight**: Heavy implementation (40%)

```yaml
template:
  id: TMPL-DSN
  name: "Design Review"
  version: "4.0.0"
  domain_match: ["T.DEV.*", "E.ENG.*"]

  phases:
    - phase: 0
      name: "Initialization"
      duration_factor: 0.05
      activities:
        - "Design document ingestion"
        - "Requirement extraction"
        - "Constraint identification"
        - "Review scope definition"
      outputs:
        - "Review scope document"
        - "Requirement checklist"
        - "Constraint catalog"
      gate:
        criteria: "All inputs processed, scope defined"
        confidence: 80%

    - phase: 1
      name: "Architectural Analysis"
      duration_factor: 0.20
      expert_focus:
        primary: [ARC-ST, ARC-IM]
        secondary: [ARC-TH]
      activities:
        - "Component decomposition"
        - "Interface analysis"
        - "Dependency mapping"
        - "Scalability assessment"
        - "Maintainability evaluation"
      outputs:
        - "Architecture diagram (validated)"
        - "Component catalog"
        - "Interface specifications"
        - "Dependency graph"
      gate:
        criteria: "Architecture fully documented and understood"
        confidence: 85%

    - phase: 2
      name: "Functional Correctness"
      duration_factor: 0.20
      expert_focus:
        primary: [ARC-TH, ARC-IM]
        secondary: [ARC-QA]
      activities:
        - "Requirement traceability"
        - "Logic verification"
        - "State machine analysis"
        - "Edge case identification"
        - "Error handling review"
      outputs:
        - "Traceability matrix"
        - "Logic verification report"
        - "State diagrams"
        - "Edge case catalog"
      iteration:
        type: "completeness_driven"
        convergence: "All requirements traced, no unhandled states"
      gate:
        criteria: "100% requirement coverage, all states handled"
        confidence: 90%

    - phase: 3
      name: "Quality Attributes"
      duration_factor: 0.15
      expert_focus:
        primary: [ARC-IM, ARC-QA]
        secondary: [ARC-ST]
      activities:
        - "Performance analysis"
        - "Reliability assessment"
        - "Security review (cross-reference TMPL-SEC)"
        - "Testability evaluation"
        - "Operability assessment"
      outputs:
        - "Quality attribute scores"
        - "Trade-off analysis"
        - "Risk register"
      gate:
        criteria: "All quality attributes assessed"
        confidence: 85%

    - phase: 4
      name: "Adversarial Challenge"
      duration_factor: 0.15
      expert_focus:
        primary: [ARC-AD]
        secondary: [ARC-TH, ARC-IM]
      activities:
        - "Failure mode identification"
        - "Attack vector analysis"
        - "Assumption challenging"
        - "Stress scenario construction"
      outputs:
        - "Failure mode catalog"
        - "Attack vector list"
        - "Challenged assumptions"
        - "Stress test recommendations"
      iteration:
        type: "adversarial"
        convergence: "No new critical issues for 2 cycles"
      gate:
        criteria: "All critical failure modes addressed"
        confidence: 90%

    - phase: 5
      name: "Recommendation Synthesis"
      duration_factor: 0.15
      expert_focus:
        primary: [ARC-ST, ARC-QA]
        secondary: [ARC-IM]
      activities:
        - "Issue prioritization"
        - "Recommendation formulation"
        - "Implementation guidance"
        - "Risk-benefit analysis"
      outputs:
        - "Prioritized issue list"
        - "Recommendations with rationale"
        - "Implementation roadmap"
        - "Risk-benefit summary"
      gate:
        criteria: "All issues have recommendations, priorities assigned"
        confidence: 90%

    - phase: 6
      name: "Final Report & Meta-Analysis"
      duration_factor: 0.10
      activities:
        - "Report compilation"
        - "Executive summary"
        - "Process review"
        - "Template improvement"
      outputs:
        - "Design review report"
        - "Executive summary"
        - "Process improvements"
```

---

### 3.3 SCIENTIFIC_RESEARCH Template

**Domain Match**: S.* (Science domains)
**Archetype Weight**: Heavy theoretical (40%)

```yaml
template:
  id: TMPL-SCI
  name: "Scientific Research"
  version: "4.0.0"
  domain_match: "S.*"

  phases:
    - phase: 0
      name: "Initialization"
      duration_factor: 0.05
      activities:
        - "Research question formalization"
        - "Hypothesis generation"
        - "Literature scope definition"
        - "Methodology selection"
      outputs:
        - "Formal research questions"
        - "Initial hypotheses"
        - "Search strategy"
      gate:
        criteria: "Clear research questions, testable hypotheses"
        confidence: 80%

    - phase: 1
      name: "Literature Review"
      duration_factor: 0.20
      expert_focus:
        primary: [ARC-TH]
        secondary: [ARC-ST, ARC-QA]
      activities:
        - "Systematic literature search"
        - "Source quality assessment"
        - "Knowledge synthesis"
        - "Gap identification"
        - "Theoretical framework construction"
      outputs:
        - "Literature synthesis"
        - "Knowledge gaps"
        - "Theoretical framework"
        - "Prior art summary"
      iteration:
        type: "exhaustive"
        convergence: "No new relevant sources for 2 iterations"
      gate:
        criteria: "Comprehensive literature coverage"
        confidence: 85%

    - phase: 2
      name: "Theoretical Development"
      duration_factor: 0.25
      expert_focus:
        primary: [ARC-TH]
        secondary: [ARC-AD, ARC-IM]
      activities:
        - "Theory construction"
        - "Model development"
        - "Mathematical formalization"
        - "Prediction generation"
        - "Falsifiability analysis"
      outputs:
        - "Theoretical model"
        - "Mathematical formulation"
        - "Testable predictions"
        - "Falsification criteria"
      iteration:
        type: "refinement"
        convergence: "Theory internally consistent, predictions specific"
      gate:
        criteria: "Coherent theory with falsifiable predictions"
        confidence: 90%

    - phase: 3
      name: "Methodological Design"
      duration_factor: 0.15
      expert_focus:
        primary: [ARC-IM, ARC-QA]
        secondary: [ARC-TH]
      activities:
        - "Experimental design"
        - "Variable operationalization"
        - "Control specification"
        - "Statistical power analysis"
        - "Bias mitigation"
      outputs:
        - "Research methodology"
        - "Experimental protocol"
        - "Analysis plan"
        - "Bias mitigation strategies"
      gate:
        criteria: "Rigorous methodology, adequate power"
        confidence: 85%

    - phase: 4
      name: "Critical Analysis"
      duration_factor: 0.15
      expert_focus:
        primary: [ARC-AD, ARC-TH]
        secondary: [ARC-QA]
      activities:
        - "Assumption challenging"
        - "Alternative explanation generation"
        - "Confound identification"
        - "Limitation analysis"
        - "Counter-argument construction"
      outputs:
        - "Challenged assumptions"
        - "Alternative explanations"
        - "Confound catalog"
        - "Limitation analysis"
      iteration:
        type: "adversarial"
        convergence: "All major objections addressed"
      gate:
        criteria: "Robust against known criticisms"
        confidence: 90%

    - phase: 5
      name: "Synthesis & Contribution"
      duration_factor: 0.15
      expert_focus:
        primary: [ARC-ST, ARC-TH]
        secondary: [ARC-QA]
      activities:
        - "Findings integration"
        - "Contribution articulation"
        - "Implications derivation"
        - "Future direction identification"
      outputs:
        - "Research synthesis"
        - "Contribution statement"
        - "Implications analysis"
        - "Future research agenda"
      gate:
        criteria: "Clear contribution, actionable implications"
        confidence: 90%

    - phase: 6
      name: "Meta-Analysis"
      duration_factor: 0.05
      activities:
        - "Research quality assessment"
        - "Methodology review"
        - "Template improvement"
      outputs:
        - "Quality assessment"
        - "Methodology lessons"
```

---

### 3.4 LEGAL_ANALYSIS Template

**Domain Match**: L.* (Legal domains)
**Archetype Weight**: Balanced theoretical/adversarial (25%/25%)

```yaml
template:
  id: TMPL-LEG
  name: "Legal Analysis"
  version: "4.0.0"
  domain_match: "L.*"

  phases:
    - phase: 0
      name: "Initialization"
      duration_factor: 0.05
      activities:
        - "Legal issue identification"
        - "Jurisdiction determination"
        - "Applicable law identification"
        - "Stakeholder mapping"
      outputs:
        - "Issue statement"
        - "Jurisdictional analysis"
        - "Applicable law list"
      gate:
        criteria: "Issues clear, jurisdiction established"
        confidence: 80%

    - phase: 1
      name: "Statutory & Regulatory Review"
      duration_factor: 0.20
      expert_focus:
        primary: [ARC-TH]
        secondary: [ARC-QA]
      activities:
        - "Statute identification"
        - "Regulatory framework mapping"
        - "Legislative history review"
        - "Regulatory guidance analysis"
      outputs:
        - "Applicable statutes"
        - "Regulatory framework"
        - "Legislative intent analysis"
      gate:
        criteria: "All relevant law identified"
        confidence: 85%

    - phase: 2
      name: "Case Law Analysis"
      duration_factor: 0.20
      expert_focus:
        primary: [ARC-TH, ARC-AD]
        secondary: [ARC-ST]
      activities:
        - "Precedent research"
        - "Case synthesis"
        - "Distinguishing analysis"
        - "Trend identification"
      outputs:
        - "Relevant precedents"
        - "Case synthesis"
        - "Distinguishing factors"
        - "Legal trend analysis"
      iteration:
        type: "exhaustive"
        convergence: "No new binding precedents"
      gate:
        criteria: "Comprehensive precedent review"
        confidence: 90%

    - phase: 3
      name: "Argument Construction"
      duration_factor: 0.20
      expert_focus:
        primary: [ARC-TH, ARC-ST]
        secondary: [ARC-IM]
      activities:
        - "Legal argument formulation"
        - "Element analysis"
        - "Evidence mapping"
        - "Remedy identification"
      outputs:
        - "Legal arguments"
        - "Element-by-element analysis"
        - "Evidence requirements"
        - "Available remedies"
      gate:
        criteria: "All arguments supported by authority"
        confidence: 85%

    - phase: 4
      name: "Counter-Argument Analysis"
      duration_factor: 0.15
      expert_focus:
        primary: [ARC-AD]
        secondary: [ARC-TH]
      activities:
        - "Opposing argument anticipation"
        - "Weakness identification"
        - "Rebuttal preparation"
        - "Risk assessment"
      outputs:
        - "Anticipated counter-arguments"
        - "Argument weaknesses"
        - "Rebuttals"
        - "Litigation risk assessment"
      iteration:
        type: "adversarial"
        convergence: "All major counter-arguments addressed"
      gate:
        criteria: "Robust against opposition"
        confidence: 90%

    - phase: 5
      name: "Recommendation & Synthesis"
      duration_factor: 0.15
      expert_focus:
        primary: [ARC-ST, ARC-QA]
        secondary: [ARC-IM]
      activities:
        - "Legal opinion formulation"
        - "Risk-benefit analysis"
        - "Strategic recommendation"
        - "Compliance pathway"
      outputs:
        - "Legal opinion"
        - "Risk assessment"
        - "Strategic recommendations"
        - "Compliance roadmap"
      gate:
        criteria: "Clear opinion with supporting analysis"
        confidence: 90%

    - phase: 6
      name: "Meta-Analysis"
      duration_factor: 0.05
      activities:
        - "Analysis quality review"
        - "Template improvement"
      outputs:
        - "Quality assessment"
        - "Lessons learned"
```

---

### 3.5 BUSINESS_STRATEGY Template

**Domain Match**: B.* (Business domains)
**Archetype Weight**: Heavy strategic (35%)

```yaml
template:
  id: TMPL-BUS
  name: "Business Strategy"
  version: "4.0.0"
  domain_match: "B.*"

  phases:
    - phase: 0
      name: "Initialization"
      duration_factor: 0.05
      activities:
        - "Strategic question formalization"
        - "Stakeholder identification"
        - "Constraint mapping"
        - "Success criteria definition"
      outputs:
        - "Strategic questions"
        - "Stakeholder map"
        - "Constraints"
        - "Success metrics"
      gate:
        criteria: "Clear strategic scope"
        confidence: 80%

    - phase: 1
      name: "Situational Analysis"
      duration_factor: 0.20
      expert_focus:
        primary: [ARC-TH, ARC-ST]
        secondary: [ARC-AD]
      activities:
        - "Market analysis"
        - "Competitive landscape"
        - "Internal capability assessment"
        - "SWOT/PESTEL analysis"
        - "Industry dynamics"
      outputs:
        - "Market analysis"
        - "Competitive map"
        - "Capability assessment"
        - "SWOT matrix"
      gate:
        criteria: "Comprehensive situational understanding"
        confidence: 85%

    - phase: 2
      name: "Option Generation"
      duration_factor: 0.20
      expert_focus:
        primary: [ARC-ST, ARC-IM]
        secondary: [ARC-TH]
      activities:
        - "Strategic option brainstorming"
        - "Scenario planning"
        - "Innovation opportunity identification"
        - "Partnership/M&A options"
      outputs:
        - "Strategic options"
        - "Scenario analyses"
        - "Innovation roadmap"
        - "Partnership opportunities"
      iteration:
        type: "generative"
        convergence: "Diminishing novel options"
      gate:
        criteria: "Multiple viable options identified"
        confidence: 85%

    - phase: 3
      name: "Option Evaluation"
      duration_factor: 0.20
      expert_focus:
        primary: [ARC-TH, ARC-QA]
        secondary: [ARC-AD, ARC-IM]
      activities:
        - "Financial modeling"
        - "Risk assessment"
        - "Capability gap analysis"
        - "Execution feasibility"
        - "Stakeholder impact"
      outputs:
        - "Financial projections"
        - "Risk register"
        - "Capability requirements"
        - "Execution assessment"
      gate:
        criteria: "All options quantitatively evaluated"
        confidence: 90%

    - phase: 4
      name: "Stress Testing"
      duration_factor: 0.15
      expert_focus:
        primary: [ARC-AD]
        secondary: [ARC-TH, ARC-ST]
      activities:
        - "Assumption challenging"
        - "Downside scenario analysis"
        - "Competitive response modeling"
        - "Black swan identification"
      outputs:
        - "Challenged assumptions"
        - "Downside scenarios"
        - "Competitive responses"
        - "Contingency triggers"
      iteration:
        type: "adversarial"
        convergence: "Strategy robust under stress"
      gate:
        criteria: "Strategy survives stress testing"
        confidence: 90%

    - phase: 5
      name: "Recommendation & Roadmap"
      duration_factor: 0.15
      expert_focus:
        primary: [ARC-ST, ARC-IM]
        secondary: [ARC-QA]
      activities:
        - "Option selection rationale"
        - "Implementation roadmap"
        - "Resource allocation"
        - "KPI definition"
        - "Governance structure"
      outputs:
        - "Strategic recommendation"
        - "Implementation plan"
        - "Resource requirements"
        - "KPI framework"
        - "Governance model"
      gate:
        criteria: "Actionable recommendation with roadmap"
        confidence: 90%

    - phase: 6
      name: "Meta-Analysis"
      duration_factor: 0.05
      activities:
        - "Analysis quality review"
        - "Process improvement"
      outputs:
        - "Quality assessment"
        - "Template refinements"
```

---

## 4. Template Composition Rules

### 4.1 Template Selection Algorithm

```
TEMPLATE SELECTION ALGORITHM
═══════════════════════════════════════════════════════════════════════════════

INPUT: DomainProfile from DOMAIN-TAXONOMY.md

PROCESS:

Step 1: Primary Template Match
  FOR EACH template IN [TMPL-SEC, TMPL-DSN, TMPL-SCI, TMPL-LEG, TMPL-BUS]:
    IF domain_profile.primary MATCHES template.domain_match:
      primary_template = template
      BREAK

Step 2: Secondary Template Identification
  secondary_templates = []
  FOR EACH secondary_domain IN domain_profile.secondary:
    FOR EACH template IN templates:
      IF secondary_domain MATCHES template.domain_match:
        secondary_templates.append(template)

Step 3: Template Fusion
  IF len(secondary_templates) > 0:
    fused_template = fuse_templates(primary_template, secondary_templates)
  ELSE:
    fused_template = primary_template

Step 4: Precision Adaptation
  adapted_template = adapt_to_precision(fused_template, precision_level)

OUTPUT: adapted_template

═══════════════════════════════════════════════════════════════════════════════
```

### 4.2 Template Fusion Protocol

When multiple templates apply, merge using these rules:

```yaml
fusion_rules:
  phase_merging:
    rule: "Union of phases, merge overlapping phases"
    priority: "Primary template phase order takes precedence"
    conflict_resolution: "Longer duration wins for overlapping phases"

  expert_merging:
    rule: "Combine expert requirements, adjust ratios proportionally"
    constraint: "Total must still meet panel size limits"

  gate_merging:
    rule: "Intersection of gate criteria (must pass all)"
    confidence: "Take maximum confidence requirement"

  iteration_merging:
    rule: "Union of iteration types"
    convergence: "All convergence criteria must be met"
```

**Fusion Example**:

```
Primary: TMPL-SEC (Security Analysis)
Secondary: TMPL-DSN (Design Review)

Fused Template:
  - Phase 1: Attack Surface Analysis + Architectural Analysis
  - Phase 2: Vulnerability Identification (SEC primary)
  - Phase 3: Functional Correctness (DSN addition)
  - Phase 4: Threat Scenario Construction + Adversarial Challenge
  - Phase 5: Countermeasure Design + Quality Attributes
  - Phase 6: Verification & Synthesis
  - Phase 7: Meta-Analysis

Expert Ratios (adjusted):
  ARC-AD: 30% (weighted from SEC 35%, DSN 15%)
  ARC-IM: 28% (weighted from SEC 20%, DSN 40%)
  ARC-TH: 17% (weighted from SEC 15%, DSN 20%)
  ARC-ST: 15% (weighted from SEC 15%, DSN 15%)
  ARC-QA: 10% (weighted from SEC 15%, DSN 10%)
```

---

## 5. Phase Execution Protocols

### 5.1 Phase Entry Protocol

```
PHASE ENTRY PROTOCOL
═══════════════════════════════════════════════════════════════════════════════

PRE-ENTRY CHECKLIST:
  □ Previous phase gate passed
  □ Required inputs available
  □ Expert panel ready for phase
  □ Resources allocated
  □ Success criteria understood

ENTRY ACTIONS:
  1. Announce phase transition to all experts
  2. Distribute phase-specific context
  3. Set iteration counter = 0
  4. Initialize phase outputs structure
  5. Begin first expert round

═══════════════════════════════════════════════════════════════════════════════
```

### 5.2 Phase Iteration Protocol

```
PHASE ITERATION PROTOCOL
═══════════════════════════════════════════════════════════════════════════════

ITERATION LOOP:
  WHILE NOT converged AND iteration < max_iterations:

    // Expert Round
    FOR EACH expert IN phase.active_experts:
      contribution = expert.analyze(context, previous_contributions)
      contributions.append(contribution)

    // Synthesis Round
    synthesis = synthesizer.integrate(contributions)

    // Convergence Check
    IF iteration_type == "adversarial":
      converged = no_new_critical_issues(synthesis, previous_synthesis)
    ELIF iteration_type == "exhaustive":
      converged = no_new_findings(synthesis, previous_synthesis)
    ELIF iteration_type == "refinement":
      converged = quality_threshold_met(synthesis)
    ELIF iteration_type == "generative":
      converged = diminishing_novelty(synthesis, previous_synthesis)

    iteration += 1
    previous_synthesis = synthesis

OUTPUT: Final synthesis for phase

═══════════════════════════════════════════════════════════════════════════════
```

### 5.3 Phase Gate Protocol

```
PHASE GATE PROTOCOL
═══════════════════════════════════════════════════════════════════════════════

GATE EVALUATION:
  1. Collect all phase outputs
  2. Evaluate against gate criteria:
     - Completeness: All required outputs present
     - Quality: Outputs meet quality standards
     - Confidence: Aggregated confidence >= threshold
     - Coverage: No identified gaps

GATE OUTCOMES:
  PASS:
    - Record gate passage with timestamp
    - Proceed to next phase
    - Archive phase outputs

  CONDITIONAL_PASS:
    - Proceed with documented caveats
    - Flag for meta-analysis review
    - May require follow-up

  FAIL:
    - Identify specific deficiencies
    - Return to phase with guidance
    - Increment retry counter
    - IF retries > max_retries: Escalate to meta-analysis

═══════════════════════════════════════════════════════════════════════════════
```

---

## 6. Custom Template Definition

### 6.1 Template Definition Schema

```yaml
template_schema:
  id: "TMPL-XXX"
  name: "Template Name"
  version: "4.0.0"
  domain_match: "Domain pattern or list"

  metadata:
    author: "Author name"
    created: "Date"
    purpose: "Template purpose description"

  phases:
    - phase: N
      name: "Phase Name"
      duration_factor: 0.XX  # Proportion of total effort
      expert_focus:
        primary: [ARC-*]     # Lead archetypes
        secondary: [ARC-*]   # Supporting archetypes
      activities:
        - "Activity description"
      outputs:
        - "Output description"
      iteration:
        type: "exhaustive|adversarial|refinement|generative"
        minimum_cycles: N
        convergence: "Convergence criteria"
      gate:
        criteria: "Gate criteria"
        confidence: XX%

  customization_points:
    - point: "Name"
      description: "What can be customized"
      constraints: "Customization constraints"
```

### 6.2 Template Inheritance

Templates can extend existing templates:

```yaml
template:
  id: "TMPL-SEC-PQC"
  name: "Post-Quantum Cryptography Security Analysis"
  extends: "TMPL-SEC"
  version: "4.0.0"
  domain_match: "T.SEC.CRY.PQC"

  overrides:
    phases:
      - phase: 2  # Vulnerability Identification
        activities:
          - ADD: "Lattice-based cryptanalysis"
          - ADD: "Grover/Shor algorithm applicability"
          - ADD: "Side-channel analysis (post-quantum specific)"
        expert_focus:
          primary: [ARC-AD, ARC-TH]  # Increase theoretical

      - phase: 4  # Countermeasure Design
        activities:
          - ADD: "Hybrid classical/PQC scheme design"
          - ADD: "Migration strategy development"

  additions:
    phases:
      - phase: 2.5  # New phase after Vulnerability Identification
        name: "Quantum Threat Assessment"
        duration_factor: 0.10
        activities:
          - "Quantum computer timeline analysis"
          - "Harvest-now-decrypt-later risk assessment"
          - "Algorithm agility requirements"
```

---

## 7. Template Library Index

### 7.1 Primary Templates

| ID | Name | Domain Match | Key Characteristic |
|----|------|--------------|-------------------|
| TMPL-SEC | Security Analysis | T.SEC.* | Heavy adversarial |
| TMPL-DSN | Design Review | T.DEV.*, E.ENG.* | Heavy implementation |
| TMPL-SCI | Scientific Research | S.* | Heavy theoretical |
| TMPL-LEG | Legal Analysis | L.* | Balanced TH/AD |
| TMPL-BUS | Business Strategy | B.* | Heavy strategic |

### 7.2 Specialized Templates (Derived)

| ID | Name | Extends | Domain Match |
|----|------|---------|--------------|
| TMPL-SEC-PQC | PQ Crypto Analysis | TMPL-SEC | T.SEC.CRY.PQC |
| TMPL-SEC-PRO | Protocol Analysis | TMPL-SEC | T.SEC.PRO.* |
| TMPL-SEC-APT | APT Campaign Analysis | TMPL-SEC | T.SEC.OFF.APT |
| TMPL-DSN-DIS | Distributed Systems | TMPL-DSN | T.DEV.SYS.DIS |
| TMPL-SCI-EXP | Experimental Design | TMPL-SCI | S.*.EXP |
| TMPL-BUS-MA | M&A Due Diligence | TMPL-BUS | B.FIN.*, B.STR.* |

### 7.3 Cross-Domain Templates

| ID | Name | Primary | Secondary |
|----|------|---------|-----------|
| TMPL-X-SECBUS | Security Business Case | TMPL-SEC | TMPL-BUS |
| TMPL-X-LEGTECH | Legal Tech Review | TMPL-LEG | TMPL-DSN |
| TMPL-X-SCIBUS | R&D Strategy | TMPL-SCI | TMPL-BUS |

---

## 8. Template Evolution

### 8.1 Template Versioning

```yaml
versioning:
  format: "MAJOR.MINOR.PATCH"

  major_change:
    - "Phase structure change"
    - "Gate criteria fundamental change"
    - "Expert balance significant shift"

  minor_change:
    - "Activity additions"
    - "Output refinements"
    - "Iteration tuning"

  patch_change:
    - "Wording clarifications"
    - "Confidence threshold adjustments"
    - "Duration factor tuning"
```

### 8.2 Template Improvement Pipeline

```
TEMPLATE IMPROVEMENT PIPELINE
═══════════════════════════════════════════════════════════════════════════════

SOURCES OF IMPROVEMENT:
  1. Meta-analysis outputs from template executions
  2. User feedback on template effectiveness
  3. Cross-template pattern analysis
  4. Domain evolution (new threats, methods, standards)

IMPROVEMENT PROCESS:
  1. Collect improvement signals
  2. Categorize by impact (major/minor/patch)
  3. Draft template modification
  4. Validate against historical cases
  5. A/B test new version
  6. Graduate to production if improved

VALIDATION CRITERIA:
  - No regression in gate passage rates
  - Improved output quality scores
  - Reduced iteration counts for convergence
  - Positive expert feedback

═══════════════════════════════════════════════════════════════════════════════
```

---

## 9. Integration Points

### 9.1 Domain Taxonomy Integration

```
Domain Detection → Template Selection
  - Primary domain determines primary template
  - Secondary domains add template elements
  - Domain confidence affects template adaptation
```

### 9.2 Expert Archetypes Integration

```
Template Phases → Expert Assignment
  - Phase expert_focus maps to archetype synthesis
  - Phase activities inform expert persona calibration
  - Phase outputs guide expert communication format
```

### 9.3 Precision Levels Integration

```
Precision Level → Template Adaptation
  - PL1-2: Condensed phases, relaxed gates
  - PL3-4: Full phases, standard gates
  - PL5: Extended phases, rigorous gates, formal verification
```

---

## Appendix A: Template Quick Reference

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                       USF 4.0 TEMPLATE QUICK REFERENCE                       ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  TMPL-SEC │ Security Analysis    │ T.SEC.* │ Attack→Vuln→Threat→Counter     ║
║  TMPL-DSN │ Design Review        │ T.DEV.* │ Arch→Correct→Quality→Challenge ║
║  TMPL-SCI │ Scientific Research  │ S.*     │ Lit→Theory→Method→Critique     ║
║  TMPL-LEG │ Legal Analysis       │ L.*     │ Statute→Case→Argue→Counter     ║
║  TMPL-BUS │ Business Strategy    │ B.*     │ Situation→Options→Eval→Stress  ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  All templates: Phase 0 (Init) + Core Phases + Synthesis + Meta-Analysis     ║
║  Gates between all phases, iteration within phases                           ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## Appendix B: Change Log

| Version | Date | Changes |
|---------|------|---------|
| 4.0.0 | 2025-12-10 | Initial USF 4.0 phase template specification |

---

*This document is part of the USF 4.0 specification suite. See MASTER-SPECIFICATION.md for framework overview.*
