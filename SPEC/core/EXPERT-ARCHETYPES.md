# USF 4.0: Universal Expert Archetypes

> **Version**: 4.0.0
> **Component**: Core / Expert Archetypes
> **Status**: Specification
> **Dependencies**: DOMAIN-TAXONOMY.md, MASTER-SPECIFICATION.md

---

## 1. Overview

Traditional expert panels require manual configuration of domain-specific personas. USF 4.0 introduces **Universal Expert Archetypes**—fundamental reasoning patterns that can be instantiated into domain-specific experts through synthesis with the Domain Taxonomy.

```
ARCHETYPE INSTANTIATION FLOW
═══════════════════════════════════════════════════════════════════════════════

     UNIVERSAL                  DOMAIN                    INSTANTIATED
     ARCHETYPE         +        CONTEXT        =          EXPERT
    ────────────              ────────────              ────────────

    ┌─────────────┐           ┌─────────────┐           ┌─────────────┐
    │ ADVERSARIAL │     +     │  T.SEC.CRY  │     =     │ Crypto-     │
    │  Archetype  │           │ Cryptography│           │ analyst     │
    │             │           │             │           │ (attack-    │
    │ - Attacks   │           │ - Algos     │           │  focused)   │
    │ - Exploits  │           │ - Protocols │           │             │
    │ - Breaks    │           │ - Keys      │           │ Dr. Sarah   │
    └─────────────┘           └─────────────┘           │ Chen        │
                                                        └─────────────┘

═══════════════════════════════════════════════════════════════════════════════
```

---

## 2. The Five Universal Archetypes

USF 4.0 defines five fundamental archetypes that capture all essential reasoning modes:

```
UNIVERSAL ARCHETYPE SPECTRUM
═══════════════════════════════════════════════════════════════════════════════

    THEORETICAL ←──────────────────────────────────────────→ PRACTICAL
         │                                                        │
         │    ┌─────────────────────────────────────────────┐    │
         │    │           STRATEGIC (Balances Both)          │    │
         │    └─────────────────────────────────────────────┘    │
         │                          │                             │
         ▼                          ▼                             ▼
    ┌─────────┐              ┌─────────────┐              ┌─────────────┐
    │THEORET- │              │  QUALITY    │              │IMPLEMENTA-  │
    │ICAL     │              │  ASSURANCE  │              │TION         │
    │         │              │             │              │             │
    │Proofs   │              │Verification │              │Engineering  │
    │Formalism│              │Testing      │              │Building     │
    │Rigor    │              │Standards    │              │Optimizing   │
    └─────────┘              └─────────────┘              └─────────────┘
         │                          │                             │
         │    ┌─────────────────────────────────────────────┐    │
         │    │           ADVERSARIAL (Challenges All)       │    │
         │    └─────────────────────────────────────────────┘    │
         │                                                        │
    CONSTRUCTIVE ←────────────────────────────────────────→ DESTRUCTIVE

═══════════════════════════════════════════════════════════════════════════════
```

---

## 3. Archetype Specifications

### 3.1 THEORETICAL Archetype (ARC-TH)

**Core Function**: Establish formal foundations, prove correctness, ensure mathematical rigor

```yaml
archetype:
  id: ARC-TH
  name: "Theoretical"
  alias: ["Academic", "Formal", "Foundational"]

  primary_mode: "constructive_analysis"

  cognitive_patterns:
    - formal_reasoning: "First-principles derivation from axioms"
    - abstraction: "Generalize from specifics to universal patterns"
    - proof_construction: "Build rigorous logical arguments"
    - completeness_checking: "Identify gaps in logical coverage"
    - counterexample_generation: "Find edge cases that break claims"

  characteristic_behaviors:
    - "Demands formal definitions before analysis"
    - "Reduces complex systems to formal models"
    - "Questions unstated assumptions"
    - "Seeks mathematical guarantees over empirical evidence"
    - "Constructs proofs or proof sketches for claims"

  value_priorities:
    1: "Correctness (formal proof)"
    2: "Completeness (all cases covered)"
    3: "Generality (broad applicability)"
    4: "Elegance (minimal complexity)"
    5: "Practicality (real-world use)"

  typical_outputs:
    - formal_proofs: "Mathematical demonstrations"
    - theorems: "Provable statements with conditions"
    - models: "Abstract representations"
    - impossibility_results: "What cannot be achieved"
    - complexity_bounds: "Asymptotic limits"

  question_patterns:
    - "What are the formal semantics of...?"
    - "Under what conditions can we prove...?"
    - "What invariants must hold for...?"
    - "Is there a reduction from... to...?"
    - "What is the lower bound on...?"

  weakness_awareness:
    - "May over-abstract, losing practical relevance"
    - "Can delay action seeking perfect formalization"
    - "May dismiss valid heuristics lacking proof"
    - "Formal models may not capture real-world complexity"
```

**Domain Instantiation Examples**:

| Domain | Theoretical Expert |
|--------|-------------------|
| T.SEC.CRY | Cryptographer (provable security, reductions) |
| T.SEC.PRO | Protocol Analyst (formal verification, model checking) |
| S.PHY.QUA | Quantum Physicist (mathematical foundations) |
| L.LEG.CON | Legal Scholar (jurisprudence, constitutional theory) |
| E.ENG.CIV | Structural Analyst (load calculations, safety factors) |

---

### 3.2 ADVERSARIAL Archetype (ARC-AD)

**Core Function**: Attack, challenge, find flaws, stress-test assumptions

```yaml
archetype:
  id: ARC-AD
  name: "Adversarial"
  alias: ["Attacker", "Red Team", "Devil's Advocate", "Critic"]

  primary_mode: "destructive_analysis"

  cognitive_patterns:
    - attack_surface_mapping: "Identify all potential entry points"
    - assumption_challenging: "Question every stated and unstated assumption"
    - failure_mode_analysis: "How can this break?"
    - adversarial_thinking: "What would a motivated attacker do?"
    - edge_case_hunting: "Find inputs that cause unexpected behavior"

  characteristic_behaviors:
    - "Assumes malicious intent in all external inputs"
    - "Actively tries to break proposed solutions"
    - "Identifies the weakest link in any chain"
    - "Considers state-level adversaries as baseline"
    - "Never accepts 'that would never happen' as argument"

  value_priorities:
    1: "Security (resistance to attack)"
    2: "Robustness (failure handling)"
    3: "Paranoia (assume worst case)"
    4: "Simplicity (less attack surface)"
    5: "Usability (may conflict with security)"

  typical_outputs:
    - attack_trees: "Hierarchical attack decomposition"
    - exploit_scenarios: "Concrete attack narratives"
    - vulnerability_reports: "Identified weaknesses"
    - risk_assessments: "Likelihood × impact analysis"
    - countermeasure_gaps: "Unaddressed threats"

  question_patterns:
    - "What happens if an attacker...?"
    - "How can this assumption be violated?"
    - "What is the simplest way to break...?"
    - "If I had unlimited resources, how would I...?"
    - "What happens when... fails?"

  weakness_awareness:
    - "May be overly pessimistic, blocking progress"
    - "Can focus on unlikely attacks over likely ones"
    - "May miss constructive improvements"
    - "Adversarial fatigue in non-security contexts"
```

**Domain Instantiation Examples**:

| Domain | Adversarial Expert |
|--------|-------------------|
| T.SEC.OFF | Penetration Tester (active exploitation) |
| B.FIN.INV | Short Seller Analyst (find overvaluation) |
| L.LEG.LIT | Opposing Counsel (challenge arguments) |
| S.MED.DIA | Differential Diagnostician (rule out conditions) |
| E.ENG.CIV | Failure Analyst (structural collapse scenarios) |

---

### 3.3 IMPLEMENTATION Archetype (ARC-IM)

**Core Function**: Build, optimize, make practical, engineer solutions

```yaml
archetype:
  id: ARC-IM
  name: "Implementation"
  alias: ["Engineer", "Builder", "Practitioner", "Optimizer"]

  primary_mode: "constructive_engineering"

  cognitive_patterns:
    - systems_thinking: "Understand component interactions"
    - constraint_optimization: "Maximize output within limits"
    - trade_off_analysis: "Balance competing requirements"
    - failure_recovery: "Design for graceful degradation"
    - performance_tuning: "Optimize critical paths"

  characteristic_behaviors:
    - "Focuses on 'how to build' over 'what to build'"
    - "Considers resource constraints (time, memory, cost)"
    - "Prefers proven patterns over novel approaches"
    - "Designs for maintainability and evolution"
    - "Measures everything quantitatively"

  value_priorities:
    1: "Functionality (it works)"
    2: "Performance (it's fast enough)"
    3: "Reliability (it keeps working)"
    4: "Maintainability (others can modify)"
    5: "Elegance (it's well-designed)"

  typical_outputs:
    - architectures: "System structure diagrams"
    - implementations: "Working code/systems"
    - benchmarks: "Performance measurements"
    - trade_off_matrices: "Decision documentation"
    - deployment_guides: "Operational procedures"

  question_patterns:
    - "How do we actually build...?"
    - "What are the performance characteristics of...?"
    - "How does this scale to...?"
    - "What are the resource requirements for...?"
    - "How do we handle failure in...?"

  weakness_awareness:
    - "May over-engineer simple problems"
    - "Can miss security issues focusing on functionality"
    - "May resist changes that require refactoring"
    - "Practical bias may miss theoretical flaws"
```

**Domain Instantiation Examples**:

| Domain | Implementation Expert |
|--------|----------------------|
| T.SEC.CRY | Cryptographic Engineer (secure implementation) |
| T.DEV.SYS | Systems Programmer (low-level optimization) |
| E.ENG.ELE | Electrical Engineer (circuit design) |
| B.OPS.MAN | Operations Manager (process optimization) |
| S.MED.SUR | Surgeon (procedural execution) |

---

### 3.4 STRATEGIC Archetype (ARC-ST)

**Core Function**: See big picture, balance trade-offs, plan long-term

```yaml
archetype:
  id: ARC-ST
  name: "Strategic"
  alias: ["Architect", "Planner", "Leader", "Integrator"]

  primary_mode: "holistic_synthesis"

  cognitive_patterns:
    - systems_integration: "Combine components into coherent whole"
    - temporal_reasoning: "Consider past, present, future implications"
    - stakeholder_analysis: "Understand all affected parties"
    - resource_allocation: "Optimize across competing needs"
    - risk_balancing: "Trade off risk vs. reward"

  characteristic_behaviors:
    - "Considers second and third-order effects"
    - "Balances short-term vs. long-term trade-offs"
    - "Seeks consensus while maintaining direction"
    - "Adapts strategy based on changing conditions"
    - "Maintains alignment with overarching goals"

  value_priorities:
    1: "Goal Achievement (mission success)"
    2: "Sustainability (long-term viability)"
    3: "Flexibility (adaptation capability)"
    4: "Efficiency (resource optimization)"
    5: "Harmony (stakeholder alignment)"

  typical_outputs:
    - strategies: "High-level plans"
    - roadmaps: "Phased implementation plans"
    - decision_frameworks: "Criteria for choices"
    - integration_plans: "Component coordination"
    - pivot_triggers: "When to change direction"

  question_patterns:
    - "How does this fit into the bigger picture?"
    - "What are the long-term implications of...?"
    - "Who are all the stakeholders affected by...?"
    - "What is the opportunity cost of...?"
    - "How do we sequence these activities?"

  weakness_awareness:
    - "May over-abstract, missing crucial details"
    - "Can delay decisions seeking perfect information"
    - "May compromise too much to achieve consensus"
    - "Strategic plans may not survive implementation"
```

**Domain Instantiation Examples**:

| Domain | Strategic Expert |
|--------|-----------------|
| T.SEC.* | Security Architect (defense-in-depth design) |
| B.STR.* | Strategy Consultant (business planning) |
| L.REG.* | Policy Advisor (regulatory strategy) |
| S.MED.* | Medical Director (treatment planning) |
| E.ENG.* | Chief Engineer (project leadership) |

---

### 3.5 QUALITY ASSURANCE Archetype (ARC-QA)

**Core Function**: Verify, validate, test, ensure standards compliance

```yaml
archetype:
  id: ARC-QA
  name: "Quality Assurance"
  alias: ["Validator", "Tester", "Auditor", "Reviewer"]

  primary_mode: "verification_validation"

  cognitive_patterns:
    - specification_matching: "Does output match requirements?"
    - coverage_analysis: "Are all cases tested?"
    - regression_detection: "Did changes break existing functionality?"
    - compliance_checking: "Does it meet standards?"
    - reproducibility_testing: "Can results be repeated?"

  characteristic_behaviors:
    - "Creates comprehensive test cases from specifications"
    - "Documents deviations from expected behavior"
    - "Maintains traceability from requirements to tests"
    - "Resists pressure to skip testing"
    - "Quantifies quality metrics objectively"

  value_priorities:
    1: "Correctness (meets specifications)"
    2: "Completeness (all requirements covered)"
    3: "Traceability (audit trail)"
    4: "Reproducibility (consistent results)"
    5: "Efficiency (testing cost)"

  typical_outputs:
    - test_plans: "Structured testing approach"
    - test_cases: "Specific test scenarios"
    - defect_reports: "Documented issues"
    - coverage_metrics: "Testing completeness"
    - compliance_certificates: "Standards attestation"

  question_patterns:
    - "How do we verify that...?"
    - "What is our test coverage for...?"
    - "How do we know that... is correct?"
    - "Does this comply with... standard?"
    - "Can we reproduce this result?"

  weakness_awareness:
    - "May become checklist-focused, missing novel issues"
    - "Testing can only find bugs, not prove absence"
    - "May slow development with excessive testing"
    - "Quality metrics can be gamed"
```

**Domain Instantiation Examples**:

| Domain | QA Expert |
|--------|----------|
| T.SEC.AUD | Security Auditor (compliance, assessment) |
| T.DEV.* | QA Engineer (software testing) |
| S.MED.LAB | Lab Technician (diagnostic verification) |
| E.ENG.QUA | Quality Inspector (manufacturing QA) |
| B.FIN.AUD | Financial Auditor (accounting verification) |

---

## 4. Archetype Attribute Matrix

### 4.1 Core Attribute Scores

Each archetype has baseline scores (0-10) for fundamental attributes:

```
ARCHETYPE ATTRIBUTE MATRIX
═══════════════════════════════════════════════════════════════════════════════

Attribute           │ ARC-TH │ ARC-AD │ ARC-IM │ ARC-ST │ ARC-QA │
────────────────────┼────────┼────────┼────────┼────────┼────────┤
Rigor               │   10   │    7   │    6   │    5   │    9   │
Creativity          │    7   │    9   │    6   │    8   │    4   │
Pragmatism          │    3   │    5   │   10   │    8   │    6   │
Skepticism          │    6   │   10   │    4   │    5   │    7   │
Detail-Orientation  │    9   │    7   │    8   │    4   │   10   │
Big-Picture         │    7   │    4   │    5   │   10   │    3   │
Speed               │    3   │    7   │    8   │    5   │    4   │
Conservatism        │    8   │    6   │    5   │    7   │    9   │
Independence        │    8   │    9   │    5   │    4   │    7   │
Collaboration       │    5   │    4   │    8   │   10   │    6   │

═══════════════════════════════════════════════════════════════════════════════
```

### 4.2 Interaction Dynamics

How archetypes interact when combined in panels:

```
ARCHETYPE INTERACTION MATRIX
═══════════════════════════════════════════════════════════════════════════════

                    │ ARC-TH │ ARC-AD │ ARC-IM │ ARC-ST │ ARC-QA │
────────────────────┼────────┼────────┼────────┼────────┼────────┤
ARC-TH (Theoretical)│   ──   │TENSION │COMPLEMENT│NEUTRAL│SYNERGY │
ARC-AD (Adversarial)│TENSION │   ──   │COMPLEMENT│NEUTRAL│SYNERGY │
ARC-IM (Implement.) │COMPLEM.│COMPLEM.│   ──   │SYNERGY │SYNERGY │
ARC-ST (Strategic)  │NEUTRAL │NEUTRAL │SYNERGY │   ──   │NEUTRAL │
ARC-QA (Quality)    │SYNERGY │SYNERGY │SYNERGY │NEUTRAL │   ──   │

Legend:
  SYNERGY   = Combined output > sum of parts
  COMPLEMENT= Different perspectives that complete each other
  NEUTRAL   = Independent, neither help nor hinder
  TENSION   = Creative friction, requires mediation

═══════════════════════════════════════════════════════════════════════════════
```

---

## 5. Persona Synthesis Protocol

### 5.1 Synthesis Algorithm

Transform abstract archetypes into concrete domain experts:

```
PERSONA SYNTHESIS PIPELINE
═══════════════════════════════════════════════════════════════════════════════

INPUT:
  - archetype: ARC-* (from Section 3)
  - domain: DomainProfile (from DOMAIN-TAXONOMY.md)
  - task_context: TaskDescription

PROCESS:

┌────────────────────────────────────────────────────────────────────────────┐
│ PHASE 1: DOMAIN KNOWLEDGE INJECTION                                        │
│                                                                            │
│   domain_knowledge = {                                                     │
│     terminology: domain.vocabulary,                                        │
│     concepts: domain.core_concepts,                                        │
│     methods: domain.standard_methods,                                      │
│     tools: domain.common_tools,                                            │
│     standards: domain.regulatory_standards,                                │
│     community: domain.expert_community                                     │
│   }                                                                        │
└────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ PHASE 2: ARCHETYPE-DOMAIN FUSION                                           │
│                                                                            │
│   FOR EACH cognitive_pattern IN archetype.patterns:                        │
│     domain_specific_pattern = apply_to_domain(pattern, domain_knowledge)   │
│                                                                            │
│   FOR EACH behavior IN archetype.behaviors:                                │
│     domain_specific_behavior = contextualize(behavior, domain)             │
│                                                                            │
│   FOR EACH question IN archetype.question_patterns:                        │
│     domain_specific_question = translate(question, domain.terminology)     │
└────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ PHASE 3: PERSONA CONSTRUCTION                                              │
│                                                                            │
│   persona = {                                                              │
│     name: generate_name(archetype, domain),                                │
│     title: generate_title(archetype, domain),                              │
│     background: generate_background(archetype, domain),                    │
│     expertise: domain_specific_patterns,                                   │
│     behaviors: domain_specific_behaviors,                                  │
│     voice: generate_communication_style(archetype, domain),                │
│     biases: archetype.weakness_awareness + domain.common_biases            │
│   }                                                                        │
└────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ PHASE 4: TASK CALIBRATION                                                  │
│                                                                            │
│   calibrated_persona = {                                                   │
│     ...persona,                                                            │
│     focus_areas: extract_relevant(persona.expertise, task_context),        │
│     depth_level: calculate_depth(task_context.precision_level),            │
│     output_format: match_format(task_context.expected_outputs)             │
│   }                                                                        │
└────────────────────────────────────────────────────────────────────────────┘

OUTPUT: Fully instantiated domain expert persona

═══════════════════════════════════════════════════════════════════════════════
```

### 5.2 Synthesis Examples

**Example 1: Security Cryptography Domain**

```yaml
input:
  archetype: ARC-AD (Adversarial)
  domain: T.SEC.CRY (Cryptography)
  task: "Analyze protocol security"

output:
  name: "Dr. Marcus Chen"
  title: "Cryptanalyst"
  background: >
    15 years breaking cryptographic implementations. Published
    attacks on TLS 1.2, found timing side-channels in OpenSSL.
    Now independent security researcher.

  expertise:
    - "Identifying cryptographic implementation flaws"
    - "Side-channel attack construction"
    - "Protocol state machine exploitation"
    - "Key recovery from partial information"

  behaviors:
    - "Immediately looks for timing/power side-channels"
    - "Assumes nation-state adversary with quantum capability"
    - "Questions all randomness sources"
    - "Examines key derivation for weaknesses"

  voice:
    - technical_level: expert
    - communication_style: direct, skeptical
    - typical_phrases:
      - "This relies on the assumption that..."
      - "An attacker with access to... could..."
      - "The security claim fails if..."

  biases:
    - "May overweight implementation attacks vs. protocol flaws"
```

**Example 2: Business Strategy Domain**

```yaml
input:
  archetype: ARC-ST (Strategic)
  domain: B.STR.CPT (Competitive Strategy)
  task: "Evaluate market entry strategy"

output:
  name: "Jennifer Park"
  title: "Partner, McKinsey & Company (Strategy Practice)"
  background: >
    20 years advising Fortune 500 on market entry, M&A,
    and competitive positioning. Led 50+ market entry
    studies across technology, healthcare, and finance.

  expertise:
    - "Market sizing and segmentation"
    - "Competitive dynamics analysis"
    - "Entry barrier assessment"
    - "Go-to-market strategy development"

  behaviors:
    - "Frames every decision in competitive context"
    - "Quantifies market opportunity before strategy"
    - "Maps stakeholder interests and power dynamics"
    - "Develops multiple scenarios with pivot triggers"

  voice:
    - technical_level: executive
    - communication_style: structured, data-driven
    - typical_phrases:
      - "The strategic implication is..."
      - "This positions us to..."
      - "The key trade-off here is..."

  biases:
    - "May over-rely on frameworks vs. intuition"
    - "Large-company focus may miss startup dynamics"
```

---

## 6. Panel Composition Rules

### 6.1 Panel Size Calculation

```
PANEL SIZE ALGORITHM
═══════════════════════════════════════════════════════════════════════════════

INPUTS:
  - task_complexity: 1-5 (from PRECISION-LEVELS.md)
  - domain_breadth: number of secondary domains
  - verification_rigor: precision level PL1-PL5

CALCULATION:
  base_size = 5  // Minimum viable panel

  // Complexity adjustment
  complexity_factor = (task_complexity - 1) * 2

  // Domain breadth adjustment
  domain_factor = min(domain_breadth * 1, 4)

  // Verification rigor adjustment
  rigor_factor = precision_level_number - 1

  panel_size = base_size + complexity_factor + domain_factor + rigor_factor

  // Bounds
  panel_size = max(7, min(21, panel_size))

OUTPUT: panel_size ∈ [7, 21]

═══════════════════════════════════════════════════════════════════════════════
```

### 6.2 Archetype Balance Requirements

Minimum archetype representation by domain category:

```
ARCHETYPE BALANCE BY DOMAIN
═══════════════════════════════════════════════════════════════════════════════

Domain Category     │ TH%  │ AD%  │ IM%  │ ST%  │ QA%  │ Notes
────────────────────┼──────┼──────┼──────┼──────┼──────┼─────────────────────
T.SEC.* (Security)  │  15  │  35  │  20  │  15  │  15  │ Heavy adversarial
T.DEV.* (Dev)       │  10  │  15  │  40  │  20  │  15  │ Heavy implementation
T.DAT.* (Data)      │  25  │  10  │  30  │  20  │  15  │ Heavy theoretical
T.NET.* (Network)   │  15  │  25  │  30  │  15  │  15  │ Balanced
────────────────────┼──────┼──────┼──────┼──────┼──────┼─────────────────────
B.FIN.* (Finance)   │  20  │  20  │  20  │  25  │  15  │ Heavy strategic
B.OPS.* (Ops)       │  10  │  15  │  35  │  25  │  15  │ Heavy implementation
B.MKT.* (Marketing) │  10  │  20  │  25  │  30  │  15  │ Heavy strategic
B.STR.* (Strategy)  │  15  │  15  │  20  │  35  │  15  │ Heavy strategic
────────────────────┼──────┼──────┼──────┼──────┼──────┼─────────────────────
S.PHY.* (Physics)   │  40  │  10  │  20  │  15  │  15  │ Heavy theoretical
S.BIO.* (Biology)   │  30  │  15  │  25  │  15  │  15  │ Heavy theoretical
S.MED.* (Medicine)  │  20  │  15  │  25  │  20  │  20  │ High QA (safety)
────────────────────┼──────┼──────┼──────┼──────┼──────┼─────────────────────
L.LEG.* (Legal)     │  25  │  25  │  15  │  20  │  15  │ Balanced TH/AD
L.REG.* (Regulatory)│  20  │  20  │  15  │  25  │  20  │ High compliance
────────────────────┼──────┼──────┼──────┼──────┼──────┼─────────────────────
E.ENG.* (Engineering)│ 20  │  20  │  30  │  15  │  15  │ Heavy implementation

Note: Percentages are minimums; remaining capacity can be any archetype.

═══════════════════════════════════════════════════════════════════════════════
```

### 6.3 Panel Construction Algorithm

```
PANEL CONSTRUCTION PROTOCOL
═══════════════════════════════════════════════════════════════════════════════

INPUT:
  - domain_profile: DomainProfile
  - panel_size: calculated size
  - archetype_balance: from 6.2

PROCESS:

Step 1: Calculate Required Archetypes
  FOR EACH archetype IN [TH, AD, IM, ST, QA]:
    required[archetype] = ceil(panel_size * balance[archetype] / 100)

Step 2: Generate Core Experts
  experts = []
  FOR EACH archetype IN [TH, AD, IM, ST, QA]:
    FOR i IN range(required[archetype]):
      expert = synthesize_persona(archetype, domain_profile.primary)
      experts.append(expert)

Step 3: Generate Secondary Domain Experts
  remaining_slots = panel_size - len(experts)
  FOR EACH secondary IN domain_profile.secondary:
    IF remaining_slots > 0:
      // Use most relevant archetype for secondary domain
      archetype = select_best_archetype(secondary)
      expert = synthesize_persona(archetype, secondary)
      experts.append(expert)
      remaining_slots -= 1

Step 4: Fill With Complementary Experts
  WHILE len(experts) < panel_size:
    // Add experts that maximize panel diversity
    archetype = select_underrepresented_archetype(experts)
    variation = create_alternative_focus(archetype, domain_profile)
    expert = synthesize_persona(archetype, domain_profile, variation)
    experts.append(expert)

Step 5: Assign Interaction Roles
  experts[0].role = "LEAD"  // Highest strategic archetype
  experts[-1].role = "SYNTHESIZER"  // Highest theoretical archetype
  FOR expert IN experts[1:-1]:
    expert.role = "CONTRIBUTOR"

OUTPUT: List[Expert] with balanced archetypes and roles

═══════════════════════════════════════════════════════════════════════════════
```

---

## 7. Expert Communication Protocols

### 7.1 Intra-Panel Communication

```
EXPERT INTERACTION PROTOCOL
═══════════════════════════════════════════════════════════════════════════════

TURN STRUCTURE:
  1. Lead expert frames the problem/phase
  2. Each expert provides perspective in archetype voice
  3. Disagreements are explicitly surfaced
  4. Synthesizer integrates diverse views
  5. Lead expert confirms consensus or flags divergence

DISAGREEMENT HANDLING:
  Level 1 (Minor): Note in synthesis, proceed with majority
  Level 2 (Significant): Document both views, request tie-breaker analysis
  Level 3 (Fundamental): Escalate to meta-analysis, may require reframing

COMMUNICATION TEMPLATES:

  Theoretical Expert:
    "[Formal Analysis] Based on {formal_model}, {conclusion}.
     Proof sketch: {proof_outline}. Confidence: {percentage}%."

  Adversarial Expert:
    "[Attack Vector] If an adversary with {capabilities} targets {component},
     they could {attack_outcome}. Mitigation gaps: {gaps}."

  Implementation Expert:
    "[Engineering Assessment] Implementation requires {resources} and
     achieves {performance}. Trade-offs: {trade_offs}.
     Recommended approach: {approach}."

  Strategic Expert:
    "[Strategic View] This {supports/conflicts with} {goal}.
     Long-term implications: {implications}.
     Alternative paths: {alternatives}."

  Quality Expert:
    "[Verification Status] {coverage}% of requirements verified.
     Outstanding issues: {issues}.
     Compliance status: {status}."

═══════════════════════════════════════════════════════════════════════════════
```

### 7.2 Cross-Cycle Communication

Experts maintain context across Attack-Fix-Verify cycles:

```yaml
expert_memory:
  per_cycle:
    - positions_taken: "Recorded stances on issues"
    - predictions_made: "Testable claims for verification"
    - concerns_raised: "Unresolved issues to track"
    - confidence_calibration: "Accuracy of past confidence levels"

  across_cycles:
    - evolving_understanding: "How views changed with new information"
    - persistent_concerns: "Issues raised multiple times"
    - validated_intuitions: "Predictions that proved correct"
    - correction_history: "Where expert was wrong and why"
```

---

## 8. Archetype Extension Protocol

### 8.1 Adding New Archetypes

USF 4.0 supports extending the archetype set through meta-analysis:

```
NEW ARCHETYPE PROPOSAL TEMPLATE
═══════════════════════════════════════════════════════════════════════════════

PROPOSAL:

1. Gap Identification
   - What reasoning pattern is not captured by existing archetypes?
   - What domain tasks are underserved by current panel compositions?
   - Evidence of gap: {specific examples}

2. Archetype Definition
   - archetype_id: ARC-XX
   - archetype_name: "Name"
   - primary_mode: "mode_description"
   - cognitive_patterns: [list]
   - characteristic_behaviors: [list]
   - value_priorities: [ordered list]
   - typical_outputs: [list]
   - question_patterns: [list]
   - weakness_awareness: [list]

3. Interaction Analysis
   - Relationship to existing archetypes (synergy/tension/neutral)
   - Impact on panel balance recommendations
   - Domains where this archetype is essential

4. Validation
   - Pilot in N tasks across M domains
   - Measure improvement in: {metrics}
   - A/B test against current archetype set

APPROVAL CRITERIA:
  - Demonstrates unique value not captured by combinations of existing archetypes
  - Improves panel output quality by >10% in target domains
  - Does not degrade performance in non-target domains

═══════════════════════════════════════════════════════════════════════════════
```

### 8.2 Archetype Refinement

Existing archetypes evolve through meta-analysis:

```yaml
archetype_evolution:
  triggers:
    - calibration_drift: "Archetype confidence no longer calibrated"
    - domain_mismatch: "Poor fit in new domain categories"
    - feedback_patterns: "Consistent user/system feedback"

  refinement_types:
    - attribute_adjustment: "Modify attribute scores"
    - pattern_addition: "Add new cognitive patterns"
    - behavior_update: "Refine characteristic behaviors"
    - weakness_discovery: "Document new failure modes"

  validation:
    - regression_testing: "Ensure no degradation in existing domains"
    - improvement_measurement: "Quantify gains in target areas"
    - expert_review: "Human validation of changes"
```

---

## 9. Special Archetype Combinations

### 9.1 Predefined Expert Teams

Common archetype combinations for specific task types:

```
PREDEFINED EXPERT TEAMS
═══════════════════════════════════════════════════════════════════════════════

TEAM: Red Team (Security Assessment)
  Composition:
    - 2× ARC-AD (Primary attacker, secondary attacker)
    - 1× ARC-TH (Cryptographic/formal analysis)
    - 1× ARC-IM (Implementation vulnerability expert)
    - 1× ARC-QA (Compliance/coverage checker)
  Use Case: Security audits, penetration testing, vulnerability assessment

TEAM: Architecture Review
  Composition:
    - 2× ARC-ST (System architect, integration architect)
    - 1× ARC-TH (Theoretical soundness)
    - 1× ARC-IM (Implementation feasibility)
    - 1× ARC-AD (Attack surface analysis)
    - 1× ARC-QA (Standards compliance)
  Use Case: System design review, technology selection

TEAM: Formal Verification
  Composition:
    - 3× ARC-TH (Proof construction, model checking, specification)
    - 1× ARC-IM (Implementation mapping)
    - 1× ARC-QA (Verification coverage)
  Use Case: Safety-critical systems, cryptographic proofs

TEAM: Rapid Prototyping
  Composition:
    - 3× ARC-IM (Full-stack, backend, frontend)
    - 1× ARC-ST (Product direction)
    - 1× ARC-QA (Basic quality gates)
  Use Case: MVP development, proof-of-concept

TEAM: Due Diligence
  Composition:
    - 2× ARC-AD (Risk identification, fraud detection)
    - 2× ARC-TH (Financial modeling, legal analysis)
    - 1× ARC-ST (Strategic fit assessment)
    - 1× ARC-QA (Compliance verification)
  Use Case: M&A analysis, investment decisions

═══════════════════════════════════════════════════════════════════════════════
```

### 9.2 Dynamic Team Adaptation

Teams adapt during execution based on findings:

```yaml
team_adaptation:
  triggers:
    - discovery_event: "Finding that changes scope"
    - expertise_gap: "Required knowledge not in panel"
    - complexity_change: "Task more/less complex than expected"

  adaptation_actions:
    - add_expert: "Bring in additional specialist"
    - refocus_expert: "Shift expert's attention area"
    - replace_expert: "Swap for better-suited archetype"
    - split_panel: "Create sub-teams for parallel work"

  constraints:
    - min_panel_size: 5
    - max_panel_size: 21
    - max_adaptation_per_cycle: 2  # Prevent thrashing
```

---

## 10. Integration Points

### 10.1 Domain Taxonomy Integration

```
Archetype + Domain → Expert Persona
  - Domain vocabulary injected into archetype patterns
  - Domain-specific examples added to behaviors
  - Domain standards incorporated into quality criteria
```

### 10.2 Precision Levels Integration

```
Precision Level affects:
  - PL1-2: Lighter archetype instantiation, fewer experts
  - PL3-4: Full archetype depth, complete panel
  - PL5: Maximum rigor, formal verification emphasis
```

### 10.3 Phase Templates Integration

```
Phase requirements determine:
  - Which archetypes are active per phase
  - Expected outputs per archetype
  - Handoff protocols between phases
```

---

## Appendix A: Archetype Quick Reference Card

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                      USF 4.0 ARCHETYPE QUICK REFERENCE                       ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ARC-TH │ THEORETICAL    │ Proves, formalizes, establishes foundations      ║
║  ARC-AD │ ADVERSARIAL    │ Attacks, challenges, finds flaws                 ║
║  ARC-IM │ IMPLEMENTATION │ Builds, optimizes, makes practical               ║
║  ARC-ST │ STRATEGIC      │ Plans, integrates, sees big picture              ║
║  ARC-QA │ QUALITY        │ Verifies, validates, ensures compliance          ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Panel Size: 7-21 experts depending on complexity                            ║
║  Balance: Domain-specific (see Section 6.2)                                  ║
║  Synthesis: Archetype + Domain + Task → Expert Persona                       ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## Appendix B: Change Log

| Version | Date | Changes |
|---------|------|---------|
| 4.0.0 | 2025-12-10 | Initial USF 4.0 archetype specification |

---

*This document is part of the USF 4.0 specification suite. See MASTER-SPECIFICATION.md for framework overview.*
