# USF 4.0: Execution Flow

> **Version**: 4.1.1 (See VERSION.yaml)
> **Component**: Integration / Execution Flow
> **Status**: Specification
> **Dependencies**: All core specifications
> **Last Updated**: 2025-12-10
> **SKYNET Integration**: Behavioral modes, workflow patterns

---

## 1. Overview

The Execution Flow defines the complete operational pipeline of USF 4.0, from task input to final output with meta-analysis. It integrates all components into a coherent execution model.

```
USF 4.0 COMPLETE EXECUTION FLOW
═══════════════════════════════════════════════════════════════════════════════

    INPUT                    OPERATIONAL LAYER                    OUTPUT
    ─────                    ─────────────────                    ──────

    ┌─────────┐
    │  TASK   │
    │  INPUT  │
    └────┬────┘
         │
         ▼
    ┌────────────────────────────────────────────────────────────────────────┐
    │                        INITIALIZATION ENGINE                            │
    │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
    │  │   Domain    │  │  Precision  │  │   Expert    │  │   Template  │   │
    │  │  Detection  │─►│ Calibration │─►│ Generation  │─►│  Selection  │   │
    │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘   │
    └────────────────────────────────────────────────────────────────────────┘
         │
         ▼
    ┌────────────────────────────────────────────────────────────────────────┐
    │                         EXECUTION ENGINE                                │
    │                                                                         │
    │     Phase 1 ──► Phase 2 ──► ... ──► Phase N ──► Synthesis              │
    │        │           │                   │             │                  │
    │     [Gate]      [Gate]              [Gate]      [Verify]               │
    │                                                                         │
    │     Attack ──► Fix ──► Verify (per phase as needed)                    │
    │                                                                         │
    └────────────────────────────────────────────────────────────────────────┘
         │
         ▼
    ┌────────────────────────────────────────────────────────────────────────┐
    │                       VERIFICATION ENGINE                               │
    │                                                                         │
    │     Chain A ─┬─► Chain Aggregation ─► Uncertainty ─► Confidence        │
    │     Chain B ─┤                                                          │
    │     Chain C ─┤                                                          │
    │     Chain D ─┤                                                          │
    │     Chain E ─┘                                                          │
    │                                                                         │
    └────────────────────────────────────────────────────────────────────────┘
         │
         ▼
    ┌─────────┐
    │ OUTPUT  │
    │  WITH   │
    │CONFIDENCE
    └────┬────┘
         │
         ▼
    ┌────────────────────────────────────────────────────────────────────────┐
    │                        META-ANALYSIS LAYER                              │
    │                                                                         │
    │  MAL-COVERAGE  MAL-QUALITY  MAL-EFFICIENCY  MAL-NOVELTY  MAL-CONV     │
    │       │             │             │              │            │         │
    │       └─────────────┴──────┬──────┴──────────────┴────────────┘         │
    │                            ▼                                            │
    │                   IMPROVEMENT PROPOSALS                                 │
    │                            │                                            │
    │                   SELF-EVOLUTION ENGINE                                 │
    │                                                                         │
    └────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════
```

---

## 2. Initialization Phase

### 2.1 Task Receipt

```yaml
task_receipt:
  inputs:
    task_description:
      type: "Text"
      required: true
      content: "Problem statement, requirements, context"

    user_context:
      type: "Structured"
      optional: true
      content: "User preferences, constraints, prior interactions"

    explicit_parameters:
      type: "Structured"
      optional: true
      content:
        - precision_override: "User-specified precision level"
        - domain_hints: "User-specified domain hints"
        - output_format: "Desired output format"
        - deadline: "Time constraints"

  preprocessing:
    normalization: "Standardize input format"
    validation: "Verify input completeness"
    enhancement: "Extract implicit requirements"
```

### 2.2 Domain Detection

```yaml
domain_detection:
  source: "domain-adaptation/DOMAIN-DETECTOR.md"

  execution:
    1: "Extract signals (lexical, structural, semantic)"
    2: "Fuse signals into domain scores"
    3: "Traverse taxonomy to find primary domain"
    4: "Identify secondary domains"
    5: "Calculate confidence"

  output:
    domain_profile:
      primary: "T.SEC.CRY.SYM"
      secondary: ["T.NET.PRO", "T.DEV.SYS"]
      confidence: 0.92

  time_budget: "< 100ms typical"
```

### 2.3 Precision Calibration

```yaml
precision_calibration:
  source: "precision/PRECISION-CALIBRATOR.md"

  execution:
    1: "Extract task context factors"
    2: "Score each precision factor (CS, DC, AE, VA, TC)"
    3: "Calculate base precision level"
    4: "Apply override rules"
    5: "Generate precision configuration"

  output:
    precision_level: "PL3"
    configuration:
      methods_enabled: ["formal_spec", "proof_sketches", "model_checking"]
      chains_required: "4/5"
      confidence_target: 0.95

  time_budget: "< 50ms"
```

### 2.4 Expert Panel Generation

```yaml
expert_generation:
  source: "domain-adaptation/EXPERT-GENERATOR.md"

  execution:
    1: "Calculate panel size from complexity"
    2: "Determine archetype distribution"
    3: "Synthesize personas for each slot"
    4: "Assign panel roles (LEAD, SYNTHESIZER, CONTRIBUTOR)"
    5: "Validate panel completeness and diversity"

  output:
    panel:
      size: 11
      experts:
        - name: "Dr. Marcus Chen"
          archetype: "ARC-AD"
          role: "CONTRIBUTOR"
          # ... full persona
        # ... more experts

  time_budget: "< 200ms"
```

### 2.5 Template Selection

```yaml
template_selection:
  source: "core/PHASE-TEMPLATES.md"

  execution:
    1: "Match primary domain to template"
    2: "Identify secondary domain templates"
    3: "Fuse templates if multiple apply"
    4: "Adapt template to precision level"
    5: "Generate execution plan"

  output:
    template: "TMPL-SEC"
    phases:
      - phase: 0, name: "Initialization", duration: 0.05
      - phase: 1, name: "Attack Surface Analysis", duration: 0.15
      # ... remaining phases
    total_phases: 7

  time_budget: "< 50ms"
```

### 2.6 Resource Budgets and Timeouts

```yaml
resource_budgets:
  purpose: "Prevent runaway execution and ensure predictable performance"

  global_limits:
    max_total_duration:
      by_precision:
        PL1: "30 minutes"
        PL2: "2 hours"
        PL3: "8 hours"
        PL4: "24 hours"
        PL5: "72 hours (with checkpoints)"
      enforcement: "Hard limit, graceful degradation on approach"

    max_iterations_total:
      default: 100
      by_mode:
        fast: 20
        standard: 50
        deep: 200
      enforcement: "Trigger convergence review at 80%"

  per_phase_limits:
    max_phase_duration:
      calculation: "total_budget × phase_weight"
      default_weight: "1 / num_phases"
      override: "Phase templates can specify custom weights"

    max_phase_iterations:
      default: 10
      by_precision:
        PL1: 3
        PL2: 5
        PL3: 10
        PL4: 15
        PL5: 25

    stall_detection:
      trigger: "No progress for 3 consecutive iterations"
      actions:
        - "Upgrade precision if room"
        - "Add expert to panel"
        - "Force synthesis"
        - "Graceful degradation"

  checkpoint_protocol:
    frequency: "Every 25% of phase budget consumed"
    captures:
      - "Current state"
      - "Progress metrics"
      - "Remaining budget"
    actions:
      - "Save recoverable checkpoint"
      - "Assess progress rate"
      - "Adjust strategy if needed"

  graceful_degradation:
    trigger: "Budget exhaustion imminent (< 10% remaining)"
    protocol:
      1: "Complete current iteration"
      2: "Force synthesis with available findings"
      3: "Mark output as resource-limited"
      4: "Document what was not completed"
      5: "Provide recommendations for follow-up"
```

---

## 3. Execution Phase

### 3.1 Phase Execution Loop

```yaml
phase_execution:
  main_loop:
    ```
    FOR EACH phase IN template.phases:

      // Phase Entry
      validate_gate(previous_phase)
      prepare_phase_context(phase)
      activate_relevant_experts(phase.expert_focus)

      // Phase Iteration Loop
      iteration = 0
      converged = false

      WHILE NOT converged AND iteration < max_iterations:

        // Expert Contribution Round
        FOR EACH expert IN active_experts:
          contribution = expert.analyze(context)
          contributions.append(contribution)

        // Synthesis
        synthesis = synthesizer.integrate(contributions)

        // Check for Attack-Fix-Verify cycle
        IF phase.requires_afv:
          afv_result = execute_afv_cycle(synthesis)
          synthesis = afv_result.synthesis

        // Convergence Check
        converged = check_convergence(synthesis, phase.convergence_criteria)

        iteration += 1
        update_context(synthesis)

      // Phase Exit
      phase_output = finalize_phase(synthesis)
      evaluate_gate(phase.gate)
    ```
```

### 3.2 Attack-Fix-Verify Cycle

```yaml
attack_fix_verify:
  description: "Core adversarial improvement cycle"

  attack_phase:
    actors: "ARC-AD experts"
    activities:
      - "Identify weaknesses in current state"
      - "Construct attack scenarios"
      - "Challenge assumptions"
      - "Find edge cases"
    output: "List of issues with severity"

  fix_phase:
    actors: "ARC-IM, ARC-TH experts"
    activities:
      - "Address identified issues"
      - "Propose mitigations"
      - "Strengthen weak points"
      - "Document fixes"
    output: "Updated solution with fixes"

  verify_phase:
    actors: "ARC-QA, ARC-TH experts"
    activities:
      - "Verify fixes address issues"
      - "Check for regressions"
      - "Validate no new issues introduced"
      - "Update confidence"
    output: "Verified state with confidence"

  cycle_termination:
    conditions:
      - "No new HIGH/CRITICAL issues for N cycles"
      - "Maximum iterations reached"
      - "Confidence target achieved"
```

### 3.3 Gate Evaluation

```yaml
gate_evaluation:
  gate_check:
    inputs:
      - phase_outputs: "What the phase produced"
      - gate_criteria: "What's required to pass"
      - precision_level: "Strictness of evaluation"

    evaluation:
      completeness: "Are all required outputs present?"
      quality: "Do outputs meet quality standards?"
      confidence: "Is confidence at or above threshold?"
      coverage: "Are there gaps?"

    outcomes:
      PASS:
        action: "Proceed to next phase"
        documentation: "Record gate passage"

      CONDITIONAL_PASS:
        action: "Proceed with caveats"
        documentation: "Document conditions, flag for review"

      FAIL:
        action: "Return to phase"
        guidance: "Specific areas needing work"
        max_retries: 3

      ESCALATE:
        action: "Upgrade precision or request help"
        trigger: "Multiple failures or fundamental issue"
```

### 3.4 Convergence Detection

```yaml
convergence_detection:
  metrics:
    position_stability:
      description: "Experts stop changing positions"
      measurement: "Position change rate < threshold"

    issue_discovery:
      description: "No new significant issues"
      measurement: "New HIGH+ issues = 0 for N cycles"

    confidence_plateau:
      description: "Confidence stabilized"
      measurement: "Confidence change < 1% for N cycles"

    synthesis_stability:
      description: "Synthesis not changing"
      measurement: "Synthesis diff < threshold"

  convergence_criteria:
    by_precision:
      PL1: "Position stability OR 2 iterations"
      PL2: "Position stability AND issue discovery"
      PL3: "All metrics stable for 2 cycles"
      PL4: "All metrics stable for 3 cycles"
      PL5: "All metrics stable AND external validation"
```

---

## 4. Verification Phase

### 4.1 Chain Execution

```yaml
chain_execution:
  source: "precision/VERIFICATION-CHAINS.md"

  execution:
    parallel_phase:
      chains: ["CHAIN-A", "CHAIN-B", "CHAIN-D"]
      strategy: "Execute in parallel"

    sequential_phase:
      chains: ["CHAIN-C"]
      dependencies: "May use parallel phase findings"

    review_phase:
      chains: ["CHAIN-E"]
      strategy: "Reviews all prior chains"

  per_chain:
    1: "Scope determination"
    2: "Method selection"
    3: "Analysis execution"
    4: "Finding documentation"
    5: "Confidence calculation"
```

### 4.2 Aggregation and Uncertainty

```yaml
aggregation:
  source: "precision/UNCERTAINTY-QUANTIFICATION.md"

  execution:
    1: "Collect all chain verdicts"
    2: "Check chain independence"
    3: "Calculate agreement level"
    4: "Aggregate confidence"
    5: "Decompose uncertainty"
    6: "Calibrate confidence"
    7: "Generate uncertainty profile"

  output:
    final_confidence: 0.92
    uncertainty_profile:
      epistemic: "Low"
      aleatory: "Moderate"
      model: "Low"
      key_assumptions: [...]
```

---

## 5. Output Generation

### 5.1 Output Assembly

```yaml
output_assembly:
  components:
    primary_output:
      content: "Main analysis/findings/recommendations"
      format: "Determined by template and user preference"

    confidence_section:
      content: "Confidence score and uncertainty profile"
      format: "Standardized uncertainty report"

    methodology_section:
      content: "How analysis was conducted"
      format: "Phase summary, expert panel, methods used"

    assumptions_section:
      content: "Key assumptions and limitations"
      format: "Structured assumption list with sensitivity"

    recommendations_section:
      content: "Actionable next steps"
      format: "Prioritized recommendation list"

  assembly_order:
    1: "Executive summary (if applicable)"
    2: "Primary findings"
    3: "Detailed analysis"
    4: "Confidence and uncertainty"
    5: "Assumptions and limitations"
    6: "Recommendations"
    7: "Methodology appendix"
```

### 5.2 Output Validation

```yaml
output_validation:
  checks:
    completeness:
      - "All required sections present"
      - "All claims have evidence"
      - "All recommendations have rationale"

    consistency:
      - "No contradictions between sections"
      - "Confidence matches analysis depth"
      - "Recommendations align with findings"

    quality:
      - "Meets precision level requirements"
      - "Uncertainty properly characterized"
      - "Actionable for intended audience"

  validation_failure:
    action: "Return to execution for refinement"
    documentation: "Record validation issues"
```

---

## 6. Meta-Analysis Phase

### 6.1 Post-Task Analysis

```yaml
post_task_analysis:
  trigger: "Task completion"

  agent_execution:
    parallel:
      - "MAL-COVERAGE: Domain coverage analysis"
      - "MAL-QUALITY: Output quality assessment"
      - "MAL-EFFICIENCY: Resource usage analysis"
      - "MAL-NOVELTY: Innovation tracking"

    sequential:
      - "MAL-CONVERGENCE: Convergence pattern analysis"
      - "MAL-ADVERSARIAL: Challenge effectiveness"

    synthesis:
      - "Aggregate findings"
      - "Generate improvement proposals"
      - "Update metrics"
```

### 6.2 Improvement Processing

```yaml
improvement_processing:
  source: "self-evolution/IMPROVEMENT-PROTOCOL.md"

  execution:
    1: "Receive proposals from MAL agents"
    2: "Classify proposals by category and risk"
    3: "Queue for validation"
    4: "Execute validation pipeline"
    5: "Route through approval workflow"
    6: "Apply approved improvements"
    7: "Update version lineage"
```

---

## 7. Execution Modes

### 7.1 Standard Mode

```yaml
standard_mode:
  description: "Full execution with all components"
  use_case: "Normal analysis tasks"

  flow:
    initialization: "Complete"
    execution: "All phases"
    verification: "Full chain verification"
    meta_analysis: "Enabled"
```

### 7.2 Fast Mode

```yaml
fast_mode:
  description: "Accelerated execution with reduced depth"
  use_case: "Time-sensitive tasks, preliminary analysis"

  flow:
    initialization: "Streamlined"
    execution:
      - "Condensed phases"
      - "Reduced iterations"
      - "Simplified convergence"
    verification: "Reduced chains (3 instead of 5)"
    meta_analysis: "Lightweight"

  constraints:
    max_precision: "PL2"
    explicit_confidence_caveat: true
```

### 7.3 Deep Mode

```yaml
deep_mode:
  description: "Maximum depth analysis"
  use_case: "Critical systems, formal verification"

  flow:
    initialization: "Comprehensive"
    execution:
      - "Extended phases"
      - "Increased iterations"
      - "Strict convergence"
    verification: "All chains at maximum depth"
    meta_analysis: "Full with external validation"

  constraints:
    min_precision: "PL4"
    external_review: "Required for PL5"
```

### 7.4 Incremental Mode

```yaml
incremental_mode:
  description: "Build on previous analysis"
  use_case: "Updates, refinements, follow-up questions"

  flow:
    initialization:
      - "Load previous execution context"
      - "Identify changed inputs"
      - "Determine delta scope"
    execution:
      - "Execute only affected phases"
      - "Preserve unchanged analysis"
    verification: "Re-verify changed components"
    meta_analysis: "Focus on changes"

  benefits:
    - "Faster than full re-execution"
    - "Preserves prior work"
    - "Focuses on what's new"
```

### 7.5 Automatic Mode Selection

```yaml
mode_auto_selection:
  purpose: "Intelligently select execution mode based on task characteristics"

  selection_algorithm:
    inputs:
      - task_characteristics: "From precision calibrator"
      - user_context: "History, preferences, urgency"
      - resource_availability: "Current system load"

    rules:
      fast_mode_triggers:
        - condition: "TC (time_criticality) >= 4"
          weight: 0.8
        - condition: "user_explicit_fast_request"
          weight: 1.0
        - condition: "task_type == 'preliminary_analysis'"
          weight: 0.7
        - condition: "precision_override <= PL2"
          weight: 0.6

      deep_mode_triggers:
        - condition: "CS (consequence_severity) >= 4"
          weight: 0.7
        - condition: "domain IN safety_critical_domains"
          weight: 0.9
        - condition: "precision_level >= PL4"
          weight: 0.8
        - condition: "user_explicit_deep_request"
          weight: 1.0

      incremental_mode_triggers:
        - condition: "prior_task_exists AND task_similarity > 0.7"
          weight: 0.9
        - condition: "user_explicit_update_request"
          weight: 1.0
        - condition: "delta_scope_identifiable"
          weight: 0.8

      standard_mode_default:
        condition: "No strong triggers for other modes"
        threshold: "Highest trigger weight < 0.6"

    selection_process:
      1: "Calculate trigger weights for each mode"
      2: "Select mode with highest aggregate weight"
      3: "Apply user override if specified"
      4: "Validate mode is compatible with precision level"
      5: "Return selected mode with rationale"

  mode_compatibility:
    fast_deep_conflict:
      resolution: "Deep mode takes priority (safety over speed)"
      notification: "Inform user of mode elevation"

    incremental_requirements:
      prerequisite: "Valid prior task context must exist"
      fallback: "Standard mode if incremental unavailable"

  user_override:
    permitted: true
    constraints:
      - "Cannot downgrade from deep mode for safety-critical tasks"
      - "Must acknowledge tradeoffs"
```

### 7.6 Behavioral Modes (SKYNET Integration)

```yaml
behavioral_modes:
  source: "SKYNET Integration - SuperClaude_Framework patterns"
  purpose: "Adapt execution behavior to task context"

  brainstorming_mode:
    description: "Divergent thinking for creative exploration"
    activation_triggers:
      - "Ideation tasks"
      - "Open-ended problem exploration"
      - "Requirements gathering"
    behavior:
      output_style: "Many options, questions, alternatives"
      convergence: "Delayed - encourage divergence first"
      expert_mix: "Heavy ARC-TH (Theoretical)"
    usf_phase_mapping: "Phase 1 Divergence"

  business_panel_mode:
    description: "Multi-expert strategic analysis"
    activation_triggers:
      - "Business decisions"
      - "Strategic planning"
      - "Stakeholder analysis"
    behavior:
      output_style: "Multiple expert perspectives synthesized"
      convergence: "Structured debate → consensus"
      expert_mix: ["ARC-ST", "ARC-TH", "ARC-AD", "ARC-IM"]
    usf_phase_mapping: "Multi-phase synthesis"

  deep_research_mode:
    description: "Thorough autonomous investigation"
    activation_triggers:
      - "Research tasks"
      - "PL3+ precision requirements"
      - "Unknown domain exploration"
    behavior:
      output_style: "Comprehensive, cited, thorough"
      convergence: "Strict - require multiple sources"
      expert_mix: "Heavy ARC-TH + ARC-QA"
    verification_chain: "CHAIN-D Empirical primary"

  orchestration_mode:
    description: "Multi-tool coordination"
    activation_triggers:
      - "Complex multi-step tasks"
      - "Cross-component coordination"
      - "Tool-heavy workflows"
    behavior:
      output_style: "Efficient tool chaining"
      convergence: "Progress-oriented"
      expert_mix: "Heavy ARC-IM (Implementation)"
    resource_aware: true

  token_efficiency_mode:
    description: "Context-aware concise output"
    activation_triggers:
      - "Long tasks approaching context limit"
      - "Context utilization > 70%"
      - "Explicit efficiency request"
    behavior:
      output_style: "Concise, focused, minimal verbosity"
      convergence: "Accelerated"
      expert_mix: "Reduced panel size"
    performance_impact:
      token_reduction: "30-50%"
      quality_tradeoff: "Minimal when applied correctly"

  task_management_mode:
    description: "Systematic organization and tracking"
    activation_triggers:
      - "Multi-step tasks"
      - "Project-level work"
      - "Todo-heavy workflows"
    behavior:
      output_style: "Structured planning, checklists"
      convergence: "Milestone-based"
      expert_mix: "Heavy ARC-ST (Strategic)"
    todo_integration: true

  introspection_mode:
    description: "Meta-cognitive analysis and self-improvement"
    activation_triggers:
      - "Self-improvement requests"
      - "Methodology review"
      - "Quality retrospectives"
    behavior:
      output_style: "Analytical, critical, reflective"
      convergence: "Thorough self-examination"
      expert_mix: "All archetypes for balance"
    mal_integration: true  # Feeds into MAL agents

  mode_conflict_resolution:
    priority_hierarchy:
      1: token_efficiency  # Resource constraints take precedence
      2: deep_research     # Quality requirements
      3: task_management   # Structure requirements
      4: orchestration     # Coordination needs
      5: business_panel    # Multi-expert analysis
      6: brainstorming     # Creative exploration
      7: introspection     # Meta-cognitive (lowest)

    resolution_rules:
      single_mode: "If one mode clearly matches, use it"
      multiple_modes: "Higher priority mode wins"
      user_override: "User can force specific mode via explicit request"

    mode_combinations:
      allowed:
        - [task_management, orchestration]  # Structure + coordination
        - [deep_research, introspection]    # Research + reflection
      disallowed:
        - [token_efficiency, deep_research]  # Contradictory
        - [brainstorming, task_management]   # Divergent vs structured

  mode_selection_logic:
    automatic:
      priority_order:
        1: "token_efficiency_mode (if context pressure)"
        2: "User-specified mode"
        3: "Task-inferred mode"
        4: "Default to standard execution"

    combination_allowed:
      - "token_efficiency + any other mode"
      - "task_management + orchestration"
      - "deep_research + introspection"

    mutual_exclusion:
      - "brainstorming ↔ deep_research (conflicting convergence)"
```

### 7.7 Development Workflow Template (SKYNET Integration)

```yaml
development_workflow:
  source: "SKYNET Integration - Anthropic Best Practices"
  name: "Explore → Plan → Code → Commit"

  phases:
    explore:
      description: "Understand before acting"
      critical: true
      activities:
        - "Read relevant files without writing code"
        - "Map dependencies and relationships"
        - "Identify constraints and requirements"
      anti_pattern: "Jumping straight to coding"
      gate: "Understanding confirmed"
      duration_weight: 0.15

    plan:
      description: "Design before implementing"
      activities:
        - "Create structured plan"
        - "Identify risks and mitigations"
        - "Define success criteria"
      think_level: "think hard or higher"
      output: "Actionable implementation steps"
      gate: "Plan reviewed and approved"
      duration_weight: 0.20

    code:
      description: "Implement with verification"
      activities:
        - "Implement planned changes"
        - "Verify at checkpoints"
        - "Run tests after changes"
      checkpoints: "After each significant change"
      gate: "All tests passing"
      duration_weight: 0.50

    commit:
      description: "Document and finalize"
      activities:
        - "Create meaningful commit message"
        - "Update documentation"
        - "Prepare for review"
      requirement: "Meaningful commit messages"
      gate: "PR approved or ready for review"
      duration_weight: 0.15

  workflow_integration:
    with_behavioral_modes:
      explore: "Can use deep_research_mode"
      plan: "Can use brainstorming_mode → task_management_mode"
      code: "Can use orchestration_mode"
      commit: "Standard execution"

    with_precision_levels:
      PL1-PL2: "Condensed workflow (explore + code + commit)"
      PL3: "Full workflow"
      PL4-PL5: "Extended workflow (multiple plan/code iterations)"
```

---

## 8. Error Handling

### 8.1 Error Categories

```yaml
error_categories:
  recoverable:
    convergence_failure:
      description: "Phase fails to converge"
      recovery: "Upgrade precision, add experts, extend iterations"

    gate_failure:
      description: "Phase fails gate criteria"
      recovery: "Return to phase with guidance"

    chain_disagreement:
      description: "Verification chains disagree"
      recovery: "Expert adjudication, additional chain"

  non_recoverable:
    domain_unrecognized:
      description: "Cannot classify domain"
      recovery: "Request user clarification"

    resource_exhaustion:
      description: "Exceeded resource limits"
      recovery: "Report with partial results"

    fundamental_ambiguity:
      description: "Task cannot be resolved"
      recovery: "Report ambiguity, request clarification"
```

### 8.2 Graceful Degradation

```yaml
graceful_degradation:
  principle: "Return best possible result even on partial failure"

  strategies:
    reduce_scope:
      trigger: "Resource constraints"
      action: "Complete subset of analysis"
      documentation: "Document what was completed vs planned"

    reduce_precision:
      trigger: "Cannot achieve target precision"
      action: "Complete at achievable precision"
      documentation: "Document precision shortfall"

    partial_verification:
      trigger: "Some chains fail"
      action: "Report with available chain results"
      documentation: "Document verification gaps"
```

---

## 9. Performance Optimization

### 9.1 Parallelization

```yaml
parallelization:
  opportunities:
    initialization: "Domain detection || Precision calibration"
    execution: "Independent expert analysis"
    verification: "Chains A, B, D in parallel"
    meta_analysis: "All MAL agents in parallel"

  constraints:
    dependencies: "Respect data dependencies"
    resources: "Balance parallel load"
    coherence: "Maintain state consistency"
```

### 9.2 Caching

```yaml
caching:
  cached_items:
    domain_prototypes: "Pre-computed embeddings"
    expert_templates: "Base persona templates"
    pattern_library: "Cross-domain patterns"
    recent_results: "Recent task results"

  cache_invalidation:
    version_change: "Clear on USF version change"
    ttl_expiry: "Time-based expiration"
    explicit_invalidation: "Manual cache clear"
```

---

## Appendix A: Execution Flow Quick Reference

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                     USF 4.0 EXECUTION FLOW REFERENCE                         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  INITIALIZATION: Domain → Precision → Experts → Template                    ║
║                                                                              ║
║  EXECUTION: Phase Loop with Attack-Fix-Verify cycles, Gate checks           ║
║                                                                              ║
║  VERIFICATION: 5 Chains → Aggregation → Uncertainty → Confidence            ║
║                                                                              ║
║  OUTPUT: Primary + Confidence + Methodology + Assumptions + Recommendations ║
║                                                                              ║
║  META-ANALYSIS: MAL agents → Improvement proposals → Self-evolution         ║
║                                                                              ║
║  MODES: Standard | Fast | Deep | Incremental                                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## Appendix B: Change Log

| Version | Date | Changes |
|---------|------|---------|
| 4.0.0 | 2025-12-10 | Initial USF 4.0 execution flow specification |
| 4.0.1 | 2025-12-10 | Added resource budgets (2.6), mode auto-selection (7.5) per Cycle 2 red team |
| 4.1.0 | 2025-12-10 | SKYNET Integration: Added 7 behavioral modes (7.6), development workflow template (7.7) |
| 4.1.1 | 2025-12-10 | Fixed HIGH-009: Added mode conflict resolution with priority hierarchy and combination rules (7.6) |

---

*This document is part of the USF 4.0 specification suite. See MASTER-SPECIFICATION.md for framework overview.*
