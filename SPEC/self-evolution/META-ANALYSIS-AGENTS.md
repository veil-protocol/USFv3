# USF 4.0: Meta-Analysis Agents

> **Version**: 4.1.1 (See VERSION.yaml)
> **Component**: Self-Evolution / Meta-Analysis Agents
> **Status**: Specification
> **Dependencies**: MASTER-SPECIFICATION.md, EXPERT-ARCHETYPES.md
> **Last Updated**: 2025-12-10
> **SKYNET Integration**: 5 new MAL agents, tool permission model

---

## 1. Overview

Meta-Analysis Agents (MAL-*) are specialized components that analyze USF's own operation, identify weaknesses, and propose improvements. They enable the recursive self-improvement capability central to USF 4.0.

```
META-ANALYSIS AGENT ARCHITECTURE
═══════════════════════════════════════════════════════════════════════════════

                         OPERATIONAL LAYER (Mode A)
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                                                                         │
    │   Task Input ───► USF Execution ───► Output + Execution Trace          │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ Execution Trace
                                    │ Performance Metrics
                                    │ Output Quality Signals
                                    ▼
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                      META-ANALYSIS LAYER (Mode B)                       │
    │                                                                         │
    │  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐ │
    │  │    MAL    │ │    MAL    │ │    MAL    │ │    MAL    │ │    MAL    │ │
    │  │ COVERAGE  │ │  QUALITY  │ │EFFICIENCY │ │  NOVELTY  │ │CONVERGENCE│ │
    │  └─────┬─────┘ └─────┬─────┘ └─────┬─────┘ └─────┬─────┘ └─────┬─────┘ │
    │        │             │             │             │             │       │
    │        └──────────────────────┬────────────────────────────────┘       │
    │                               │                                         │
    │                               ▼                                         │
    │                    ┌───────────────────────┐                           │
    │                    │    MAL-ADVERSARIAL    │                           │
    │                    │  (Challenge Findings) │                           │
    │                    └───────────┬───────────┘                           │
    │                               │                                         │
    │                               ▼                                         │
    │                    ┌───────────────────────┐                           │
    │                    │ IMPROVEMENT PROPOSALS │                           │
    │                    └───────────────────────┘                           │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════
```

---

## 2. Agent Specifications

### 2.1 MAL-COVERAGE: Domain Completeness Analyzer

**Purpose**: Ensure USF can handle all relevant domains and subdomains

```yaml
agent:
  id: MAL-COVERAGE
  name: "Domain Coverage Analyzer"
  category: "Completeness Assessment"

  inputs:
    - domain_taxonomy: "Current domain classification"
    - execution_logs: "Tasks processed by domain"
    - failure_logs: "Domain-related failures"
    - external_signals: "New domain emergence indicators"

  analysis_methods:
    taxonomy_gap_detection:
      description: "Find domains not represented in taxonomy"
      process:
        - "Analyze failed task classifications"
        - "Identify tasks falling to 'OTHER' category"
        - "Cluster unclassified tasks by semantic similarity"
        - "Propose new taxonomy entries"

    template_coverage_analysis:
      description: "Check template availability per domain"
      process:
        - "Map domains to available templates"
        - "Identify domains with no dedicated template"
        - "Assess template fit quality"
        - "Propose template creation/modification"

    expert_archetype_coverage:
      description: "Verify archetype instantiation quality"
      process:
        - "Test archetype synthesis for each domain"
        - "Identify domains with poor expert generation"
        - "Analyze persona quality metrics"
        - "Propose archetype refinements"

  outputs:
    coverage_report:
      - domain_coverage_score: "Percentage of domains fully supported"
      - gap_inventory: "List of coverage gaps"
      - priority_ranking: "Gaps ranked by impact"

    improvement_proposals:
      - taxonomy_additions: "New domains to add"
      - template_creations: "New templates needed"
      - archetype_refinements: "Expert generation improvements"

  metrics:
    - taxonomy_completeness: "% of encountered tasks classifiable"
    - template_coverage: "% of domains with dedicated templates"
    - expert_quality: "Average persona fit score"

  triggers:
    proactive:
      - "Weekly taxonomy review"
      - "Monthly cross-domain analysis"
    reactive:
      - "Domain classification failure rate > 5%"
      - "Template match confidence < 80%"
```

---

### 2.2 MAL-QUALITY: Output Quality Assessor

**Purpose**: Measure and improve the quality of USF outputs

```yaml
agent:
  id: MAL-QUALITY
  name: "Output Quality Assessor"
  category: "Quality Assessment"

  inputs:
    - outputs: "USF-generated outputs"
    - ground_truth: "Known correct answers (when available)"
    - user_feedback: "Explicit and implicit user signals"
    - expert_reviews: "External expert assessments"
    - outcome_data: "Real-world outcome of recommendations"

  analysis_methods:
    accuracy_assessment:
      description: "Compare outputs to ground truth"
      process:
        - "Match outputs to known correct answers"
        - "Calculate accuracy, precision, recall"
        - "Identify systematic errors"
        - "Trace errors to methodology steps"
      metrics:
        - accuracy_rate: "% of correct outputs"
        - error_classification: "Types of errors made"
        - error_source_analysis: "Root cause identification"

    completeness_assessment:
      description: "Verify all aspects addressed"
      process:
        - "Extract requirement checklist from task"
        - "Map outputs to requirements"
        - "Identify unaddressed requirements"
        - "Assess depth of coverage per requirement"
      metrics:
        - requirement_coverage: "% of requirements addressed"
        - depth_score: "Thoroughness per requirement"

    actionability_assessment:
      description: "Evaluate practical usefulness"
      process:
        - "Assess clarity of recommendations"
        - "Evaluate feasibility of actions"
        - "Check for missing implementation details"
        - "Verify priority and sequencing guidance"
      metrics:
        - clarity_score: "How clear are recommendations"
        - feasibility_score: "How implementable are actions"
        - guidance_completeness: "Implementation detail level"

    outcome_correlation:
      description: "Track real-world outcomes"
      process:
        - "Collect outcome data where available"
        - "Correlate recommendations with results"
        - "Identify successful vs unsuccessful patterns"
        - "Refine methodology based on outcomes"
      metrics:
        - outcome_success_rate: "% of recommendations with positive outcomes"
        - prediction_calibration: "Confidence vs actual success"

  outputs:
    quality_report:
      - overall_quality_score: "Aggregate quality metric"
      - dimension_scores: "Per-dimension quality"
      - trend_analysis: "Quality over time"

    improvement_proposals:
      - methodology_fixes: "Process improvements to address errors"
      - template_refinements: "Template changes for better completeness"
      - expert_calibration: "Expert tuning for accuracy"

  triggers:
    proactive:
      - "After every task completion"
      - "Weekly quality aggregation"
      - "Monthly trend analysis"
    reactive:
      - "Quality score drops below threshold"
      - "Negative user feedback received"
      - "Outcome data shows poor results"
```

---

### 2.3 MAL-EFFICIENCY: Process Efficiency Monitor

**Purpose**: Optimize USF resource usage while maintaining quality

```yaml
agent:
  id: MAL-EFFICIENCY
  name: "Process Efficiency Monitor"
  category: "Efficiency Optimization"

  inputs:
    - execution_traces: "Detailed step-by-step logs"
    - resource_usage: "Compute, time, iteration counts"
    - phase_timings: "Duration per phase"
    - convergence_data: "Iteration counts to convergence"

  analysis_methods:
    resource_profiling:
      description: "Identify resource-intensive operations"
      process:
        - "Profile compute usage per component"
        - "Identify bottlenecks"
        - "Compare across task types"
        - "Find optimization opportunities"
      metrics:
        - compute_per_task: "Resource units consumed"
        - bottleneck_locations: "Where time is spent"
        - variance_analysis: "Consistency of resource use"

    convergence_analysis:
      description: "Optimize iteration efficiency"
      process:
        - "Track iterations to convergence"
        - "Identify slow-converging patterns"
        - "Analyze divergence causes"
        - "Propose early termination criteria"
      metrics:
        - average_iterations: "Mean cycles to converge"
        - convergence_variance: "Predictability"
        - wasted_iterations: "Post-convergence cycling"

    phase_efficiency:
      description: "Optimize phase structure"
      process:
        - "Measure time per phase"
        - "Identify unnecessary phases"
        - "Find parallelization opportunities"
        - "Propose phase consolidation"
      metrics:
        - phase_contribution: "Value added per phase"
        - parallelization_potential: "Concurrent execution opportunities"

    expert_utilization:
      description: "Optimize panel usage"
      process:
        - "Track expert contribution frequency"
        - "Identify underutilized experts"
        - "Measure contribution quality"
        - "Propose panel size optimization"
      metrics:
        - contribution_rate: "Meaningful contributions per expert"
        - redundancy_score: "Overlap between experts"
        - panel_size_efficiency: "Output quality vs panel size"

  outputs:
    efficiency_report:
      - overall_efficiency: "Resources per quality unit"
      - bottleneck_analysis: "Top inefficiencies"
      - trend_data: "Efficiency over time"

    improvement_proposals:
      - convergence_tuning: "Better stopping criteria"
      - phase_optimization: "Restructured phase sequences"
      - panel_right_sizing: "Optimized expert counts"
      - parallelization: "Concurrent execution plans"

  triggers:
    proactive:
      - "After every task (lightweight)"
      - "Weekly efficiency aggregation"
    reactive:
      - "Resource usage exceeds threshold"
      - "Convergence takes >2x expected iterations"
      - "User reports slow performance"
```

---

### 2.4 MAL-NOVELTY: Innovation Rate Tracker

**Purpose**: Ensure USF continues to discover new insights and methods

```yaml
agent:
  id: MAL-NOVELTY
  name: "Innovation Rate Tracker"
  category: "Innovation Assessment"

  inputs:
    - outputs: "Generated outputs and findings"
    - historical_outputs: "Past outputs for comparison"
    - external_knowledge: "Published knowledge base"
    - improvement_history: "Past USF improvements"

  analysis_methods:
    output_novelty_detection:
      description: "Identify genuinely new findings"
      process:
        - "Compare outputs to historical baseline"
        - "Identify unprecedented claims"
        - "Assess novelty significance"
        - "Track novel finding rate over time"
      metrics:
        - novelty_rate: "% of outputs with new findings"
        - novelty_significance: "Impact of new findings"
        - staleness_risk: "Decreasing novelty trend"

    methodology_innovation:
      description: "Track method improvements"
      process:
        - "Monitor improvement proposal generation"
        - "Track accepted vs rejected improvements"
        - "Measure improvement impact"
        - "Identify innovation patterns"
      metrics:
        - improvement_rate: "New improvements per cycle"
        - improvement_impact: "Quality delta from improvements"
        - innovation_sources: "Where good ideas come from"

    cross_domain_innovation:
      description: "Identify transferable innovations"
      process:
        - "Detect patterns successful in one domain"
        - "Assess transferability to other domains"
        - "Track cross-domain adoption"
        - "Measure transfer success"
      metrics:
        - transfer_candidates: "Patterns worth transferring"
        - transfer_success_rate: "Successful transfers"
        - cross_pollination: "Domains benefiting from transfer"

  stagnation_detection:
    description: "Identify when innovation slows"
    indicators:
      - "Novelty rate declining for 3+ cycles"
      - "No significant improvements for 5+ cycles"
      - "Output similarity to templates increasing"
      - "Expert contributions becoming formulaic"
    responses:
      - "Inject external knowledge"
      - "Force exploration of edge cases"
      - "Introduce adversarial challenges"
      - "Request domain expansion"

  outputs:
    novelty_report:
      - innovation_health: "Overall innovation status"
      - trend_analysis: "Innovation trajectory"
      - stagnation_warnings: "Early warning indicators"

    improvement_proposals:
      - exploration_prompts: "Push for novel analysis"
      - knowledge_injection: "External knowledge to incorporate"
      - challenge_scenarios: "Edge cases to explore"

  triggers:
    proactive:
      - "After each task (lightweight novelty check)"
      - "Weekly innovation aggregation"
      - "Monthly stagnation assessment"
    reactive:
      - "Novelty rate drops below threshold"
      - "Multiple cycles without significant findings"
```

---

### 2.5 MAL-CONVERGENCE: Convergence Behavior Analyst

**Purpose**: Ensure proper convergence patterns and prevent pathological behaviors

```yaml
agent:
  id: MAL-CONVERGENCE
  name: "Convergence Behavior Analyst"
  category: "Process Health"

  inputs:
    - iteration_data: "Per-cycle outputs and changes"
    - expert_positions: "Expert stances over iterations"
    - confidence_trajectories: "Confidence evolution"
    - disagreement_logs: "Expert disagreement patterns"

  analysis_methods:
    convergence_pattern_analysis:
      description: "Classify convergence behavior"
      patterns:
        healthy_convergence:
          description: "Monotonic approach to consensus"
          indicators:
            - "Decreasing disagreement"
            - "Stabilizing confidence"
            - "Diminishing changes between cycles"
          assessment: "Normal, expected behavior"

        oscillating_convergence:
          description: "Cycling between positions"
          indicators:
            - "Alternating conclusions"
            - "Persistent disagreement"
            - "Confidence fluctuation"
          response: "Introduce tie-breaker, reframe problem"

        premature_convergence:
          description: "Too-quick agreement"
          indicators:
            - "Convergence in <2 cycles"
            - "Low disagreement from start"
            - "High initial confidence"
          response: "Force adversarial challenge, verify assumptions"

        divergent_behavior:
          description: "Increasing disagreement"
          indicators:
            - "Growing gap between positions"
            - "Decreasing confidence"
            - "New issues emerging each cycle"
          response: "Scope reduction, problem decomposition"

        false_convergence:
          description: "Apparent agreement masking issues"
          indicators:
            - "Surface agreement, different reasoning"
            - "Unexamined assumptions"
            - "Superficial justifications"
          response: "Deep assumption probing, reasoning comparison"

    expert_behavior_analysis:
      description: "Track individual expert patterns"
      metrics:
        - position_stability: "How often expert changes position"
        - justification_quality: "Depth of reasoning provided"
        - responsiveness: "Engagement with other experts"
        - influence_pattern: "Impact on final consensus"

    confidence_calibration:
      description: "Verify confidence accuracy"
      process:
        - "Compare claimed confidence to outcomes"
        - "Track overconfidence/underconfidence patterns"
        - "Identify calibration drift"
        - "Propose confidence adjustments"

  outputs:
    convergence_report:
      - pattern_classification: "Type of convergence observed"
      - health_assessment: "Is convergence healthy?"
      - expert_behavior_summary: "Individual expert patterns"
      - calibration_status: "Confidence accuracy"

    improvement_proposals:
      - process_interventions: "Real-time fixes for pathological patterns"
      - expert_tuning: "Adjustments to expert behavior"
      - calibration_corrections: "Confidence recalibration"

  triggers:
    proactive:
      - "Real-time monitoring during execution"
      - "Post-task convergence analysis"
    reactive:
      - "Oscillation detected (3+ cycles)"
      - "Divergence detected"
      - "Premature convergence suspected"
```

---

### 2.6 MAL-ADVERSARIAL: Challenge Effectiveness Scorer

**Purpose**: Ensure adversarial processes are effective and not theatrical

```yaml
agent:
  id: MAL-ADVERSARIAL
  name: "Challenge Effectiveness Scorer"
  category: "Adversarial Quality"

  inputs:
    - adversarial_outputs: "All adversarial contributions"
    - challenge_outcomes: "What happened to challenges"
    - fix_effectiveness: "How well fixes addressed challenges"
    - bypass_data: "When challenges were bypassed vs addressed"

  analysis_methods:
    challenge_quality_assessment:
      description: "Evaluate adversarial contribution value"
      metrics:
        novelty_score:
          description: "Are challenges finding new issues?"
          calculation: "New issues / Total challenges"
          healthy_range: [0.3, 0.8]

        severity_distribution:
          description: "Are challenges finding important issues?"
          calculation: "Distribution of challenge severity"
          expectation: "Mix of severities, not all trivial"

        technical_depth:
          description: "Are challenges substantive?"
          calculation: "Average technical sophistication"
          healthy_range: "Domain-appropriate depth"

    fix_effectiveness_tracking:
      description: "Verify challenges lead to real improvements"
      metrics:
        fix_rate:
          description: "What percentage of challenges get fixed?"
          healthy_range: [0.7, 0.95]

        fix_completeness:
          description: "Do fixes fully address challenges?"
          assessment: "Adversarial re-verification"

        regression_rate:
          description: "Do fixed issues recur?"
          healthy_range: [0, 0.1]

    adversarial_theater_detection:
      description: "Identify when adversarial process is performative"
      indicators:
        - "All challenges trivially addressed"
        - "No challenges to core assumptions"
        - "Adversarial experts agree too quickly"
        - "Challenges cluster in non-critical areas"
      response:
        - "Force challenge of core claims"
        - "Inject external adversarial perspective"
        - "Require alternative hypothesis generation"

    adversarial_calibration:
      description: "Tune adversarial intensity"
      too_weak_indicators:
        - "Fix rate > 95%"
        - "No CRITICAL findings"
        - "Challenges feel pro forma"
      too_strong_indicators:
        - "Fix rate < 50%"
        - "Paralysis from over-challenge"
        - "Adversarial becomes destructive"
      calibration_actions:
        - "Adjust adversarial archetype intensity"
        - "Modify adversarial expert personas"
        - "Tune challenge acceptance thresholds"

  outputs:
    adversarial_report:
      - effectiveness_score: "Overall adversarial health"
      - challenge_distribution: "Where challenges are focused"
      - fix_tracking: "Challenge resolution status"
      - theater_warnings: "Performative behavior indicators"

    improvement_proposals:
      - intensity_adjustments: "Adversarial strength tuning"
      - focus_redirects: "Where to direct adversarial attention"
      - expert_refinements: "Adversarial persona improvements"

  triggers:
    proactive:
      - "After each adversarial phase"
      - "Weekly adversarial health check"
    reactive:
      - "Fix rate outside healthy range"
      - "Theater indicators detected"
```

---

### 2.7 MAL-CONTEXT: Context Optimization Manager (SKYNET Integration)

**Purpose**: Optimize context window utilization and prevent context exhaustion

```yaml
agent:
  id: MAL-CONTEXT
  name: "Context Optimization Manager"
  category: "Resource Management"
  source: "SKYNET Integration - VoltAgent context-manager pattern"

  inputs:
    - context_utilization: "Current context window usage"
    - token_counts: "Token consumption per component"
    - conversation_history: "Message history"
    - active_state: "Currently loaded context"

  analysis_methods:
    context_pressure_detection:
      description: "Identify context exhaustion risk"
      process:
        - "Monitor context utilization percentage"
        - "Track utilization trend"
        - "Predict exhaustion point"
        - "Trigger early warning"
      metrics:
        - utilization_rate: "% of context window used"
        - growth_rate: "Context growth per turn"
        - exhaustion_eta: "Turns until limit"

    context_optimization:
      description: "Recommend context reduction strategies"
      strategies:
        summarization: "Summarize verbose sections"
        pruning: "Remove low-value context"
        compression: "Compact repeated patterns"
        offloading: "Move to external storage"
      metrics:
        - reduction_potential: "Achievable reduction %"
        - quality_impact: "Information loss risk"

  outputs:
    context_report:
      - current_utilization: "Usage percentage"
      - optimization_recommendations: "Prioritized strategies"
      - urgency_level: "LOW|MEDIUM|HIGH|CRITICAL"

  tools: ["Read"]  # Read-only agent

  triggers:
    proactive:
      - "Context utilization > 60%"
      - "Every 10 turns"
    reactive:
      - "Context utilization > 80%"
      - "Rapid growth detected"
```

---

### 2.8 MAL-ERROR: Error Handling Coordinator (SKYNET Integration)

**Purpose**: Coordinate error handling and recovery across USF execution

```yaml
agent:
  id: MAL-ERROR
  name: "Error Handling Coordinator"
  category: "Process Recovery"
  source: "SKYNET Integration - VoltAgent error-coordinator pattern"

  inputs:
    - error_logs: "Execution errors and exceptions"
    - failure_patterns: "Historical failure data"
    - recovery_attempts: "Previous recovery actions"
    - system_state: "Current execution state"

  analysis_methods:
    error_classification:
      description: "Categorize and prioritize errors"
      process:
        - "Classify error type (see ERROR-CODES.md)"
        - "Assess severity and impact"
        - "Identify affected components"
        - "Determine recovery priority"
      categories:
        - transient: "Retry likely to succeed"
        - persistent: "Requires intervention"
        - cascading: "May cause additional failures"
        - blocking: "Prevents execution continuation"

    root_cause_analysis:
      description: "Identify underlying causes"
      process:
        - "Trace error propagation"
        - "Identify trigger conditions"
        - "Find common failure patterns"
        - "Propose systemic fixes"

    recovery_coordination:
      description: "Orchestrate error recovery"
      strategies:
        retry: "Attempt operation again"
        fallback: "Use alternative approach"
        graceful_degradation: "Continue with reduced capability"
        escalation: "Request human intervention"

  outputs:
    error_report:
      - error_summary: "Categorized error inventory"
      - root_causes: "Identified underlying issues"
      - recovery_plan: "Recommended recovery actions"

  tools: ["Read", "Grep"]  # Read + search only

  triggers:
    reactive:
      - "Any ERROR or higher severity"
      - "Multiple WARN in sequence"
      - "Recovery attempt failed"
```

---

### 2.9 MAL-KNOWLEDGE: Knowledge Synthesis Agent (SKYNET Integration)

**Purpose**: Synthesize and persist knowledge across sessions for cross-session learning

```yaml
agent:
  id: MAL-KNOWLEDGE
  name: "Knowledge Synthesis Agent"
  category: "Learning & Persistence"
  source: "SKYNET Integration - VoltAgent knowledge-synthesizer pattern"

  inputs:
    - session_outcomes: "Results from completed tasks"
    - lesson_candidates: "Potential learnings identified"
    - pattern_library: "Existing knowledge patterns"
    - feedback_signals: "User and outcome feedback"

  analysis_methods:
    lesson_extraction:
      description: "Extract reusable learnings from sessions"
      process:
        - "Identify successful patterns"
        - "Document failure modes"
        - "Abstract generalizable principles"
        - "Validate against existing knowledge"
      criteria:
        - repeatability: "Pattern observed multiple times"
        - significance: "Meaningful impact on outcomes"
        - generalizability: "Applicable beyond source context"

    knowledge_integration:
      description: "Integrate new knowledge with existing"
      process:
        - "Check for conflicts with existing patterns"
        - "Merge complementary knowledge"
        - "Update pattern confidence scores"
        - "Archive superseded patterns"

    knowledge_retrieval:
      description: "Provide relevant knowledge to active tasks"
      process:
        - "Match task characteristics to patterns"
        - "Rank patterns by relevance"
        - "Surface applicable lessons"
        - "Track retrieval effectiveness"

  outputs:
    knowledge_updates:
      - new_patterns: "Newly validated patterns"
      - updated_patterns: "Modified existing patterns"
      - deprecated_patterns: "Patterns to retire"

  tools: ["Read", "Write"]  # Can update knowledge store

  knowledge_store:
    location: ".usf/knowledge/"
    format: "YAML files"
    schema:
      patterns:
        file: "patterns.yaml"
        structure:
          - pattern_id: "Unique identifier"
          - description: "Pattern description"
          - confidence: "0.0-1.0"
          - observations: "Count of supporting observations"
          - last_updated: "ISO timestamp"
          - source_tasks: "Task IDs that contributed"
      lessons:
        file: "lessons.yaml"
        structure:
          - lesson_id: "Unique identifier"
          - category: "success|failure|insight"
          - description: "What was learned"
          - applicability: "When this applies"
          - confidence: "0.0-1.0"
    retention:
      max_patterns: 500
      max_lessons: 200
      pruning: "Remove lowest confidence when limit reached"

  triggers:
    proactive:
      - "After task completion"
      - "Weekly knowledge consolidation"
    reactive:
      - "Significant success or failure"
      - "User provides explicit feedback"
```

---

### 2.10 MAL-TASK: Task Distribution Optimizer (SKYNET Integration)

**Purpose**: Optimize task decomposition and distribution for parallel execution

```yaml
agent:
  id: MAL-TASK
  name: "Task Distribution Optimizer"
  category: "Workflow Optimization"
  source: "SKYNET Integration - VoltAgent task-distributor pattern"

  inputs:
    - task_structure: "Current task breakdown"
    - dependency_graph: "Task dependencies"
    - resource_availability: "Available execution capacity"
    - historical_performance: "Past task execution data"

  analysis_methods:
    dependency_analysis:
      description: "Map task dependencies and constraints"
      process:
        - "Identify data dependencies"
        - "Map execution order constraints"
        - "Find parallelization opportunities"
        - "Calculate critical path"
      outputs:
        - dependency_graph: "Visual task dependencies"
        - parallel_groups: "Tasks that can run together"
        - critical_path: "Longest sequential chain"

    decomposition_optimization:
      description: "Optimize task breakdown"
      process:
        - "Assess granularity appropriateness"
        - "Identify merge opportunities"
        - "Identify split opportunities"
        - "Balance load across resources"
      criteria:
        - granularity: "Not too fine, not too coarse"
        - cohesion: "Related work grouped together"
        - independence: "Minimize cross-task dependencies"

    execution_planning:
      description: "Plan optimal execution sequence"
      process:
        - "Schedule parallel execution"
        - "Allocate resources to tasks"
        - "Plan synchronization points"
        - "Build contingency paths"

  outputs:
    task_plan:
      - optimized_breakdown: "Refined task structure"
      - execution_schedule: "Parallel execution plan"
      - resource_allocation: "Resource assignments"

  tools: ["Read"]  # Read-only analysis

  triggers:
    proactive:
      - "Complex task received (>5 subtasks)"
      - "Parallel execution opportunity detected"
    reactive:
      - "Task taking longer than expected"
      - "Resource contention detected"
```

---

### 2.11 MAL-WORKFLOW: Workflow Orchestration Agent (SKYNET Integration)

**Purpose**: Orchestrate complex multi-phase workflows and coordinate transitions

```yaml
agent:
  id: MAL-WORKFLOW
  name: "Workflow Orchestration Agent"
  category: "Process Orchestration"
  source: "SKYNET Integration - VoltAgent workflow-orchestrator pattern"

  scope_clarification:
    note: "MAL-WORKFLOW performs META-ANALYSIS of workflow health"
    distinction:
      EXECUTION-FLOW: "Defines and executes workflows"
      MAL-WORKFLOW: "Monitors, analyzes, and optimizes workflow patterns"
    does:
      - "Analyze workflow efficiency"
      - "Detect workflow bottlenecks"
      - "Propose workflow optimizations"
    does_not:
      - "Execute workflows directly"
      - "Override EXECUTION-FLOW decisions"
      - "Control workflow routing"

  inputs:
    - workflow_definition: "Current workflow structure"
    - execution_state: "Current phase and progress"
    - phase_outcomes: "Results from completed phases"
    - transition_criteria: "Phase gate requirements"

  analysis_methods:
    workflow_optimization:
      description: "Optimize workflow structure"
      process:
        - "Analyze phase sequence efficiency"
        - "Identify unnecessary phases"
        - "Find consolidation opportunities"
        - "Propose workflow improvements"
      patterns:
        sequential: "Phase A → Phase B → Phase C"
        parallel: "Phase A + Phase B → Phase C"
        conditional: "IF condition THEN Phase A ELSE Phase B"
        iterative: "WHILE condition DO Phase A"

    transition_management:
      description: "Manage phase transitions"
      process:
        - "Verify gate criteria met"
        - "Prepare next phase context"
        - "Handle transition failures"
        - "Coordinate handoffs"

    progress_monitoring:
      description: "Track workflow progress"
      metrics:
        - phase_completion_rate: "Phases completed / total"
        - velocity: "Progress rate"
        - blockers: "Current impediments"
        - eta: "Estimated completion"

  outputs:
    workflow_status:
      - current_state: "Workflow execution status"
      - optimization_proposals: "Workflow improvements"
      - transition_recommendations: "Next phase guidance"

  tools: ["Read", "Glob"]  # Read + file discovery

  triggers:
    proactive:
      - "At each phase transition"
      - "Workflow stall detected"
    reactive:
      - "Phase gate failure"
      - "Resource exhaustion during workflow"
```

---

## 2.12 Tool Permission Model (SKYNET Integration)

```yaml
tool_permission_model:
  source: "SKYNET Integration - VoltAgent subagent tool philosophy"
  principle: "Minimal necessary permissions"

  permission_tiers:
    readonly:
      tools: ["Read", "Grep", "Glob"]
      rationale: "Analysis only - no modification capability"
      agents:
        - MAL-COVERAGE
        - MAL-QUALITY
        - MAL-ADVERSARIAL
        - MAL-CONVERGENCE
        - MAL-CONTEXT
        - MAL-TASK
        - MAL-WORKFLOW

    read_search:
      tools: ["Read", "Grep", "Glob", "WebFetch", "WebSearch"]
      rationale: "Analysis with external research capability"
      agents:
        - MAL-NOVELTY  # Needs external knowledge

    write_enabled:
      tools: ["Read", "Write", "Edit", "Glob", "Grep"]
      rationale: "Can propose and draft specification changes"
      agents:
        - MAL-EFFICIENCY  # May propose optimizations
        - MAL-KNOWLEDGE   # Updates knowledge store
        - MAL-ERROR       # May draft recovery procedures

  security_benefits:
    memory_efficiency: "Independent context windows prevent contamination"
    accuracy: "Focused scope reduces hallucination"
    predictability: "Defined boundaries ensure consistent behavior"
    auditability: "Clear tool usage for compliance"

  override_protocol:
    temporary_elevation:
      approval: "Human approval required"
      duration: "Single task only"
      logging: "Full audit trail"
```

---

## 3. Agent Coordination Protocol

### 3.1 Agent Execution Order

```
AGENT COORDINATION FLOW (USF 4.1 - All 11 Agents)
═══════════════════════════════════════════════════════════════════════════════

POST-TASK META-ANALYSIS SEQUENCE:

  Phase 0: Continuous Monitoring (Reactive - Always Active)
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   MAL-CONTEXT                         MAL-ERROR                    │
    │        │                                  │                        │
    │        ▼                                  ▼                        │
    │   Context Optimization              Error Coordination            │
    │   (Trigger: >60% context)          (Trigger: Error/Warn)          │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

  Phase 1: Parallel Assessment (Independent Analysis - 5 Agents)
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │ MAL-COVERAGE  MAL-QUALITY  MAL-EFFICIENCY  MAL-NOVELTY  MAL-TASK   │
    │      │             │              │              │           │     │
    │      ▼             ▼              ▼              ▼           ▼     │
    │  Coverage      Quality       Efficiency      Novelty    Task Dist  │
    │  Assessment    Assessment    Assessment      Assessment Optimization│
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
  Phase 2: Sequential Integration (Requires Phase 1 outputs - 2 Agents)
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   MAL-CONVERGENCE                                                   │
    │        │                                                           │
    │        ▼                                                           │
    │   Convergence Pattern Assessment                                   │
    │   (Analyzes iteration data + Phase 1 findings)                     │
    │        │                                                           │
    │        ▼                                                           │
    │   MAL-WORKFLOW                                                      │
    │        │                                                           │
    │        ▼                                                           │
    │   Workflow Optimization                                            │
    │   (Orchestrates phase transitions + workflow structure)            │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
  Phase 3: Adversarial Meta-Challenge (Challenges all findings - 1 Agent)
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   MAL-ADVERSARIAL                                                   │
    │        │                                                           │
    │        ▼                                                           │
    │   Challenge Phase 1 + 2 Findings                                   │
    │   Verify Improvement Proposals                                     │
    │   Identify Overlooked Weaknesses                                   │
    │   Test Adversarial Effectiveness                                   │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
  Phase 4: Knowledge Synthesis (Persist learnings - 1 Agent)
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   MAL-KNOWLEDGE                                                     │
    │        │                                                           │
    │        ▼                                                           │
    │   Extract Reusable Lessons                                         │
    │   Integrate with Knowledge Store                                   │
    │   Update Pattern Library                                           │
    │        │                                                           │
    │        ▼                                                           │
    │   IMPROVEMENT PROPOSAL AGGREGATION                                  │
    │        │                                                           │
    │        ▼                                                           │
    │   Consolidated improvement proposals                               │
    │   Priority ranking                                                 │
    │   Risk assessment                                                  │
    │   Cross-session learnings persisted                                │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════

AGENT EXECUTION SUMMARY:
  Phase 0: 2 agents (continuous/reactive monitoring)
  Phase 1: 5 agents (parallel independent assessment)
  Phase 2: 2 agents (sequential integration)
  Phase 3: 1 agent  (adversarial challenge)
  Phase 4: 1 agent  (knowledge synthesis)
  ────────────────────────────────────────
  Total:  11 agents (6 core + 5 SKYNET)
```

### 3.2 Inter-Agent Communication

```yaml
communication_protocol:
  format: "Structured JSON messages"

  message_types:
    finding:
      from: "Any MAL agent"
      to: "Aggregator or specific MAL agent"
      content:
        - finding_id: "Unique identifier"
        - category: "Coverage|Quality|Efficiency|Novelty|Convergence|Adversarial"
        - severity: "LOW|MEDIUM|HIGH|CRITICAL"
        - description: "Finding description"
        - evidence: "Supporting data"
        - proposal: "Suggested improvement"

    challenge:
      from: "MAL-ADVERSARIAL"
      to: "Any MAL agent"
      content:
        - finding_id: "Finding being challenged"
        - challenge_type: "Evidence|Logic|Scope|Impact"
        - challenge_description: "Nature of challenge"
        - resolution_required: true/false

    resolution:
      from: "Any MAL agent"
      to: "MAL-ADVERSARIAL"
      content:
        - challenge_id: "Challenge being resolved"
        - resolution_type: "Accepted|Refuted|Modified"
        - updated_finding: "Modified finding if applicable"
        - justification: "Reasoning"

    synthesis:
      from: "Aggregator"
      to: "Improvement Protocol"
      content:
        - cycle_id: "Meta-analysis cycle identifier"
        - findings: "List of validated findings"
        - proposals: "Prioritized improvement proposals"
        - metrics: "Aggregate health metrics"
```

### 3.3 SKYNET Agent Integration Specifics

```yaml
skynet_integration:
  purpose: "Integrate operational patterns from SKYNET (VoltAgent) into USF 4.1"
  version: "4.1.0"
  source: "Multi-agent analysis workspace for protocol security review"

  agent_categorization:
    core_analysis_agents:
      description: "Original USF 4.0 agents - domain analysis and meta-improvement"
      agents: [MAL-COVERAGE, MAL-QUALITY, MAL-EFFICIENCY, MAL-NOVELTY, MAL-CONVERGENCE, MAL-ADVERSARIAL]
      execution_model: "Post-task batch analysis"

    operational_agents:
      description: "SKYNET agents - runtime coordination and resource management"
      agents: [MAL-CONTEXT, MAL-ERROR, MAL-TASK, MAL-WORKFLOW, MAL-KNOWLEDGE]
      execution_model: "Continuous monitoring + event-driven activation"

  phase_0_continuous_monitoring:
    description: "Always-active agents that respond to runtime conditions"

    MAL-CONTEXT:
      activation_triggers:
        - "Context utilization exceeds 60%"
        - "Every 10 conversation turns"
        - "Rapid context growth detected (>10% in single turn)"
      response_latency: "Real-time (immediate)"
      tool_permissions: ["Read"]
      output_destination: "Context management recommendations"

    MAL-ERROR:
      activation_triggers:
        - "Any ERROR or CRITICAL severity event"
        - "3+ WARN events in sequence"
        - "Recovery attempt failed"
        - "Execution exception caught"
      response_latency: "Real-time (immediate)"
      tool_permissions: ["Read", "Grep"]
      output_destination: "Error recovery coordination"

  phase_1_parallel_augmentation:
    description: "MAL-TASK added to Phase 1 parallel assessment"

    MAL-TASK:
      purpose: "Optimize task decomposition alongside quality assessment"
      parallel_execution_with: [MAL-COVERAGE, MAL-QUALITY, MAL-EFFICIENCY, MAL-NOVELTY]
      analysis_focus:
        - "Task breakdown granularity"
        - "Dependency mapping"
        - "Parallelization opportunities"
        - "Critical path identification"
      tool_permissions: ["Read"]
      output_format: "Task structure recommendations"

  phase_2_sequential_augmentation:
    description: "MAL-WORKFLOW added to Phase 2 after MAL-CONVERGENCE"

    MAL-WORKFLOW:
      purpose: "Orchestrate workflow structure after convergence analysis"
      depends_on: "MAL-CONVERGENCE (must complete first)"
      analysis_focus:
        - "Phase sequence optimization"
        - "Transition management"
        - "Workflow pattern detection"
        - "Progress monitoring"
      tool_permissions: ["Read", "Glob"]
      output_format: "Workflow optimization proposals"

  phase_4_knowledge_persistence:
    description: "MAL-KNOWLEDGE synthesizes and persists learnings"

    MAL-KNOWLEDGE:
      purpose: "Extract and persist cross-session knowledge"
      execution_timing: "After MAL-ADVERSARIAL challenge phase"
      analysis_focus:
        - "Successful pattern extraction"
        - "Failure mode documentation"
        - "Generalizable principle abstraction"
        - "Knowledge integration with existing patterns"
      tool_permissions: ["Read", "Write"]
      persistent_artifacts:
        - "KNOWLEDGE-PATTERNS.md (updated)"
        - "LESSON-LIBRARY.yaml (updated)"
        - "FAILURE-MODES.md (appended)"
      output_format: "Knowledge update manifest + improvement proposals"

  coordination_dependencies:
    parallel_phases:
      description: "Agents with no inter-dependencies"
      phase_1_parallel:
        - MAL-COVERAGE
        - MAL-QUALITY
        - MAL-EFFICIENCY
        - MAL-NOVELTY
        - MAL-TASK
      execution: "Can run simultaneously, independent context windows"

    sequential_phases:
      description: "Agents requiring prior phase outputs"
      phase_2_sequential:
        step_1:
          agent: MAL-CONVERGENCE
          requires: "Phase 1 completion + execution trace data"
        step_2:
          agent: MAL-WORKFLOW
          requires: "MAL-CONVERGENCE output"

      phase_3_challenge:
        agent: MAL-ADVERSARIAL
        requires: "Phase 1 + Phase 2 all findings"

      phase_4_synthesis:
        agent: MAL-KNOWLEDGE
        requires: "Phase 3 validated findings"

    continuous_agents:
      description: "No phase dependency - reactive triggers"
      agents:
        - MAL-CONTEXT
        - MAL-ERROR
      execution: "Event-driven, can interrupt any phase"

  tool_permission_rationale:
    readonly_agents:
      agents: [MAL-COVERAGE, MAL-QUALITY, MAL-CONVERGENCE, MAL-ADVERSARIAL, MAL-CONTEXT, MAL-TASK, MAL-WORKFLOW]
      tools: ["Read", "Grep", "Glob"]
      reason: "Analysis-only - no system modification needed"

    write_enabled_agents:
      agents: [MAL-EFFICIENCY, MAL-KNOWLEDGE, MAL-ERROR]
      tools: ["Read", "Write", "Edit", "Grep", "Glob"]
      reason:
        MAL-EFFICIENCY: "May draft optimization proposals as spec changes"
        MAL-KNOWLEDGE: "Must persist lessons to knowledge store"
        MAL-ERROR: "May write recovery procedures"

    search_enabled_agents:
      agents: [MAL-NOVELTY]
      tools: ["Read", "Grep", "Glob", "WebFetch", "WebSearch"]
      reason: "Requires external knowledge for novelty assessment"

  integration_benefits:
    operational_robustness:
      - "Real-time context management prevents mid-execution failures"
      - "Error coordination enables graceful recovery"

    execution_efficiency:
      - "Task distribution optimization enables better parallelization"
      - "Workflow orchestration reduces unnecessary phase transitions"

    cross_session_learning:
      - "Knowledge persistence creates institutional memory"
      - "Failure patterns prevent repeat errors"

    separation_of_concerns:
      - "Core agents focus on quality/coverage analysis"
      - "Operational agents handle runtime coordination"
      - "Clean dependency graph prevents coordination explosion"

  migration_from_4_0:
    backward_compatibility: "USF 4.0 execution flow remains valid"
    augmentation_only: "SKYNET agents extend, not replace, core agents"
    phased_adoption:
      phase_0_agents: "Enable first - critical for stability"
      phase_1_4_agents: "Enable after Phase 0 validated"
      monitoring: "Track agent effectiveness before full integration"
```

---

## 4. Agent Health Monitoring

### 4.1 Meta-Meta-Analysis

The agents themselves are monitored for health:

```yaml
agent_health_monitoring:
  metrics_per_agent:
    - analysis_coverage: "% of relevant signals analyzed"
    - finding_accuracy: "Validated findings / Total findings"
    - proposal_acceptance_rate: "Accepted proposals / Total proposals"
    - false_positive_rate: "Invalid findings / Total findings"
    - resource_consumption: "Compute per analysis"

  health_indicators:
    healthy:
      - "Finding accuracy > 80%"
      - "Proposal acceptance > 50%"
      - "False positive rate < 10%"

    degraded:
      - "Finding accuracy 60-80%"
      - "Proposal acceptance 30-50%"
      - "False positive rate 10-20%"

    unhealthy:
      - "Finding accuracy < 60%"
      - "Proposal acceptance < 30%"
      - "False positive rate > 20%"

  remediation:
    recalibration:
      trigger: "Degraded for 3+ cycles"
      action: "Adjust agent parameters based on ground truth"

    replacement:
      trigger: "Unhealthy for 5+ cycles"
      action: "Propose agent replacement in improvement protocol"
```

### 4.2 Agent Coordination Health

```yaml
coordination_health:
  metrics:
    - agent_agreement: "Correlation between agent findings"
    - challenge_resolution_rate: "Challenges resolved vs outstanding"
    - synthesis_coherence: "Consistency of final proposals"

  pathologies:
    agent_conflict:
      description: "Agents generating contradictory findings"
      detection: "High disagreement, low resolution"
      response: "Scope clarification, domain splitting"

    echo_chamber:
      description: "Agents reinforcing without challenge"
      detection: "No challenges, immediate acceptance"
      response: "Force adversarial injection"

    analysis_paralysis:
      description: "Excessive meta-analysis, no action"
      detection: "Many findings, few accepted proposals"
      response: "Time-box meta-analysis, force prioritization"
```

---

## 5. Agent Configuration

### 5.1 Configuration Parameters

```yaml
agent_configuration:
  MAL-COVERAGE:
    analysis_depth: [1, 3]  # 1=quick, 3=deep
    taxonomy_scan_frequency: "weekly"
    external_signal_weight: 0.3
    gap_significance_threshold: 0.1

  MAL-QUALITY:
    dimensions_to_assess: ["accuracy", "completeness", "actionability"]
    ground_truth_required: false
    user_feedback_weight: 0.4
    outcome_tracking_window: "90 days"

  MAL-EFFICIENCY:
    resource_tracking_granularity: "phase"
    efficiency_threshold: 0.8
    optimization_aggressiveness: "moderate"
    parallelization_enabled: true

  MAL-NOVELTY:
    novelty_threshold: 0.2
    stagnation_window: 5  # cycles
    external_knowledge_refresh: "monthly"
    cross_domain_analysis: true

  MAL-CONVERGENCE:
    monitoring_frequency: "real-time"
    pattern_detection_sensitivity: "high"
    intervention_threshold: 3  # cycles
    calibration_window: 20  # tasks

  MAL-ADVERSARIAL:
    intensity: "moderate"  # low, moderate, high, maximum
    theater_detection_sensitivity: "high"
    challenge_scope: "comprehensive"
    meta_challenge_enabled: true
```

### 5.2 Tuning Protocol

```yaml
tuning_protocol:
  automatic_tuning:
    enabled: true
    frequency: "After 10 meta-analysis cycles"
    method: "Bayesian optimization on acceptance rate"
    constraints:
      - "Maintain finding accuracy > 70%"
      - "Keep resource usage within 2x baseline"

  manual_override:
    permitted: true
    approval_required: "Phase 1-2 bootstrap"
    documentation_required: true
```

---

## 6. Integration Points

### 6.1 Input from Operational Layer

```yaml
operational_inputs:
  execution_trace:
    - task_id: "Unique task identifier"
    - domain_profile: "Detected domain"
    - template_used: "Phase template selected"
    - precision_level: "PL1-PL5"
    - expert_panel: "Instantiated experts"
    - phase_sequence: "Phases executed"
    - iteration_counts: "Cycles per phase"
    - convergence_data: "Convergence patterns"
    - outputs: "Generated deliverables"

  performance_metrics:
    - execution_time: "Total and per-phase"
    - resource_usage: "Compute consumed"
    - confidence_achieved: "Final confidence"
    - coverage_achieved: "Final coverage"

  quality_signals:
    - user_feedback: "Explicit ratings, comments"
    - implicit_signals: "Acceptance, rejection, iteration"
    - outcome_data: "Real-world results (when available)"
```

### 6.2 Output to Improvement Protocol

```yaml
improvement_outputs:
  format: "Structured improvement proposals"

  proposal_structure:
    - proposal_id: "Unique identifier"
    - source_agent: "MAL-* that generated it"
    - category: "Taxonomy|Template|Archetype|Process|Precision|Verification"
    - priority: "LOW|MEDIUM|HIGH|CRITICAL"
    - description: "What to change"
    - rationale: "Why this improves USF"
    - evidence: "Supporting data"
    - risk_assessment: "Potential negative impacts"
    - validation_plan: "How to verify improvement works"
```

### 6.3 User Feedback Integration

```yaml
user_feedback_integration:
  purpose: "Incorporate explicit and implicit user signals into meta-analysis"

  feedback_channels:
    explicit_feedback:
      ratings:
        type: "1-5 star rating or thumbs up/down"
        collection_point: "After task completion"
        weight: 0.6

      comments:
        type: "Free-text feedback"
        processing: "Sentiment analysis + topic extraction"
        weight: 0.4

      corrections:
        type: "User corrections to output"
        processing: "Diff analysis + error categorization"
        weight: 0.8  # High weight - direct error signal

    implicit_feedback:
      acceptance_signals:
        - "Output used without modification" → positive
        - "Output modified significantly" → negative
        - "Task repeated with different parameters" → negative
        - "Follow-up questions on output" → neutral/exploratory

      engagement_metrics:
        - "Time spent reviewing output"
        - "Sections highlighted or copied"
        - "Output shared with others"

      abandonment_signals:
        - "Task cancelled mid-execution"
        - "Output ignored"
        - "Immediate new task on same topic"

  feedback_processing:
    aggregation:
      method: "Weighted rolling average"
      window: "Last 50 tasks per domain"
      decay: "Exponential, half-life 30 days"

    normalization:
      user_calibration: "Account for user tendency (strict/lenient)"
      domain_baseline: "Compare to domain average"

    routing:
      quality_signals: "→ MAL-QUALITY"
      coverage_signals: "→ MAL-COVERAGE"
      efficiency_signals: "→ MAL-EFFICIENCY"
      novelty_signals: "→ MAL-NOVELTY"

  feedback_impact:
    on_calibration:
      description: "Adjust confidence calibration based on feedback"
      method: "Compare claimed confidence to user satisfaction"
      action: "Recalibrate if systematic over/under confidence"

    on_improvement_prioritization:
      description: "User pain points get higher priority"
      method: "Weight improvement proposals by affected user count"
      action: "Boost priority for frequently reported issues"

    on_domain_detection:
      description: "Correct domain misclassifications"
      method: "User indicates correct domain"
      action: "Add to training data for DOMAIN-DETECTOR"

  privacy_considerations:
    data_retention: "Aggregated metrics only after 90 days"
    anonymization: "User identity not linked to feedback after processing"
    opt_out: "Users can opt out of feedback collection"
```

---

## Appendix A: Agent Quick Reference

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    USF 4.1 META-ANALYSIS AGENT REFERENCE                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  CORE AGENTS (USF 4.0)                                                       ║
║  MAL-COVERAGE    │ Domain completeness  │ Finds gaps in taxonomy/templates  ║
║  MAL-QUALITY     │ Output assessment    │ Measures accuracy, completeness   ║
║  MAL-EFFICIENCY  │ Resource optimization│ Improves speed, reduces waste     ║
║  MAL-NOVELTY     │ Innovation tracking  │ Prevents stagnation               ║
║  MAL-CONVERGENCE │ Process health       │ Ensures proper convergence        ║
║  MAL-ADVERSARIAL │ Challenge quality    │ Verifies adversarial effectiveness║
╠══════════════════════════════════════════════════════════════════════════════╣
║  SKYNET AGENTS (USF 4.1)                                                     ║
║  MAL-CONTEXT     │ Context management   │ Optimizes context window usage    ║
║  MAL-ERROR       │ Error coordination   │ Handles errors and recovery       ║
║  MAL-KNOWLEDGE   │ Knowledge synthesis  │ Cross-session learning            ║
║  MAL-TASK        │ Task distribution    │ Optimizes parallel execution      ║
║  MAL-WORKFLOW    │ Workflow orchestrate │ Manages complex workflows         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Total: 11 MAL Agents (6 core + 5 SKYNET)                                   ║
║  Execution: Parallel assessment → Convergence → Adversarial → Synthesis     ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## Appendix B: Change Log

| Version | Date | Changes |
|---------|------|---------|
| 4.0.0 | 2025-12-10 | Initial USF 4.0 meta-analysis agent specification |
| 4.0.1 | 2025-12-10 | Added user feedback integration (Section 6.3) per Cycle 2 red team |
| 4.1.0 | 2025-12-10 | SKYNET Integration: Added 5 new MAL agents (MAL-CONTEXT, MAL-ERROR, MAL-KNOWLEDGE, MAL-TASK, MAL-WORKFLOW), tool permission model (Section 2.12), updated agent quick reference |
| 4.1.1 | 2025-12-10 | Cycle 5 Enhancements: MED-016 - Added knowledge_store specification to MAL-KNOWLEDGE (Section 2.9); MED-020 - Added scope_clarification to MAL-WORKFLOW (Section 2.11) |
| 4.1.2 | 2025-12-10 | Updated Section 3.1 Agent Execution Order to include all 11 agents with 5-phase coordination flow (Phase 0: MAL-CONTEXT/MAL-ERROR continuous monitoring; Phase 1: 5-agent parallel assessment; Phase 2: MAL-CONVERGENCE→MAL-WORKFLOW sequential; Phase 3: MAL-ADVERSARIAL challenge; Phase 4: MAL-KNOWLEDGE synthesis); Added Section 3.3 SKYNET Agent Integration Specifics with detailed phase assignment, tool permissions, coordination dependencies, and migration guidance |

---

*This document is part of the USF 4.0 specification suite. See MASTER-SPECIFICATION.md for framework overview.*
