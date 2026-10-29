# USF 4.0: Expert Generator

> **Version**: 4.1.0 (See VERSION.yaml)
> **Component**: Domain Adaptation / Expert Generator
> **Status**: Specification
> **Dependencies**: core/EXPERT-ARCHETYPES.md, core/DOMAIN-TAXONOMY.md, DOMAIN-DETECTOR.md
> **Last Updated**: 2025-12-10
> **SKYNET Integration**: Standardized agent template structure

---

## 1. Overview

The Expert Generator synthesizes domain-specific expert personas from universal archetypes. It takes abstract reasoning patterns and infuses them with domain knowledge, creating fully realized experts capable of providing domain-appropriate analysis.

```
EXPERT GENERATION PIPELINE
═══════════════════════════════════════════════════════════════════════════════

    INPUTS                           SYNTHESIS                      OUTPUT
    ──────                           ─────────                      ──────

    ┌───────────────┐
    │   ARCHETYPE   │────┐
    │   (ARC-AD)    │    │
    └───────────────┘    │
                         │
    ┌───────────────┐    │    ┌─────────────────────────────┐    ┌──────────┐
    │    DOMAIN     │────┼───►│     PERSONA SYNTHESIZER     │───►│  EXPERT  │
    │  (T.SEC.CRY)  │    │    │                             │    │  PERSONA │
    └───────────────┘    │    │  • Knowledge Injection      │    │          │
                         │    │  • Pattern Contextualization│    │ Dr. Chen │
    ┌───────────────┐    │    │  • Voice Calibration        │    │ Crypto-  │
    │    TASK       │────┘    │  • Bias Awareness           │    │ analyst  │
    │   CONTEXT     │         └─────────────────────────────┘    └──────────┘
    └───────────────┘

═══════════════════════════════════════════════════════════════════════════════
```

---

## 2. Synthesis Process

### 2.1 Phase 1: Domain Knowledge Injection

```yaml
knowledge_injection:
  purpose: "Infuse archetype with domain-specific knowledge"

  knowledge_components:
    vocabulary:
      source: "Domain-specific term dictionaries"
      injection: "Replace generic terms with domain equivalents"
      example:
        generic: "system weakness"
        T.SEC.CRY: "cryptographic vulnerability"
        S.MED.DIA: "clinical contraindication"
        L.LEG.CON: "constitutional deficiency"

    concepts:
      source: "Domain concept graphs"
      injection: "Load relevant concept relationships"
      example:
        T.SEC.CRY:
          - "Cipher → Block cipher, Stream cipher"
          - "Key exchange → DH, ECDH, X25519"
          - "Attack → Side-channel, Cryptanalysis"

    methods:
      source: "Domain methodology databases"
      injection: "Equip expert with standard approaches"
      example:
        T.SEC.CRY:
          - "Provable security reductions"
          - "Random oracle model analysis"
          - "Side-channel analysis methodology"

    tools:
      source: "Domain tool registries"
      injection: "Reference appropriate tools"
      example:
        T.SEC.CRY: ["SageMath", "OpenSSL", "Cryptol"]
        T.DEV.WEB: ["Chrome DevTools", "Postman", "Jest"]
        S.MED.DIA: ["PACS", "HL7 FHIR", "Clinical DSS"]

    standards:
      source: "Regulatory and standards databases"
      injection: "Awareness of applicable standards"
      example:
        T.SEC.CRY: ["NIST SP 800-57", "FIPS 140-3"]
        S.MED: ["HIPAA", "FDA 21 CFR Part 11"]
        B.FIN: ["SOX", "Basel III", "PCI-DSS"]

  injection_process:
    1: "Load domain knowledge package"
    2: "Map archetype patterns to domain equivalents"
    3: "Expand archetype vocabulary"
    4: "Validate knowledge consistency"
```

### 2.2 Phase 2: Pattern Contextualization

```yaml
pattern_contextualization:
  purpose: "Adapt archetype cognitive patterns to domain context"

  transformations:
    ARC-TH_patterns:
      generic: "formal_reasoning"
      domain_specific:
        T.SEC.CRY: "Cryptographic proof construction"
        S.PHY.QUA: "Quantum mechanical formalism"
        L.LEG.CON: "Constitutional interpretation"

      generic: "abstraction"
      domain_specific:
        T.SEC.CRY: "Security game abstraction"
        B.STR.CPT: "Market dynamics modeling"
        E.ENG.CIV: "Structural load abstraction"

    ARC-AD_patterns:
      generic: "attack_surface_mapping"
      domain_specific:
        T.SEC.CRY: "Cryptanalytic attack surface"
        B.FIN.INV: "Investment risk surface"
        L.LEG.LIT: "Legal vulnerability analysis"

      generic: "assumption_challenging"
      domain_specific:
        T.SEC.CRY: "Security assumption challenges"
        S.MED.DIA: "Differential diagnosis challenges"
        B.STR.CPT: "Market assumption challenges"

    ARC-IM_patterns:
      generic: "systems_thinking"
      domain_specific:
        T.DEV.SYS: "Software architecture thinking"
        E.ENG.MEC: "Mechanical systems design"
        B.OPS.MAN: "Business process thinking"

    # ... patterns for all archetypes

  contextualization_process:
    1: "For each archetype pattern"
    2: "Look up domain-specific equivalent"
    3: "Substitute with domain context"
    4: "Preserve pattern structure, change content"
```

### 2.3 Phase 3: Voice Calibration

```yaml
voice_calibration:
  purpose: "Establish appropriate communication style"

  voice_dimensions:
    technical_level:
      calculation: "Based on domain + precision level"
      levels:
        - "executive": "High-level, minimal jargon"
        - "professional": "Industry standard terminology"
        - "expert": "Full technical depth"
        - "specialist": "Deep specialization vocabulary"

    formality:
      calculation: "Based on domain norms"
      examples:
        L.LEG: "High formality, legal conventions"
        T.DEV: "Moderate formality, technical clarity"
        B.MKT: "Variable formality, audience-dependent"

    communication_patterns:
      by_archetype:
        ARC-TH:
          typical_phrases:
            - "Formally, we can express this as..."
            - "The proof proceeds by..."
            - "Under the assumption that..."
          structure: "Logical, sequential, precise"

        ARC-AD:
          typical_phrases:
            - "An attacker could..."
            - "This fails if..."
            - "The vulnerability exists when..."
          structure: "Threat-focused, scenario-based"

        ARC-IM:
          typical_phrases:
            - "The implementation would require..."
            - "Performance characteristics include..."
            - "Trade-offs to consider are..."
          structure: "Practical, solution-oriented"

  voice_output:
    template: |
      Expert speaks with {formality} formality,
      using {technical_level} technical vocabulary,
      following {archetype} communication patterns,
      adapted for {domain} domain conventions.
```

### 2.4 Phase 4: Bias Awareness

```yaml
bias_awareness:
  purpose: "Equip expert with self-awareness of limitations"

  bias_sources:
    archetype_biases:
      source: "From EXPERT-ARCHETYPES.md weakness_awareness"
      injection: "Expert acknowledges archetype-inherent limitations"

    domain_biases:
      source: "Domain-specific common biases"
      examples:
        T.SEC: "Security theater, checkbox compliance"
        B.FIN: "Recency bias, overconfidence in models"
        S.MED: "Anchoring on initial diagnosis"
        L.LEG: "Jurisdiction-centric thinking"

    persona_biases:
      source: "Generated from persona background"
      example:
        persona: "Former NSA cryptanalyst"
        bias: "May overweight government threat models"

  bias_injection:
    method: "Add bias awareness to persona definition"
    output:
      - "Expert is aware they may {bias_tendency}"
      - "Expert should actively counter-balance {bias}"
      - "Expert should seek alternative views on {bias_area}"
```

---

## 3. Persona Template

### 3.1 Complete Persona Structure

```yaml
persona_template:
  identity:
    name: "Generated contextual name"
    title: "Professional title"
    background: "2-3 sentence background"
    years_experience: "Generated based on expertise level"
    affiliations: "Relevant organizations/institutions"

  expertise:
    primary_domain: "Domain identifier"
    specializations: ["Specific areas of deep expertise"]
    methodologies: ["Known/preferred methodologies"]
    tools: ["Tools regularly used"]
    publications: ["Implied publication areas"]

  archetype_expression:
    base_archetype: "ARC-* identifier"
    cognitive_patterns: ["Domain-contextualized patterns"]
    characteristic_behaviors: ["Domain-adapted behaviors"]
    value_priorities: ["Domain-calibrated priorities"]

  communication:
    voice: "Voice calibration output"
    typical_phrases: ["Domain + archetype phrases"]
    question_patterns: ["How expert asks questions"]
    output_formats: ["Preferred analysis structures"]

  biases_and_limitations:
    acknowledged_biases: ["Known biases"]
    blind_spots: ["Potential blind spots"]
    counter_balance: ["How expert compensates"]

  panel_role:
    role: "LEAD | CONTRIBUTOR | SYNTHESIZER"
    interaction_style: "How expert engages with panel"
    influence_weight: "Relative weight in synthesis"
```

### 3.2 Name Generation

```yaml
name_generation:
  purpose: "Create contextually appropriate expert names"

  factors:
    domain_culture:
      T: "Tech industry naming conventions"
      B: "Business professional naming"
      S: "Academic/scientific naming"
      L: "Legal professional naming"
      E: "Engineering profession naming"

    diversity:
      principle: "Varied backgrounds represented"
      implementation: "Rotating cultural backgrounds"

    consistency:
      principle: "Same inputs → same name"
      implementation: "Deterministic generation from seed"

  name_components:
    title:
      academic: ["Dr.", "Prof."]
      professional: [""]
      medical: ["Dr."]
      legal: [""]

    format:
      western: "{Title} {First} {Last}"
      eastern: "{Title} {Last} {First}"
```

### 3.3 Background Generation

```yaml
background_generation:
  template: |
    {years} years in {domain_area}. {notable_experience}.
    {current_role}. Known for {specialty}.

  components:
    years:
      junior: "5-10"
      senior: "10-20"
      expert: "20+"
      calculation: "Based on precision level + expertise depth"

    notable_experience:
      T.SEC: "Previously at {security_org}, discovered {vulnerability_type}"
      B.FIN: "Led {deal_type} at {institution}"
      S.MED: "Published in {journal}, specializing in {condition}"
      L.LEG: "Argued cases at {court_level}"

    current_role:
      patterns:
        - "Now {title} at {organization}"
        - "Currently leading {initiative}"
        - "Independent consultant specializing in {area}"
```

---

## 4. Panel Composition

### 4.1 Panel Size Determination

```yaml
panel_sizing:
  algorithm: |
    base_size = 5

    // Complexity adjustment
    complexity_factor = (task_complexity - 1) × 2

    // Domain breadth adjustment
    domain_factor = min(secondary_domains × 1, 4)

    // Precision adjustment
    precision_factor = precision_level - 1

    panel_size = base_size + complexity_factor + domain_factor + precision_factor
    panel_size = clamp(panel_size, 7, 21)

  examples:
    simple_task:
      task_complexity: 2
      secondary_domains: 0
      precision_level: 2
      result: 5 + 2 + 0 + 1 = 8 experts

    complex_multi_domain:
      task_complexity: 4
      secondary_domains: 3
      precision_level: 4
      result: 5 + 6 + 3 + 3 = 17 experts
```

### 4.2 Archetype Distribution

```yaml
archetype_distribution:
  source: "PHASE-TEMPLATES.md archetype balance by domain"

  distribution_algorithm:
    1: "Get domain's archetype balance percentages"
    2: "Calculate required count per archetype"
    3: "Round to ensure total = panel_size"
    4: "Verify minimum representation constraints"

  example:
    domain: "T.SEC.*"
    panel_size: 11
    balance: "TH:15%, AD:35%, IM:20%, ST:15%, QA:15%"
    distribution:
      ARC-TH: 2  # ceil(11 × 0.15)
      ARC-AD: 4  # ceil(11 × 0.35)
      ARC-IM: 2  # ceil(11 × 0.20)
      ARC-ST: 2  # ceil(11 × 0.15)
      ARC-QA: 1  # remainder

  secondary_domain_handling:
    method: "Add experts for secondary domains"
    archetype_selection: "Most relevant archetype for secondary domain"
    example:
      secondary: "T.DEV.SYS"
      add: "1 × ARC-IM with T.DEV.SYS expertise"
```

### 4.3 Role Assignment

```yaml
role_assignment:
  roles:
    LEAD:
      count: 1
      selection: "Highest strategic archetype score"
      responsibilities:
        - "Frame problems and phases"
        - "Guide panel discussion"
        - "Make tie-breaking decisions"

    SYNTHESIZER:
      count: 1
      selection: "Highest theoretical archetype score"
      responsibilities:
        - "Integrate diverse perspectives"
        - "Identify consensus and disagreement"
        - "Produce final synthesis"

    CONTRIBUTOR:
      count: "Remaining experts"
      responsibilities:
        - "Provide expertise-specific analysis"
        - "Challenge other perspectives"
        - "Support synthesis"

  assignment_algorithm:
    1: "Score all experts on strategic capacity"
    2: "Assign highest to LEAD"
    3: "Score remaining on theoretical capacity"
    4: "Assign highest to SYNTHESIZER"
    5: "Assign rest as CONTRIBUTOR"
```

---

## 5. Expert Diversity

### 5.1 Diversity Dimensions

```yaml
diversity_dimensions:
  methodological:
    principle: "Different approaches to same problem"
    implementation: "Vary methodologies across experts"
    example:
      T.SEC panel:
        - expert_1: "Static analysis specialist"
        - expert_2: "Dynamic testing expert"
        - expert_3: "Formal verification advocate"

  experiential:
    principle: "Different backgrounds and experiences"
    implementation: "Vary career backgrounds"
    example:
      - "Industry practitioner"
      - "Academic researcher"
      - "Government/regulatory background"

  cognitive:
    principle: "Different thinking styles within archetype"
    implementation: "Vary within-archetype emphasis"
    example:
      two_ARC-AD_experts:
        - expert_1: "Focus on known vulnerability patterns"
        - expert_2: "Focus on novel attack vectors"

  temporal:
    principle: "Different experience levels"
    implementation: "Mix of senior and junior perspectives"
    rationale: "Junior may catch fresh patterns seniors miss"
```

### 5.2 Diversity Enforcement

```yaml
diversity_enforcement:
  constraints:
    methodology_diversity:
      rule: "No more than 40% with same methodology"
      enforcement: "Check during panel construction"

    background_diversity:
      rule: "At least 2 distinct background types"
      enforcement: "Track and enforce during generation"

    perspective_diversity:
      rule: "Include at least one contrarian perspective"
      enforcement: "Assign contrarian role to one expert"

  conflict_resolution:
    if_constraints_conflict:
      priority: "Archetype balance > Diversity > Specific preference"
      action: "Relax diversity constraint if needed"
```

---

## 6. Dynamic Adaptation

### 6.1 Task-Specific Tuning

```yaml
task_specific_tuning:
  tuning_factors:
    task_complexity:
      low: "Reduce expert depth, broaden coverage"
      high: "Increase expert depth, focus expertise"

    output_type:
      report: "Emphasize communication, structure"
      code: "Emphasize implementation details"
      recommendation: "Emphasize strategic thinking"

    audience:
      executive: "Reduce jargon, increase summary"
      technical: "Full technical depth"
      mixed: "Layer information appropriately"

  tuning_application:
    method: "Modify persona parameters post-generation"
    scope: "Voice, output format, depth emphasis"
```

### 6.2 Mid-Task Adaptation

```yaml
mid_task_adaptation:
  triggers:
    scope_change:
      detection: "Task scope expands/contracts"
      response: "Add/remove experts as needed"

    expertise_gap:
      detection: "Panel lacks required knowledge"
      response: "Generate and add specialist"

    deadlock:
      detection: "Panel cannot converge"
      response: "Add mediator/tie-breaker expert"

  adaptation_protocol:
    1: "Detect adaptation trigger"
    2: "Determine adaptation type"
    3: "Generate new expert(s) if needed"
    4: "Integrate into existing panel"
    5: "Preserve context from previous phases"
```

---

## 7. Quality Assurance

### 7.1 Persona Validation

```yaml
persona_validation:
  checks:
    coherence:
      check: "Background matches expertise claims"
      example: "5 years experience can't claim 20 years of work"

    domain_accuracy:
      check: "Domain knowledge is correct"
      method: "Validate against domain knowledge base"

    archetype_fidelity:
      check: "Persona behaves like archetype"
      method: "Compare behavior patterns to archetype spec"

    uniqueness:
      check: "Personas are distinct"
      method: "Measure persona similarity, enforce minimum distance"

  validation_process:
    timing: "After persona generation, before panel activation"
    failure_action: "Regenerate failed personas"
```

### 7.2 Panel Validation

```yaml
panel_validation:
  checks:
    coverage:
      check: "All required archetypes represented"
      threshold: "100% of required archetypes"

    balance:
      check: "Archetype distribution within tolerance"
      threshold: "Within ±10% of target balance"

    diversity:
      check: "Diversity constraints met"
      threshold: "All diversity rules satisfied"

    role_assignment:
      check: "LEAD and SYNTHESIZER assigned"
      threshold: "Exactly 1 of each"

  validation_process:
    timing: "After panel composition"
    failure_action: "Adjust panel and revalidate"
```

---

## 8. Integration Points

### 8.1 Input Interface

```yaml
inputs:
  domain_profile:
    source: "DOMAIN-DETECTOR.md"
    content: "Primary domain, secondary domains, confidence"

  task_context:
    source: "Task input"
    content: "Task description, complexity, output expectations"

  precision_level:
    source: "PRECISION-CALIBRATOR.md"
    content: "PL1-PL5 precision level"

  template:
    source: "PHASE-TEMPLATES.md"
    content: "Selected phase template with archetype balance"
```

### 8.2 Output Interface

```yaml
outputs:
  expert_panel:
    format: "List of Expert Personas"
    content:
      - "Full persona definitions"
      - "Role assignments"
      - "Interaction protocols"

  panel_metadata:
    content:
      - "Panel size and composition"
      - "Diversity metrics"
      - "Validation results"
```

---

## 9. Standardized Agent Template Structure (SKYNET Integration)

### 9.1 Agent Template Format

```yaml
agent_template_structure:
  source: "SKYNET Integration - VoltAgent awesome-claude-code-subagents"
  purpose: "Standardized structure for defining expert agents"

  template_format:
    frontmatter:
      name:
        description: "Unique agent identifier"
        format: "kebab-case"
        example: "security-auditor"

      description:
        description: "When and why to invoke this agent"
        format: "1-2 sentence invocation trigger"
        example: "Use for security-focused code review when changes affect authentication, authorization, or data handling"

      archetype:
        description: "Base USF archetype"
        values: ["ARC-TH", "ARC-AD", "ARC-IM", "ARC-QA", "ARC-ST"]
        example: "ARC-AD"

      tools:
        description: "Permitted tool access"
        format: "Comma-separated list"
        example: "Read, Grep, Glob"
        reference: "See META-ANALYSIS-AGENTS.md Section 2.12 for permission model"

    body_sections:
      role_description:
        purpose: "Define agent's role and identity"
        content:
          - "Professional background"
          - "Years of experience"
          - "Key competencies"
        length: "2-4 paragraphs"

      expertise_areas:
        purpose: "List specific knowledge domains"
        format: "Bulleted list"
        content:
          - "Primary expertise"
          - "Secondary competencies"
          - "Tool proficiencies"

      domain_patterns:
        purpose: "Recognized patterns in this domain"
        content:
          - "Common issues to identify"
          - "Best practices to enforce"
          - "Anti-patterns to flag"

      communication_protocol:
        purpose: "How agent communicates"
        content:
          - "Output format preferences"
          - "Level of technical detail"
          - "Interaction style"

      workflow_phases:
        purpose: "Standard workflow for this agent"
        format: "Numbered phases"
        content:
          - "Phase 1: Initial assessment"
          - "Phase 2: Deep analysis"
          - "Phase 3: Recommendation generation"
          - "Phase 4: Verification"
```

### 9.2 Agent Categories

```yaml
agent_categories:
  source: "VoltAgent 10 categories, 100+ agents"
  purpose: "Organize agents by functional area"

  categories:
    core_development:
      archetype_mix: ["ARC-IM"]
      agent_count: 11
      examples:
        - "api-designer"
        - "backend-developer"
        - "frontend-developer"
        - "fullstack-specialist"

    language_specialists:
      archetype_mix: ["ARC-IM"]
      agent_count: 24
      examples:
        - "typescript-expert"
        - "python-expert"
        - "rust-expert"
        - "go-expert"

    infrastructure:
      archetype_mix: ["ARC-IM", "ARC-QA"]
      agent_count: 12
      examples:
        - "cloud-architect"
        - "devops-engineer"
        - "kubernetes-specialist"

    quality_security:
      archetype_mix: ["ARC-QA", "ARC-AD"]
      agent_count: 12
      examples:
        - "security-auditor"
        - "code-reviewer"
        - "penetration-tester"

    data_ai:
      archetype_mix: ["ARC-TH", "ARC-IM"]
      agent_count: 12
      examples:
        - "data-scientist"
        - "ml-engineer"
        - "llm-architect"

    developer_experience:
      archetype_mix: ["ARC-QA", "ARC-IM"]
      agent_count: 10
      examples:
        - "documentation-engineer"
        - "refactoring-specialist"
        - "tooling-engineer"

    specialized_domains:
      archetype_mix: "Domain-specific ARC-IM"
      agent_count: 11
      examples:
        - "blockchain-developer"
        - "fintech-engineer"
        - "game-developer"

    business_product:
      archetype_mix: ["ARC-ST"]
      agent_count: 10
      examples:
        - "product-manager"
        - "business-analyst"
        - "technical-writer"

    meta_orchestration:
      archetype_mix: "MAL agents"
      agent_count: 8
      critical: true
      note: "Maps directly to MAL-* agents"
      examples:
        - "agent-organizer → MAL-EFFICIENCY"
        - "context-manager → MAL-CONTEXT"
        - "error-coordinator → MAL-ERROR"
        - "workflow-orchestrator → MAL-WORKFLOW"

    research_analysis:
      archetype_mix: ["ARC-TH"]
      agent_count: 6
      examples:
        - "research-analyst"
        - "trend-analyst"
        - "competitive-analyst"
```

### 9.3 Agent Discovery and Loading

```yaml
agent_discovery:
  storage_locations:
    project_level:
      path: ".claude/agents/"
      precedence: "Higher (project-specific)"
      scope: "Current project only"

    user_level:
      path: "~/.claude/agents/"
      precedence: "Lower (global access)"
      scope: "All projects for user"

  discovery_process:
    1: "Scan storage locations for .md files"
    2: "Parse YAML frontmatter"
    3: "Validate against template structure"
    4: "Index by name and category"
    5: "Load on-demand based on task context"

  activation_triggers:
    explicit: "User requests specific agent"
    domain_match: "Domain detector suggests agent"
    task_pattern: "Task matches agent description"
    workflow_stage: "Workflow requires specialist"
```

### 9.4 Agent Validation

```yaml
agent_validation:
  frontmatter_validation:
    required_fields: ["name", "description", "archetype", "tools"]
    archetype_values: ["ARC-TH", "ARC-AD", "ARC-IM", "ARC-QA", "ARC-ST"]
    tools_validation: "Against permitted tools list"

  body_validation:
    required_sections: ["role_description", "expertise_areas"]
    optional_sections: ["domain_patterns", "communication_protocol", "workflow_phases"]
    minimum_content: "Each section non-empty"

  quality_checks:
    coherence: "Background matches expertise"
    archetype_alignment: "Behavior matches archetype"
    tool_appropriateness: "Tools match role needs"
```

---

## Appendix A: Expert Generator Quick Reference

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    USF 4.0 EXPERT GENERATOR REFERENCE                        ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  SYNTHESIS: Archetype + Domain + Task → Expert Persona                       ║
║                                                                              ║
║  PHASES:                                                                     ║
║    1. Knowledge Injection (vocabulary, concepts, methods, tools)            ║
║    2. Pattern Contextualization (adapt cognitive patterns)                   ║
║    3. Voice Calibration (communication style)                                ║
║    4. Bias Awareness (self-awareness of limitations)                         ║
║                                                                              ║
║  PANEL SIZE: 7-21 experts based on complexity                                ║
║  ROLES: LEAD (1), SYNTHESIZER (1), CONTRIBUTOR (rest)                        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## Appendix B: Change Log

| Version | Date | Changes |
|---------|------|---------|
| 4.0.0 | 2025-12-10 | Initial USF 4.0 expert generator specification |
| 4.1.0 | 2025-12-10 | SKYNET Integration: Added Section 9 - Standardized agent template structure with 10 categories and 100+ agent reference |

---

*This document is part of the USF 4.0 specification suite. See MASTER-SPECIFICATION.md for framework overview.*
