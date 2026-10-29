# USF 4.0: Convergence Criteria

> **Version**: 4.1.1 (See VERSION.yaml)
> **Component**: Integration / Convergence Criteria
> **Status**: Specification
> **Dependencies**: EXECUTION-FLOW.md, core/PRECISION-LEVELS.md
> **Last Updated**: 2025-12-10
> **SKYNET Integration**: Multi-perspective consensus mechanism

---

## 1. Overview

Convergence Criteria define when USF analysis has reached a stable, reliable state. Both operational convergence (task completion) and meta-convergence (self-improvement stability) are specified.

```
CONVERGENCE ARCHITECTURE
═══════════════════════════════════════════════════════════════════════════════

                    OPERATIONAL CONVERGENCE
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                         │
    │   Phase Convergence ──► Task Convergence ──► Verification Convergence  │
    │                                                                         │
    │   "When is a phase      "When is the         "When is confidence       │
    │    complete?"            analysis done?"       sufficient?"            │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘

                    META-CONVERGENCE
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                         │
    │   Improvement Convergence ──► Evolution Convergence ──► Stability      │
    │                                                                         │
    │   "When is an             "When is a version    "When is USF          │
    │    improvement done?"      stable?"              mature?"              │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════
```

---

## 2. Phase Convergence

### 2.1 Convergence Signals

```yaml
phase_convergence_signals:
  position_stability:
    definition: "Experts maintain consistent positions"
    measurement:
      metric: "Position change rate"
      formula: "(Experts changing position) / (Total experts)"
      threshold: "< 0.1 for 2 consecutive iterations"

    interpretation:
      stable: "Positions locked, analysis mature"
      unstable: "Active debate, more iteration needed"

  issue_saturation:
    definition: "No new significant issues emerging"
    measurement:
      metric: "New issue discovery rate"
      tracking:
        critical: "New CRITICAL issues"
        high: "New HIGH issues"
        any_significant: "New HIGH+ issues"
      threshold: "0 new HIGH+ issues for N iterations"
      N_by_precision:
        PL1: 1
        PL2: 2
        PL3: 2
        PL4: 3
        PL5: 3

    interpretation:
      saturated: "Major issues discovered"
      unsaturated: "More issues likely, continue"

  synthesis_stability:
    definition: "Synthesized output not materially changing"
    measurement:
      metric: "Synthesis delta"
      method: "Semantic similarity between iterations"
      threshold: "Similarity > 0.95 for 2 iterations"

    interpretation:
      stable: "Synthesis has converged"
      unstable: "Output still evolving"

  confidence_plateau:
    definition: "Confidence score stabilized"
    measurement:
      metric: "Confidence change rate"
      formula: "|confidence[n] - confidence[n-1]|"
      threshold: "< 0.01 for 2 iterations"

    interpretation:
      plateau: "Confidence stable, phase complete"
      changing: "More analysis affecting confidence"
```

### 2.2 Convergence Rules by Precision

```yaml
convergence_by_precision:
  PL1:
    required_signals: 2
    minimum_iterations: 1
    maximum_iterations: 3
    signals:
      - "Position stability OR"
      - "2 iterations completed"
    early_termination: "Allowed after 1 iteration if clear"

  PL2:
    required_signals: 3
    minimum_iterations: 2
    maximum_iterations: 5
    signals:
      - "Position stability"
      - "Issue saturation (1 iteration)"
      - "Synthesis stability OR Confidence plateau"

  PL3:
    required_signals: 4
    minimum_iterations: 3
    maximum_iterations: 7
    signals:
      - "Position stability"
      - "Issue saturation (2 iterations)"
      - "Synthesis stability"
      - "Confidence plateau"

  PL4:
    required_signals: 4
    minimum_iterations: 4
    maximum_iterations: 10
    signals:
      - "Position stability (strict)"
      - "Issue saturation (3 iterations)"
      - "Synthesis stability (strict)"
      - "Confidence plateau"
    additional: "All verification chains complete"

  PL5:
    required_signals: 4
    minimum_iterations: 5
    maximum_iterations: "Unbounded"
    signals:
      - "All PL4 signals"
      - "External validation complete"
      - "Proof completeness verified"
    additional: "Peer review approval"
```

### 2.3 Convergence Failure Handling

```yaml
convergence_failure:
  detection:
    oscillation:
      pattern: "Positions cycle between states"
      detection: "Same position pattern repeats"
      threshold: "3 repetitions of pattern"

    divergence:
      pattern: "Disagreement increasing"
      detection: "Agreement metric decreasing"
      threshold: "Decreasing for 3 iterations"

    stagnation:
      pattern: "No progress toward convergence"
      detection: "No signals met after max iterations"

  responses:
    oscillation:
      - "Introduce tie-breaker expert"
      - "Decompose problem into sub-problems"
      - "Escalate to meta-analysis"

    divergence:
      - "Scope reduction"
      - "Precision upgrade for more rigor"
      - "Expert panel expansion"

    stagnation:
      - "Force synthesis with caveats"
      - "Document non-convergence"
      - "Request external input"
```

---

## 3. Task Convergence

### 3.1 Overall Task Completion

```yaml
task_convergence:
  definition: "All phases complete with gates passed"

  requirements:
    all_phases_complete:
      check: "Every phase in template reached convergence"
      exception: "Early termination if task scope reduced"

    all_gates_passed:
      check: "Every gate evaluation returned PASS or CONDITIONAL_PASS"
      exception: "CONDITIONAL_PASS requires documentation"

    synthesis_complete:
      check: "Final synthesis phase converged"
      requirement: "Synthesizer produced integrated output"

    verification_complete:
      check: "Verification chains executed"
      requirement: "Agreement threshold met"

  completion_states:
    COMPLETE:
      definition: "All requirements met"
      confidence: "Full confidence in output"

    COMPLETE_WITH_CAVEATS:
      definition: "Requirements met with documented limitations"
      confidence: "Confidence with noted restrictions"

    PARTIAL:
      definition: "Some requirements not met"
      confidence: "Reduced confidence, documented gaps"

    FAILED:
      definition: "Cannot produce reliable output"
      confidence: "Output not reliable"
```

### 3.2 Task Quality Criteria

```yaml
quality_criteria:
  completeness:
    definition: "All aspects of task addressed"
    measurement:
      - "Requirements coverage percentage"
      - "Scope items addressed"
      - "Questions answered"
    threshold:
      PL1: "≥ 80%"
      PL2: "≥ 90%"
      PL3-5: "≥ 95%"

  consistency:
    definition: "No contradictions in output"
    measurement:
      - "Internal consistency check"
      - "Cross-reference validation"
      - "Expert agreement on claims"
    threshold: "0 contradictions"

  actionability:
    definition: "Output enables action"
    measurement:
      - "Clear recommendations"
      - "Prioritization provided"
      - "Implementation guidance"
    threshold: "User feedback metric"

  confidence:
    definition: "Appropriate confidence level"
    measurement: "Aggregated verification chain confidence"
    threshold:
      PL1: "≥ 80%"
      PL2: "≥ 90%"
      PL3: "≥ 95%"
      PL4: "≥ 99%"
      PL5: "100% (information-theoretic)"
```

---

## 4. Verification Convergence

### 4.1 Chain Agreement Convergence

```yaml
chain_agreement:
  definition: "Verification chains reach consensus"

  agreement_thresholds:
    PL1: "2/3 chains agree"
    PL2: "3/4 chains agree"
    PL3: "4/5 chains agree"
    PL4: "5/5 chains agree (unanimous)"
    PL5: "5/5 + external validation"

  convergence_process:
    1: "Execute chains (parallel where possible)"
    2: "Collect verdicts per claim"
    3: "Calculate agreement level"
    4: "If agreement < threshold:"
       - "Identify disagreement source"
       - "Resolve or document"
       - "Re-run affected chains if resolution changes input"
    5: "If agreement ≥ threshold: Converged"

  disagreement_resolution:
    additional_evidence:
      when: "Chains disagree due to incomplete information"
      action: "Gather more evidence, re-run"

    scope_clarification:
      when: "Chains analyzed different scopes"
      action: "Align scope definitions, re-run"

    expert_adjudication:
      when: "Genuine interpretive disagreement"
      action: "Expert panel decides"

    document_disagreement:
      when: "Cannot resolve"
      action: "Document in uncertainty profile"
```

### 4.2 Confidence Convergence

```yaml
confidence_convergence:
  definition: "Confidence estimate is stable and calibrated"

  convergence_signals:
    stability:
      metric: "Confidence value stable"
      threshold: "Change < 1% for 2 iterations"

    chain_alignment:
      metric: "Per-chain confidences aligned"
      threshold: "Standard deviation < 0.1"

    calibration:
      metric: "Confidence matches historical accuracy"
      threshold: "Calibration error < 5%"

  non_convergence_handling:
    unstable_confidence:
      cause: "New information changing confidence"
      response: "Continue iteration until stable"

    chain_misalignment:
      cause: "Chains have very different confidences"
      response: "Investigate cause, resolve or document"

    calibration_drift:
      cause: "Confidence doesn't match outcomes"
      response: "Apply calibration adjustment"
```

---

## 5. Meta-Convergence

### 5.1 Improvement Cycle Convergence

```yaml
improvement_convergence:
  definition: "Self-improvement process reaches stable state"

  per_improvement:
    validation_complete:
      requirement: "All validation steps finished"
      signals:
        - "External anchor validation done"
        - "Regression tests passed"
        - "A/B testing conclusive"

    decision_reached:
      requirement: "Accept/reject decision made"
      states:
        - "ACCEPTED: Improvement applied"
        - "REJECTED: Improvement discarded"
        - "DEFERRED: More information needed"

  per_cycle:
    proposals_processed:
      requirement: "All queued proposals addressed"
      metric: "Queue empty or stable"

    improvements_applied:
      requirement: "Accepted improvements integrated"
      metric: "No pending accepted improvements"

    version_stable:
      requirement: "New version validated"
      metric: "Monitoring period passed without regression"
```

### 5.2 Evolution Convergence

```yaml
evolution_convergence:
  definition: "USF evolution reaching diminishing returns"

  signals:
    improvement_rate_declining:
      metric: "Improvements per cycle decreasing"
      interpretation: "System approaching local optimum"

    quality_plateau:
      metric: "Quality metrics stable across versions"
      interpretation: "Major gains achieved"

    coverage_complete:
      metric: "Domain coverage stabilized"
      interpretation: "All relevant domains addressed"

    calibration_stable:
      metric: "Confidence calibration holding"
      interpretation: "System well-calibrated"

  maturity_levels:
    developing:
      indicators:
        - "High improvement rate"
        - "Quality increasing"
        - "Coverage expanding"
      bootstrap_phase: "1-3"

    maturing:
      indicators:
        - "Moderate improvement rate"
        - "Quality stable with occasional jumps"
        - "Coverage mostly complete"
      bootstrap_phase: "3-4"

    mature:
      indicators:
        - "Low improvement rate"
        - "Quality high and stable"
        - "Coverage complete"
      bootstrap_phase: "4+"

  convergence_is_not_stagnation:
    distinction: |
      Convergence means reaching effective operation, not stopping improvement.
      Even mature systems continue:
      - Adapting to new domains
      - Responding to external changes
      - Refining edge cases
```

### 5.3 Stability Criteria

```yaml
stability_criteria:
  operational_stability:
    definition: "Consistent task execution quality"
    metrics:
      - "Task success rate > 95%"
      - "Rollback rate < 5%"
      - "Confidence calibration < 5% error"
    duration: "Sustained for 20+ cycles"

  evolutionary_stability:
    definition: "Self-improvement process reliable"
    metrics:
      - "Improvement validation accuracy > 80%"
      - "No regression from improvements"
      - "Bootstrap phase 4 achieved"
    duration: "Sustained for 10+ cycles"

  meta_stability:
    definition: "Meta-analysis itself stable"
    metrics:
      - "MAL agent performance consistent"
      - "No meta-improvement regressions"
      - "Improvement protocol unchanged for 5+ cycles"
    duration: "Sustained"
```

---

## 6. Convergence Monitoring

### 6.1 Real-Time Monitoring

```yaml
real_time_monitoring:
  per_phase:
    tracked:
      - "Current iteration count"
      - "Signals met vs required"
      - "Convergence trajectory"
      - "Estimated iterations remaining"

    visualized:
      - "Convergence progress bar"
      - "Signal status indicators"
      - "Expert position stability graph"

  per_task:
    tracked:
      - "Phases completed"
      - "Gates passed"
      - "Current phase convergence status"
      - "Overall progress"

  per_evolution_cycle:
    tracked:
      - "Improvements proposed/processed"
      - "Validation pipeline status"
      - "Version stability metrics"
```

### 6.2 Convergence Analytics

```yaml
convergence_analytics:
  historical_analysis:
    metrics:
      - "Average iterations to convergence by domain"
      - "Convergence failure rate by type"
      - "Quality at convergence vs precision level"

    insights:
      - "Which domains converge fastest/slowest"
      - "What causes convergence failures"
      - "Precision level appropriateness"

  predictive:
    iteration_prediction:
      method: "Historical average + complexity adjustment"
      accuracy_target: "Within 2 iterations"

    failure_prediction:
      method: "Early warning from convergence trajectory"
      indicators:
        - "Oscillation pattern emerging"
        - "Divergence trend"
        - "Stagnation signals"
```

---

## 7. Convergence Acceleration

### 7.1 Acceleration Techniques

```yaml
acceleration_techniques:
  parallel_execution:
    description: "Execute independent analyses in parallel"
    application: "Expert contributions, verification chains"
    speedup: "Up to Nx where N = parallel units"

  early_termination:
    description: "Stop when confident enough"
    application: "Lower precision levels"
    criteria: "Clear convergence before max iterations"

  incremental_analysis:
    description: "Build on prior work"
    application: "Related or follow-up tasks"
    speedup: "Significant for incremental changes"

  pattern_reuse:
    description: "Apply known patterns"
    application: "Similar domain/task types"
    speedup: "Faster convergence with established patterns"
```

### 7.2 Acceleration vs Quality Trade-off

```yaml
acceleration_quality_tradeoff:
  principle: |
    Acceleration must not compromise quality below precision level requirements.
    Speed gains come from efficiency, not reduced rigor.

  safe_accelerations:
    - "Parallelization (no quality impact)"
    - "Caching (verified results reuse)"
    - "Pattern application (validated patterns)"

  risky_accelerations:
    - "Reduced iterations (may miss issues)"
    - "Fewer experts (reduced perspectives)"
    - "Fewer chains (reduced verification)"

  mitigation:
    "If risky acceleration used, explicitly document and reduce confidence"
```

---

## 8. Integration Points

### 8.1 Execution Flow Integration

```yaml
execution_flow:
  phase_loop:
    uses: "Phase convergence criteria"
    determines: "When to exit phase loop"

  task_completion:
    uses: "Task convergence criteria"
    determines: "When task is done"

  verification:
    uses: "Verification convergence"
    determines: "When confidence is established"
```

### 8.2 Meta-Analysis Integration

```yaml
meta_analysis:
  MAL-CONVERGENCE:
    monitors: "Convergence patterns"
    proposes: "Convergence improvements"

  improvement_protocol:
    uses: "Improvement convergence"
    determines: "When improvement cycle complete"
```

---

## 9. Multi-Perspective Consensus Mechanism (SKYNET Integration)

### 9.1 Consensus Architecture

```yaml
multi_perspective_consensus:
  source: "SKYNET Integration - PAL MCP consensus tool pattern"
  purpose: "Achieve robust consensus through structured multi-perspective debate"

  architecture:
    step_1_propose:
      description: "Each archetype independently proposes position"
      participants:
        - ARC-TH: "Theoretical soundness position"
        - ARC-AD: "Security/risk position"
        - ARC-IM: "Implementation feasibility position"
        - ARC-QA: "Quality assurance position"
        - ARC-ST: "Strategic value position"
      output: "5 independent position statements with reasoning"

    step_2_debate:
      description: "Structured disagreement with stance steering"
      mechanism:
        stance_steering: "Force exploration of alternative positions"
        devil_advocate: "Challenge strongest positions"
        edge_cases: "Explore boundary conditions"
      rounds: "2-3 iterations until positions stabilize"
      output: "Refined positions with addressed challenges"

    step_3_convergence:
      description: "Apply precision-level convergence criteria"
      process:
        - "Measure position agreement"
        - "Identify remaining disagreements"
        - "Apply threshold per precision level"
      threshold_reference: "See Section 2.2 Convergence Rules by Precision"

    step_4_synthesis:
      description: "Final synthesized position with confidence"
      output:
        synthesized_recommendation: "Integrated position"
        confidence_level: "Aggregated confidence"
        dissent_documentation: "Minority positions preserved"
        uncertainty_acknowledgment: "Remaining open questions"
```

### 9.2 Stance Steering Protocol

```yaml
stance_steering:
  purpose: "Ensure thorough exploration of position space"

  steering_techniques:
    position_inversion:
      description: "Force expert to argue opposite position"
      trigger: "Position held with >90% confidence"
      benefit: "Reveals hidden assumptions"

    alternative_generation:
      description: "Require 2+ alternative positions"
      trigger: "Initial convergence too fast (<2 iterations)"
      benefit: "Prevents groupthink"

    assumption_surfacing:
      description: "Explicitly list position assumptions"
      trigger: "All positions"
      benefit: "Identifies shared blindspots"

    evidence_challenge:
      description: "Demand evidence for each claim"
      trigger: "Positions with low evidence citation"
      benefit: "Grounds positions in data"

  steering_rules:
    frequency: "At least once per expert per debate"
    documentation: "All steering challenges recorded"
    resolution: "Challenges must be addressed or acknowledged"
```

### 9.3 Disagreement Documentation

```yaml
disagreement_documentation:
  purpose: "Preserve valuable minority perspectives"

  documentation_structure:
    majority_position:
      content: "Consensus recommendation"
      confidence: "Aggregated confidence"
      supporting_archetypes: "Which archetypes agree"

    minority_positions:
      content: "Dissenting views"
      reasoning: "Why dissent persists"
      conditions: "Under what conditions minority might be correct"
      archetype_source: "Which archetype(s) dissent"

    unresolved_questions:
      content: "Questions that couldn't be resolved"
      impact: "How uncertainty affects recommendation"
      future_resolution: "What would resolve the question"

  preservation_rules:
    threshold: "Document if >1 archetype dissents"
    visibility: "Include in final output"
    tracking: "Track resolution over time"
```

### 9.4 Consensus Failure Modes

```yaml
consensus_failure_modes:
  false_consensus:
    description: "Apparent agreement hiding real disagreement"
    detection:
      - "All positions identical from start"
      - "No substantive challenges made"
      - "Positions lack reasoning depth"
    response:
      - "Force stance steering"
      - "Require independent reasoning documentation"
      - "Inject adversarial challenge"

  permanent_deadlock:
    description: "Cannot achieve required agreement threshold"
    detection:
      - "Position stability but below threshold"
      - "Same disagreements persist >5 iterations"
    response:
      - "Document as PARTIAL convergence"
      - "Escalate precision level for more rigor"
      - "Decompose into sub-problems"

  cascade_agreement:
    description: "Experts influenced by early positions"
    detection:
      - "Positions cluster around first proposal"
      - "Later experts don't add new reasoning"
    response:
      - "Randomize position reveal order"
      - "Require independent initial positions"
```

## 9.5 Consensus Failure Recovery Protocols (Cycle 5 Enhancement)

```yaml
recovery_protocols:
  false_consensus_recovery:
    detection: "See Section 9.4 indicators"
    immediate_actions:
      1: "Halt current synthesis"
      2: "Inject adversarial challenge from ARC-AD"
      3: "Require each archetype to document independent reasoning"
      4: "Randomize position reveal order for re-debate"
    success_criteria: "Genuine disagreement surfaces"
    escalation: "If still false after 2 attempts, escalate to human review"

  permanent_deadlock_recovery:
    detection: "Same disagreements persist > 5 iterations"
    immediate_actions:
      1: "Document deadlock state"
      2: "Attempt problem decomposition"
      3: "Seek narrower consensus on sub-problems"
      4: "Document PARTIAL consensus with explicit uncertainties"
    success_criteria: "Either full consensus OR documented partial with path forward"
    escalation: "If decomposition fails, escalate precision level"

  cascade_agreement_recovery:
    detection: "Positions cluster around first proposal"
    immediate_actions:
      1: "Discard current positions"
      2: "Require blind independent position generation"
      3: "Use sealed-bid style reveal (all at once)"
      4: "Compare to original for genuine vs cascade"
    success_criteria: "Independent positions show diversity"
    prevention: "Default to blind generation for PL3+"

recovery_metrics:
  tracking:
    - recovery_attempts: "Count per failure type"
    - recovery_success_rate: "Successful recoveries / attempts"
    - escalation_rate: "Escalations / total failures"
  health_threshold:
    recovery_success: "> 70%"
    escalation_rate: "< 20%"
```

---

## Appendix A: Convergence Quick Reference

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    USF 4.0 CONVERGENCE CRITERIA REFERENCE                    ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  PHASE CONVERGENCE SIGNALS:                                                  ║
║    • Position stability (experts stop changing)                             ║
║    • Issue saturation (no new HIGH+ issues)                                 ║
║    • Synthesis stability (output not changing)                              ║
║    • Confidence plateau (confidence stable)                                 ║
║                                                                              ║
║  REQUIRED BY PRECISION:                                                      ║
║    PL1: 2 signals, 1-3 iterations                                           ║
║    PL2: 3 signals, 2-5 iterations                                           ║
║    PL3: 4 signals, 3-7 iterations                                           ║
║    PL4: 4 signals + verification, 4-10 iterations                           ║
║    PL5: All + external, 5+ iterations                                       ║
║                                                                              ║
║  FAILURE MODES: Oscillation, Divergence, Stagnation                         ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## Appendix B: Change Log

| Version | Date | Changes |
|---------|------|---------|
| 4.0.0 | 2025-12-10 | Initial USF 4.0 convergence criteria specification |
| 4.1.0 | 2025-12-10 | SKYNET Integration: Added Section 9 - Multi-perspective consensus mechanism with stance steering and disagreement documentation |
| 4.1.1 | 2025-12-10 | Cycle 5 Enhancements: MED-018 - Added Section 9.5 - Consensus Failure Recovery Protocols with detailed recovery procedures and metrics |

---

*This document is part of the USF 4.0 specification suite. See MASTER-SPECIFICATION.md for framework overview.*
