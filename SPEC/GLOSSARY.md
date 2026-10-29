# USF 4.0 Glossary

> **Version**: 4.0.3 (See VERSION.yaml)
> **Purpose**: Centralized terminology reference for USF 4.0
> **Last Updated**: 2025-12-10

---

## Quick Reference Index

| Term | Category | Definition |
|------|----------|------------|
| [ARC-*](#archetypes) | Core | Universal expert archetypes |
| [MAL-*](#meta-analysis-agents) | Self-Evolution | Meta-analysis agents |
| [PL1-PL5](#precision-levels) | Precision | Precision level designations |
| [TMPL-*](#templates) | Core | Phase template identifiers |
| [T/S/B/L/E](#domain-codes) | Domain | Top-level domain categories |

---

## Archetypes

### ARC-AD (Adversarial)
**Full Name**: Adversarial Archetype
**Purpose**: Destructive analysis, attack surface mapping, assumption challenging
**Primary Mode**: Challenge and break
**See**: core/EXPERT-ARCHETYPES.md

### ARC-IM (Implementation)
**Full Name**: Implementation Archetype
**Purpose**: Practical realization, systems thinking, trade-off analysis
**Primary Mode**: Build and integrate
**See**: core/EXPERT-ARCHETYPES.md

### ARC-QA (Quality Assurance)
**Full Name**: Quality Assurance Archetype
**Purpose**: Verification, validation, completeness checking
**Primary Mode**: Test and verify
**See**: core/EXPERT-ARCHETYPES.md

### ARC-ST (Strategic)
**Full Name**: Strategic Archetype
**Purpose**: High-level planning, resource allocation, stakeholder management
**Primary Mode**: Plan and coordinate
**See**: core/EXPERT-ARCHETYPES.md

### ARC-TH (Theoretical)
**Full Name**: Theoretical Archetype
**Purpose**: Formal reasoning, abstraction, proof construction
**Primary Mode**: Analyze and prove
**See**: core/EXPERT-ARCHETYPES.md

---

## Meta-Analysis Agents

### MAL-ADVERSARIAL
**Full Name**: Challenge Effectiveness Scorer
**Purpose**: Ensure adversarial processes are effective, not theatrical
**See**: self-evolution/META-ANALYSIS-AGENTS.md

### MAL-CONVERGENCE
**Full Name**: Convergence Pattern Analyzer
**Purpose**: Detect healthy vs pathological convergence patterns
**See**: self-evolution/META-ANALYSIS-AGENTS.md

### MAL-COVERAGE
**Full Name**: Domain Completeness Analyzer
**Purpose**: Ensure USF can handle all relevant domains
**See**: self-evolution/META-ANALYSIS-AGENTS.md

### MAL-EFFICIENCY
**Full Name**: Resource Optimization Analyzer
**Purpose**: Identify and eliminate waste in USF processes
**See**: self-evolution/META-ANALYSIS-AGENTS.md

### MAL-NOVELTY
**Full Name**: Innovation and Stagnation Detector
**Purpose**: Prevent methodology stagnation, encourage innovation
**See**: self-evolution/META-ANALYSIS-AGENTS.md

### MAL-QUALITY
**Full Name**: Output Quality Assessor
**Purpose**: Measure and improve quality of USF outputs
**See**: self-evolution/META-ANALYSIS-AGENTS.md

---

## Precision Levels

### PL1 (Exploratory)
**Confidence Target**: 80%
**Methods**: Heuristic analysis, pattern matching
**Verification**: 2/3 chains agree
**Use Case**: Time-critical, low-stakes tasks
**See**: core/PRECISION-LEVELS.md

### PL2 (Standard)
**Confidence Target**: 90%
**Methods**: Systematic analysis, expert review
**Verification**: 3/4 chains agree
**Use Case**: Normal analysis tasks
**See**: core/PRECISION-LEVELS.md

### PL3 (Formal)
**Confidence Target**: 95%
**Methods**: Formal specification, proof sketches, model checking
**Verification**: 4/5 chains agree
**Use Case**: High-stakes, adversarial contexts
**See**: core/PRECISION-LEVELS.md

### PL4 (Rigorous)
**Confidence Target**: 99%
**Methods**: Machine-checked proofs, exhaustive testing
**Verification**: 5/5 chains agree
**Use Case**: Safety-critical, regulatory contexts
**See**: core/PRECISION-LEVELS.md

### PL5 (Information-Theoretic)
**Confidence Target**: 100% (IT-guaranteed)
**Methods**: Information-theoretic proofs
**Verification**: 5/5 chains + formal proof
**Use Case**: Cryptographic security guarantees
**See**: core/PRECISION-LEVELS.md

---

## Templates

### TMPL-BUS
**Full Name**: Business Template
**Primary Domain**: B.* (Business)
**Phases**: Strategic, Market, Operational, Financial, Risk
**See**: core/PHASE-TEMPLATES.md

### TMPL-DSN
**Full Name**: Design Template
**Primary Domain**: T.DEV.*, E.ENG.*
**Phases**: Requirements, Architecture, Detailed Design, Review
**See**: core/PHASE-TEMPLATES.md

### TMPL-LEG
**Full Name**: Legal Template
**Primary Domain**: L.* (Legal)
**Phases**: Jurisdiction, Doctrine, Application, Risk
**See**: core/PHASE-TEMPLATES.md

### TMPL-SCI
**Full Name**: Scientific Template
**Primary Domain**: S.* (Science/Medical)
**Phases**: Hypothesis, Methodology, Analysis, Validation
**See**: core/PHASE-TEMPLATES.md

### TMPL-SEC
**Full Name**: Security Template
**Primary Domain**: T.SEC.*
**Phases**: Threat Model, Attack Surface, Vulnerability, Mitigation, Verification
**See**: core/PHASE-TEMPLATES.md

---

## Domain Codes

### Top-Level Domains

| Code | Name | Description |
|------|------|-------------|
| T | Technology | Software, hardware, security, networking |
| S | Science/Medical | Scientific research, healthcare, biology |
| B | Business | Finance, strategy, operations, marketing |
| L | Legal | Law, compliance, regulation, governance |
| E | Engineering | Civil, mechanical, electrical, aerospace |

### Common Subdomains

| Code | Full Path | Description |
|------|-----------|-------------|
| T.SEC | Technology.Security | Information security |
| T.SEC.CRY | Technology.Security.Cryptography | Cryptographic systems |
| T.DEV | Technology.Development | Software development |
| T.NET | Technology.Networking | Network systems |
| S.MED | Science.Medical | Medical/healthcare |
| B.FIN | Business.Finance | Financial services |
| B.STR | Business.Strategy | Strategic planning |
| L.REG | Legal.Regulatory | Regulatory compliance |
| E.ENG | Engineering.* | Engineering disciplines |

**See**: core/DOMAIN-TAXONOMY.md

---

## Verification Chains

### CHAIN-A (Static)
**Type**: Static Analysis
**Methods**: Code review, formal inspection, symbolic analysis
**See**: precision/VERIFICATION-CHAINS.md

### CHAIN-B (Dynamic)
**Type**: Dynamic Testing
**Methods**: Fuzzing, penetration testing, runtime verification
**See**: precision/VERIFICATION-CHAINS.md

### CHAIN-C (Formal)
**Type**: Formal Methods
**Methods**: Theorem proving, model checking, abstract interpretation
**See**: precision/VERIFICATION-CHAINS.md

### CHAIN-D (Empirical)
**Type**: Empirical Validation
**Methods**: Statistical testing, A/B testing, field trials
**See**: precision/VERIFICATION-CHAINS.md

### CHAIN-E (Expert)
**Type**: Expert Review
**Methods**: Independent expert assessment, peer review
**See**: precision/VERIFICATION-CHAINS.md

---

## Execution Modes

### Deep Mode
**Description**: Maximum depth analysis for critical systems
**Min Precision**: PL4
**Use Case**: Safety-critical, formal verification required
**See**: integration/EXECUTION-FLOW.md

### Fast Mode
**Description**: Accelerated execution with reduced depth
**Max Precision**: PL2
**Use Case**: Time-sensitive, preliminary analysis
**See**: integration/EXECUTION-FLOW.md

### Incremental Mode
**Description**: Build on previous analysis
**Use Case**: Updates, refinements, follow-up questions
**See**: integration/EXECUTION-FLOW.md

### Standard Mode
**Description**: Full execution with all components
**Use Case**: Normal analysis tasks
**See**: integration/EXECUTION-FLOW.md

---

## Bootstrap Phases

### Phase 1: Full Human Oversight
**Cycles**: 1-3
**Human Approval**: 100%
**Trust Score**: Building
**See**: self-evolution/BOOTSTRAP-PROTOCOL.md

### Phase 2: Risk-Stratified Autonomy
**Cycles**: 4-10
**Human Approval**: ~70% (risk-based)
**Trust Score**: 0.6-0.75
**See**: self-evolution/BOOTSTRAP-PROTOCOL.md

### Phase 3: Exception-Based Oversight
**Cycles**: 11-20
**Human Approval**: ~30% (exceptions only)
**Trust Score**: 0.75-0.85
**See**: self-evolution/BOOTSTRAP-PROTOCOL.md

### Phase 4: Autonomous with Audit
**Cycles**: 21+
**Human Approval**: ~5% (CRITICAL + audit)
**Trust Score**: >0.85
**See**: self-evolution/BOOTSTRAP-PROTOCOL.md

---

## Uncertainty Types

### Aleatory Uncertainty
**Definition**: Irreducible uncertainty due to inherent randomness
**Examples**: Adversary behavior, environmental variation
**See**: precision/UNCERTAINTY-QUANTIFICATION.md

### Epistemic Uncertainty
**Definition**: Reducible uncertainty due to lack of knowledge
**Examples**: Missing data, limited analysis, knowledge gaps
**See**: precision/UNCERTAINTY-QUANTIFICATION.md

### Model Uncertainty
**Definition**: Uncertainty about model/assumption accuracy
**Examples**: Threat model incomplete, abstraction loss
**See**: precision/UNCERTAINTY-QUANTIFICATION.md

---

## Other Key Terms

### AFV Cycle
**Full Name**: Attack-Fix-Verify Cycle
**Definition**: Core adversarial improvement loop where ARC-AD attacks, ARC-IM/TH fix, and ARC-QA/TH verify
**See**: integration/EXECUTION-FLOW.md

### Cold Start
**Definition**: Initial deployment state before sufficient historical data exists for trust calculation
**See**: self-evolution/BOOTSTRAP-PROTOCOL.md

### Convergence
**Definition**: State where expert panel positions stabilize and no new significant issues emerge
**See**: integration/CONVERGENCE-CRITERIA.md

### Expert Panel
**Definition**: Dynamically generated set of domain-specific expert personas synthesized from archetypes
**See**: domain-adaptation/EXPERT-GENERATOR.md

### Gate
**Definition**: Checkpoint between phases requiring criteria to be met before proceeding
**See**: core/PHASE-TEMPLATES.md

### Meta-Analysis Cycle (MAC)
**Definition**: One complete sweep of all MAL agents analyzing operational data
**Trigger**: 10 tasks OR 7 days (whichever first)
**See**: self-evolution/BOOTSTRAP-PROTOCOL.md

### ORACLE-META
**Definition**: The self-evolution engine of USF 4.0, comprising MAL agents and improvement protocols
**See**: MASTER-SPECIFICATION.md

### Pattern Library
**Definition**: Collection of cross-domain transferable patterns for analogical reasoning
**See**: domain-adaptation/CROSS-DOMAIN-TRANSFER.md

### Trust Score
**Definition**: Quantified measure of USF self-improvement reliability (0-1 scale)
**See**: self-evolution/BOOTSTRAP-PROTOCOL.md

---

## Appendix: Acronym Reference

| Acronym | Expansion |
|---------|-----------|
| AFV | Attack-Fix-Verify |
| ARC | Archetype |
| CS | Consequence Severity (precision factor) |
| DC | Domain Complexity (precision factor) |
| AE | Adversarial Exposure (precision factor) |
| IT | Information-Theoretic |
| MAC | Meta-Analysis Cycle |
| MAL | Meta-Analysis Layer |
| PL | Precision Level |
| TC | Time Criticality (precision factor) |
| TMPL | Template |
| USF | Unified Superintelligence Framework |
| VA | Verification Availability (precision factor) |

---

*This glossary is part of the USF 4.0 specification suite. See MASTER-SPECIFICATION.md for framework overview.*
