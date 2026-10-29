# USF 4.0: Improvement Protocol

> **Version**: 4.0.0 (See VERSION.yaml)
> **Component**: Self-Evolution / Improvement Protocol
> **Status**: Specification
> **Dependencies**: META-ANALYSIS-AGENTS.md, VERSION-LINEAGE.md, BOOTSTRAP-PROTOCOL.md
> **Last Updated**: 2025-12-10

---

## 1. Overview

The Improvement Protocol governs how USF 4.0 evolves through self-modification. It ensures improvements are valid, beneficial, safe, and properly integrated while maintaining system integrity and avoiding regression.

```
IMPROVEMENT LIFECYCLE
═══════════════════════════════════════════════════════════════════════════════

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                     META-ANALYSIS AGENTS                                │
    │                                                                         │
    │   MAL-COVERAGE  MAL-QUALITY  MAL-EFFICIENCY  MAL-NOVELTY  MAL-CONV     │
    │        │             │             │             │             │       │
    │        └─────────────┴─────────────┴─────────────┴─────────────┘       │
    │                                    │                                    │
    └────────────────────────────────────┼────────────────────────────────────┘
                                         │
                                         ▼
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ PHASE 1: PROPOSAL GENERATION                                            │
    │   • Structure improvement proposals                                     │
    │   • Classify by type and risk                                          │
    │   • Initial feasibility check                                          │
    └─────────────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ PHASE 2: VALIDATION                                                     │
    │   • External anchor validation                                          │
    │   • Historical regression testing                                       │
    │   • Adversarial stress testing                                         │
    │   • Safety constraint verification                                      │
    └─────────────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ PHASE 3: A/B TESTING                                                    │
    │   • Parallel execution with/without improvement                         │
    │   • Statistical significance testing                                    │
    │   • Quality delta measurement                                          │
    └─────────────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ PHASE 4: APPROVAL                                                       │
    │   • Bootstrap phase determines approval path                            │
    │   • Human approval (early phases)                                       │
    │   • Automatic approval (mature phases)                                 │
    └─────────────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ PHASE 5: INTEGRATION                                                    │
    │   • Apply improvement to USF                                           │
    │   • Update version lineage                                             │
    │   • Monitor for regression                                             │
    └─────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════
```

---

## 2. Improvement Categories

### 2.1 Category Definitions

```yaml
improvement_categories:
  TAXONOMY:
    description: "Changes to domain classification"
    examples:
      - "Add new domain category"
      - "Refine domain boundaries"
      - "Update domain terminology"
    default_risk: LOW
    typical_scope: "Localized to taxonomy"

  TEMPLATE:
    description: "Changes to phase templates"
    examples:
      - "Add new phase to template"
      - "Modify phase activities"
      - "Adjust gate criteria"
    default_risk: MEDIUM
    typical_scope: "Affects domain-specific execution"

  ARCHETYPE:
    description: "Changes to expert archetypes"
    examples:
      - "Refine archetype attributes"
      - "Add new archetype"
      - "Modify persona synthesis"
    default_risk: MEDIUM
    typical_scope: "Affects all panels"

  PRECISION:
    description: "Changes to precision calibration"
    examples:
      - "Adjust precision calculation formula"
      - "Modify level thresholds"
      - "Update method availability"
    default_risk: HIGH
    typical_scope: "Affects all task execution"

  VERIFICATION:
    description: "Changes to verification processes"
    examples:
      - "Modify chain requirements"
      - "Adjust convergence criteria"
      - "Add new verification method"
    default_risk: HIGH
    typical_scope: "Affects confidence guarantees"

  PROCESS:
    description: "Changes to execution flow"
    examples:
      - "Modify iteration logic"
      - "Adjust parallelization"
      - "Change phase sequencing"
    default_risk: MEDIUM
    typical_scope: "Affects execution efficiency"

  META:
    description: "Changes to self-evolution components"
    examples:
      - "Modify MAL agent behavior"
      - "Adjust improvement protocol"
      - "Change bootstrap phases"
    default_risk: CRITICAL
    typical_scope: "Affects self-improvement capability"

    # CRITICAL CONSTRAINT: Cross-Agent Requirement
    special_constraints:
      self_modification_prohibition:
        rule: "A MAL agent CANNOT propose improvements to its own specification"
        rationale: "Prevents self-interested modifications that could compromise oversight"
        enforcement:
          - "MAL-X cannot generate proposals for MAL-X specification"
          - "Cross-agent improvements only (MAL-A improves MAL-B)"
          - "Violation detection in proposal validation"

      meta_improvement_approval:
        rule: "ALL meta improvements require Phase 1 approval process"
        rationale: "Meta-level changes affect self-improvement capability itself"
        enforcement:
          - "Even in Phase 4, META category uses Phase 1 workflow"
          - "Human authority sign-off required"
          - "External review recommended"

      bootstrap_immunity:
        rule: "Bootstrap Protocol cannot be modified by USF self-improvement"
        rationale: "Foundation of trust model must be externally controlled"
        modification_path: "External human-only process"
```

### 2.2 Risk Classification

```
RISK CLASSIFICATION MATRIX
═══════════════════════════════════════════════════════════════════════════════

Risk Level │ Definition                        │ Approval Path  │ Rollback
───────────┼───────────────────────────────────┼────────────────┼───────────
LOW        │ Minor adjustments, localized      │ Auto (Phase 2+)│ Immediate
           │ impact, easily reversible         │                │
───────────┼───────────────────────────────────┼────────────────┼───────────
MEDIUM     │ Moderate changes, affects         │ Auto (Phase 3+)│ Fast
           │ multiple components               │                │
───────────┼───────────────────────────────────┼────────────────┼───────────
HIGH       │ Significant changes, affects      │ Auto (Phase 4+)│ Planned
           │ core guarantees                   │                │
───────────┼───────────────────────────────────┼────────────────┼───────────
CRITICAL   │ Fundamental changes, affects      │ Human required │ Emergency
           │ self-evolution capability         │ always         │

═══════════════════════════════════════════════════════════════════════════════
```

---

## 3. Proposal Generation

### 3.1 Proposal Structure

```yaml
improvement_proposal:
  # Identification
  proposal_id: "IMP-{category}-{timestamp}-{hash}"
  source_agent: "MAL-* that generated the proposal"
  generation_time: "ISO8601 timestamp"

  # Classification
  category: "TAXONOMY|TEMPLATE|ARCHETYPE|PRECISION|VERIFICATION|PROCESS|META"
  risk_level: "LOW|MEDIUM|HIGH|CRITICAL"
  affected_components: ["List of impacted specifications"]

  # Description
  title: "Brief improvement title"
  description: "Detailed description of the improvement"
  rationale: "Why this improvement is needed"
  expected_benefit: "Quantified expected improvement"

  # Evidence
  evidence:
    source_data: "Data that prompted this proposal"
    supporting_analysis: "Analysis backing the proposal"
    historical_context: "Past related improvements"

  # Specification
  current_state:
    specification: "Reference to current spec"
    content: "Current content being modified"

  proposed_state:
    modification_type: "ADD|MODIFY|REMOVE|REPLACE"
    content: "Proposed new content"
    diff: "Structured difference from current"

  # Validation Plan
  validation_plan:
    external_anchors: "Ground truth for validation"
    regression_tests: "Tests to prevent regression"
    a_b_test_design: "A/B test specification"
    success_criteria: "Quantified success metrics"

  # Risk Assessment
  risk_assessment:
    potential_negative_impacts: ["List of potential harms"]
    mitigation_strategies: ["How to prevent/address harms"]
    rollback_plan: "How to undo if needed"
    monitoring_plan: "Post-deployment monitoring"
```

### 3.2 Proposal Generation Protocol

```
PROPOSAL GENERATION PROTOCOL
═══════════════════════════════════════════════════════════════════════════════

Step 1: Finding Aggregation
  • Collect findings from all MAL agents
  • Deduplicate similar findings
  • Cluster related findings

Step 2: Improvement Ideation
  FOR EACH finding_cluster:
    • Identify root cause
    • Generate candidate solutions (≥2)
    • Preliminary feasibility assessment
    • Select most promising candidate

Step 3: Proposal Formulation
  FOR EACH selected_candidate:
    • Structure as formal proposal
    • Define current vs proposed state
    • Specify validation plan
    • Assess and document risks

Step 4: Initial Filtering
  REJECT proposals that:
    • Violate safety constraints
    • Have no clear benefit
    • Cannot be validated
    • Duplicate recent proposals
    • Conflict with pending proposals

Step 5: Prioritization
  RANK proposals by:
    • Expected benefit magnitude
    • Confidence in benefit
    • Implementation cost
    • Risk-adjusted value

OUTPUT: Prioritized proposal queue

═══════════════════════════════════════════════════════════════════════════════
```

---

## 4. Validation Framework

### 4.1 External Anchor Validation

Improvements must be validated against external ground truth to prevent self-referential drift:

```yaml
external_anchor_validation:
  anchor_types:
    academic_literature:
      description: "Published peer-reviewed research"
      application:
        - "Theoretical claims validated against papers"
        - "Methods compared to established approaches"
        - "Metrics benchmarked against reported results"
      weight: 0.3

    industry_standards:
      description: "Industry best practices and standards"
      application:
        - "Security improvements against NIST, OWASP, etc."
        - "Process improvements against ISO, CMMI, etc."
        - "Quality standards compliance"
      weight: 0.25

    known_ground_truth:
      description: "Problems with verified correct answers"
      application:
        - "Test on problems with known solutions"
        - "Compare outputs to correct answers"
        - "Measure accuracy improvement"
      weight: 0.3

    expert_review:
      description: "External human expert assessment"
      application:
        - "Domain expert reviews proposed changes"
        - "Validates reasoning quality"
        - "Checks for overlooked issues"
      weight: 0.15

  validation_process:
    1. "Identify relevant anchors for improvement type"
    2. "Collect anchor data/opinions"
    3. "Compare proposed improvement against anchors"
    4. "Calculate anchor alignment score"
    5. "Flag conflicts with anchors"

  passing_criteria:
    minimum_alignment: 0.7  # Weighted average of anchor scores
    no_critical_conflicts: true
    expert_approval: "Required for HIGH/CRITICAL risk"
```

### 4.2 Historical Regression Testing

```yaml
regression_testing:
  test_suite_composition:
    historical_tasks:
      description: "Representative past tasks"
      selection:
        - "Stratified by domain"
        - "Includes edge cases"
        - "Includes previously failed tasks"
      count: "≥50 tasks for statistically valid comparison"

    regression_markers:
      description: "Specific known cases that must not regress"
      selection:
        - "Tasks where USF previously excelled"
        - "Tasks that revealed past bugs (now fixed)"
        - "Tasks with verified correct outputs"

    stress_tests:
      description: "Edge cases and adversarial inputs"
      selection:
        - "Maximum complexity tasks"
        - "Minimum information tasks"
        - "Adversarial task formulations"

  testing_protocol:
    1. "Execute test suite with current USF"
    2. "Record baseline performance"
    3. "Execute test suite with proposed improvement"
    4. "Record improved performance"
    5. "Statistical comparison"

  passing_criteria:
    no_regression:
      definition: "No statistically significant decrease"
      threshold: "p < 0.05 for regression detection"

    improvement_detected:
      definition: "Statistically significant improvement in target area"
      threshold: "p < 0.05, effect size > 0.1"

    regression_markers_pass:
      definition: "All regression markers maintain quality"
      threshold: "100% pass rate"
```

### 4.3 Adversarial Stress Testing

```yaml
adversarial_stress_testing:
  purpose: "Ensure improvement doesn't introduce exploitable weaknesses"

  test_categories:
    input_manipulation:
      description: "Adversarial input crafting"
      tests:
        - "Ambiguous task formulations"
        - "Contradictory requirements"
        - "Incomplete information"
        - "Misleading context"

    edge_case_exploration:
      description: "Boundary condition testing"
      tests:
        - "Empty inputs"
        - "Maximum complexity inputs"
        - "Novel domain combinations"
        - "Extreme precision level requests"

    failure_mode_probing:
      description: "Deliberate failure induction"
      tests:
        - "Timeout behavior"
        - "Resource exhaustion"
        - "Circular dependencies"
        - "Conflicting expert opinions"

    meta_attack:
      description: "Attacks on self-improvement"
      tests:
        - "Improvement proposals that degrade system"
        - "Proposals that bypass validation"
        - "Proposals that corrupt versioning"
        - "Proposals that disable meta-analysis"

  passing_criteria:
    resilience_maintained: "No new failure modes introduced"
    graceful_degradation: "Failures are handled gracefully"
    no_meta_vulnerabilities: "Self-improvement remains protected"
```

### 4.4 Safety Constraint Verification

```yaml
safety_constraints:
  core_invariants:
    - invariant: "Self-improvement cannot be disabled"
      verification: "META-ANALYSIS-AGENTS cannot be removed"

    - invariant: "Human override always available"
      verification: "Manual intervention pathway preserved"

    - invariant: "Rollback always possible"
      verification: "Version lineage maintains history"

    - invariant: "No unbounded resource consumption"
      verification: "Resource limits enforced"

    - invariant: "Confidence claims are calibrated"
      verification: "No systematic overconfidence"

  constraint_verification:
    method: "Formal verification where possible, testing otherwise"
    frequency: "Every improvement proposal"
    failure_action: "Proposal rejected, investigation triggered"
```

---

## 5. A/B Testing Framework

### 5.1 Test Design

```yaml
ab_test_design:
  experiment_structure:
    control_group: "Current USF version"
    treatment_group: "USF with proposed improvement"
    allocation: "50/50 random assignment"

  sample_size_calculation:
    minimum_detectable_effect: 0.05  # 5% improvement
    statistical_power: 0.8
    significance_level: 0.05
    typical_sample_size: "100-500 tasks depending on variance"

  randomization:
    method: "Hash-based deterministic assignment"
    stratification: "By domain category"
    blocking: "By precision level"

  blinding:
    single_blind: "Evaluators don't know which version"
    double_blind: "Not applicable (system knows its version)"
```

### 5.2 Metrics Collection

```yaml
ab_metrics:
  primary_metrics:
    quality_score:
      definition: "Aggregate output quality"
      measurement: "MAL-QUALITY assessments"
      target_delta: "> 0.05 improvement"

    accuracy_rate:
      definition: "Correct outputs / total outputs"
      measurement: "Ground truth comparison"
      target_delta: "> 0.02 improvement"

  secondary_metrics:
    efficiency:
      definition: "Quality per resource unit"
      measurement: "Quality / compute time"
      constraint: "No degradation allowed"

    convergence_speed:
      definition: "Iterations to convergence"
      measurement: "Cycle count"
      constraint: "No significant increase"

    coverage:
      definition: "Requirements addressed"
      measurement: "Coverage percentage"
      constraint: "No degradation"

  guardrail_metrics:
    failure_rate:
      definition: "Tasks that fail completely"
      threshold: "Must not increase"

    regression_markers:
      definition: "Specific cases that must not regress"
      threshold: "100% pass rate"
```

### 5.3 Statistical Analysis

```yaml
statistical_analysis:
  primary_test:
    method: "Two-sample t-test or Mann-Whitney U"
    selection: "Based on normality of distribution"
    correction: "Bonferroni for multiple comparisons"

  effect_size:
    calculation: "Cohen's d for continuous, odds ratio for binary"
    minimum_practical_effect: 0.1

  sequential_analysis:
    enabled: true
    method: "O'Brien-Fleming spending function"
    interim_analyses: [0.25, 0.5, 0.75, 1.0]
    early_stopping: "For overwhelming evidence"

  decision_criteria:
    accept_improvement:
      - "p < 0.05 for primary metric"
      - "Effect size > minimum practical effect"
      - "No guardrail violations"
      - "Secondary metrics within constraints"

    reject_improvement:
      - "p > 0.2 (likely no effect)"
      - "Guardrail violation"
      - "Negative effect size"

    continue_testing:
      - "0.05 < p < 0.2 (uncertain)"
      - "Increase sample size if practical"
```

---

## 6. Approval Workflow

### 6.1 Approval Paths by Bootstrap Phase

```
APPROVAL PATHS BY BOOTSTRAP PHASE
═══════════════════════════════════════════════════════════════════════════════

Phase 1 (Cycles 1-3): FULL HUMAN OVERSIGHT
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  ALL IMPROVEMENTS → Human Review → Human Approval → Apply                  │
│                                                                             │
│  Approval criteria:                                                         │
│    • Human explicitly approves                                             │
│    • All validation passes                                                 │
│    • A/B test shows improvement                                            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

Phase 2 (Cycles 4-10): RISK-STRATIFIED OVERSIGHT
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  LOW RISK    → Auto-apply if validation passes                             │
│  MEDIUM RISK → Human spot-check (20% sample)                               │
│  HIGH RISK   → Human review required                                       │
│  CRITICAL    → Human approval required                                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

Phase 3 (Cycles 11-20): EXCEPTION-BASED OVERSIGHT
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  LOW RISK    → Auto-apply                                                  │
│  MEDIUM RISK → Auto-apply with logging                                     │
│  HIGH RISK   → Human audit (within 24h)                                    │
│  CRITICAL    → Human approval required                                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

Phase 4 (Cycles 21+): AUTONOMOUS WITH SAFEGUARDS
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  LOW RISK    → Auto-apply                                                  │
│  MEDIUM RISK → Auto-apply                                                  │
│  HIGH RISK   → Auto-apply with enhanced monitoring                         │
│  CRITICAL    → Human approval required (always)                            │
│                                                                             │
│  Exception handling:                                                        │
│    • Anomaly triggers human review                                         │
│    • Rollback triggers investigation                                       │
│    • Meta-improvement changes require Phase 1 approval                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════
```

### 6.2 Human Review Interface

```yaml
human_review_interface:
  proposal_presentation:
    summary:
      - "One-sentence improvement description"
      - "Risk level with justification"
      - "Expected benefit (quantified)"

    evidence:
      - "Source findings from MAL agents"
      - "Supporting data visualizations"
      - "Historical context"

    validation_results:
      - "External anchor alignment"
      - "Regression test results"
      - "A/B test results"
      - "Adversarial test results"

    risk_assessment:
      - "Potential negative impacts"
      - "Mitigation strategies"
      - "Rollback plan"

  decision_options:
    APPROVE:
      action: "Apply improvement"
      requires: "Explicit approval click + optional comment"

    REJECT:
      action: "Discard improvement"
      requires: "Reason selection or comment"

    MODIFY:
      action: "Revise and resubmit"
      requires: "Modification instructions"

    DEFER:
      action: "Postpone decision"
      requires: "Deferral reason and timeline"

    INVESTIGATE:
      action: "Request more information"
      requires: "Specific questions"
```

---

## 7. Integration Protocol

### 7.1 Improvement Application

```
IMPROVEMENT APPLICATION PROTOCOL
═══════════════════════════════════════════════════════════════════════════════

PRE-APPLICATION:
  1. Verify approval status
  2. Verify no conflicting pending improvements
  3. Create rollback point
  4. Notify dependent components

APPLICATION:
  1. Apply modification to target specification
  2. Update cross-references
  3. Invalidate affected caches
  4. Propagate to runtime configuration

POST-APPLICATION:
  1. Verify system stability
  2. Execute smoke tests
  3. Update version lineage
  4. Enable monitoring

MONITORING PERIOD:
  Duration: 7 days (configurable by risk level)
  Metrics: All primary and secondary A/B metrics
  Trigger: Automatic rollback if metrics degrade

═══════════════════════════════════════════════════════════════════════════════
```

### 7.2 Conflict Resolution

```yaml
conflict_resolution:
  conflict_types:
    overlapping_modifications:
      description: "Two improvements modify same content"
      resolution:
        - "Identify overlap extent"
        - "Attempt automatic merge if non-conflicting"
        - "Escalate to human if truly conflicting"
        - "Choose higher-priority improvement"

    dependent_improvements:
      description: "Improvement B requires improvement A"
      resolution:
        - "Identify dependency chain"
        - "Apply in dependency order"
        - "Rollback chain if any fails"

    contradictory_improvements:
      description: "Improvements have opposite effects"
      resolution:
        - "Run comparative A/B tests"
        - "Choose better performer"
        - "Document rejected alternative"

  merge_protocol:
    automatic_merge:
      conditions:
        - "Non-overlapping modifications"
        - "No dependency conflicts"
        - "Compatible categories"

    manual_merge:
      conditions:
        - "Overlapping but potentially compatible"
        - "Human judgment needed"

    mutual_exclusion:
      conditions:
        - "Contradictory effects"
        - "Cannot coexist"
```

---

## 8. Rollback Protocol

### 8.1 Rollback Triggers

```yaml
rollback_triggers:
  automatic:
    quality_degradation:
      condition: "Primary metrics drop > 5%"
      action: "Immediate rollback"
      notification: "Alert human operators"

    failure_rate_increase:
      condition: "Failure rate increases > 2%"
      action: "Immediate rollback"
      notification: "Alert human operators"

    convergence_failure:
      condition: "Tasks failing to converge"
      action: "Immediate rollback"
      notification: "Alert human operators"

    resource_exhaustion:
      condition: "Resource usage > 2x baseline"
      action: "Immediate rollback"
      notification: "Alert human operators"

  manual:
    human_request:
      condition: "Human operator requests rollback"
      action: "Execute rollback"
      documentation: "Required reason"

    scheduled_review:
      condition: "Periodic review finds issues"
      action: "Execute rollback if confirmed"
      documentation: "Review findings"
```

### 8.2 Rollback Execution

```
ROLLBACK EXECUTION PROTOCOL
═══════════════════════════════════════════════════════════════════════════════

IMMEDIATE ROLLBACK (Risk: LOW-MEDIUM):
  1. Stop new task processing
  2. Complete in-flight tasks with current version
  3. Restore previous specification version
  4. Clear affected caches
  5. Resume task processing
  Duration: < 1 minute

GRACEFUL ROLLBACK (Risk: HIGH):
  1. Mark improvement as "rolling back"
  2. Route new tasks to previous version
  3. Complete in-flight tasks
  4. Verify no data corruption
  5. Fully revert to previous version
  6. Post-rollback validation
  Duration: < 10 minutes

EMERGENCY ROLLBACK (Risk: CRITICAL):
  1. Immediately halt all processing
  2. Full system snapshot
  3. Revert to last known good state
  4. Comprehensive validation
  5. Human verification before resuming
  Duration: < 1 hour, human-gated resume

POST-ROLLBACK:
  1. Update version lineage (mark improvement as rolled back)
  2. Document rollback reason
  3. Create investigation ticket
  4. Notify relevant stakeholders
  5. Root cause analysis

═══════════════════════════════════════════════════════════════════════════════
```

---

## 9. Improvement Velocity Management

### 9.1 Throughput Controls

```yaml
throughput_controls:
  rate_limiting:
    max_improvements_per_day: 3
    max_improvements_per_week: 10
    max_pending_improvements: 20
    max_high_risk_per_week: 2
    max_critical_per_month: 1

  cooldown_periods:
    same_component:
      description: "Minimum time between improvements to same component"
      duration: "24 hours"

    post_rollback:
      description: "Minimum time before retrying rolled-back improvement"
      duration: "7 days"

    post_critical:
      description: "Minimum time after critical improvement"
      duration: "48 hours"

  batch_optimization:
    enabled: true
    description: "Combine compatible improvements"
    conditions:
      - "Same component"
      - "Non-conflicting"
      - "Similar risk level"
```

### 9.2 Improvement Queue Management

```yaml
queue_management:
  prioritization_factors:
    benefit_magnitude: 0.3
    confidence_in_benefit: 0.2
    risk_level: 0.2  # Lower risk = higher priority
    age_in_queue: 0.1  # Older = higher priority (prevent starvation)
    strategic_alignment: 0.2

  queue_states:
    PENDING:
      description: "Awaiting validation"
      max_duration: "7 days"
      timeout_action: "Re-prioritize or discard"

    VALIDATING:
      description: "Undergoing validation"
      max_duration: "3 days"
      timeout_action: "Restart validation"

    TESTING:
      description: "In A/B testing"
      max_duration: "14 days"
      timeout_action: "Conclude test, decide"

    APPROVED:
      description: "Awaiting application"
      max_duration: "24 hours"
      timeout_action: "Apply or expire"

  garbage_collection:
    stale_proposals: "Discard after 30 days without progress"
    rejected_proposals: "Archive after 7 days"
    superseded_proposals: "Discard when better alternative approved"
```

---

## 10. Integration Points

### 10.1 Input from Meta-Analysis Agents

```yaml
mal_input:
  findings:
    source: "All MAL agents"
    format: "Structured findings with evidence"
    frequency: "After each meta-analysis cycle"

  metrics:
    source: "MAL agent health monitoring"
    format: "Quantified performance data"
    frequency: "Real-time streaming"
```

### 10.2 Output to Version Lineage

```yaml
version_lineage_output:
  applied_improvements:
    content: "Full improvement proposal + results"
    trigger: "On improvement application"

  rollbacks:
    content: "Rollback reason + investigation"
    trigger: "On rollback execution"

  rejected_improvements:
    content: "Rejection reason + proposal archive"
    trigger: "On improvement rejection"
```

### 10.3 Bootstrap Protocol Integration

```yaml
bootstrap_integration:
  phase_query:
    description: "Get current bootstrap phase"
    usage: "Determine approval path"

  phase_transition_impact:
    description: "Notify when phase changes"
    impact: "Update approval requirements"
```

---

## Appendix A: Improvement Protocol Quick Reference

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                   USF 4.0 IMPROVEMENT PROTOCOL REFERENCE                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  LIFECYCLE: Proposal → Validation → A/B Test → Approval → Integration       ║
║                                                                              ║
║  CATEGORIES: Taxonomy, Template, Archetype, Precision, Verification,        ║
║              Process, Meta                                                   ║
║                                                                              ║
║  RISK LEVELS: LOW (auto), MEDIUM (spot-check), HIGH (review), CRITICAL     ║
║                                                                              ║
║  VALIDATION: External anchors + Regression tests + Adversarial + Safety     ║
║                                                                              ║
║  A/B TESTING: 100-500 tasks, p<0.05, effect size > 0.1                      ║
║                                                                              ║
║  ROLLBACK: Automatic on metric degradation, manual on request               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## Appendix B: Change Log

| Version | Date | Changes |
|---------|------|---------|
| 4.0.0 | 2025-12-10 | Initial USF 4.0 improvement protocol specification |
| 4.0.1 | 2025-12-10 | Added META category cross-agent constraints per red team analysis |

---

*This document is part of the USF 4.0 specification suite. See MASTER-SPECIFICATION.md for framework overview.*
