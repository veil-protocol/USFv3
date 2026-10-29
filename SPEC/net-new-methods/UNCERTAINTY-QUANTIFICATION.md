# USF 4.0: Uncertainty Quantification

> **Version**: 4.0.0
> **Component**: Precision / Uncertainty Quantification
> **Status**: Specification
> **Dependencies**: VERIFICATION-CHAINS.md, PRECISION-CALIBRATOR.md

---

## 1. Overview

Uncertainty Quantification (UQ) provides calibrated, multi-dimensional uncertainty estimates for all USF outputs. Rather than single-point confidence scores, UQ characterizes what we know, what we don't know, and why—enabling informed decision-making.

```
UNCERTAINTY QUANTIFICATION ARCHITECTURE
═══════════════════════════════════════════════════════════════════════════════

    INPUTS                          ANALYSIS                       OUTPUT
    ──────                          ────────                       ──────

    ┌─────────────┐
    │   CHAIN     │───┐
    │  VERDICTS   │   │
    └─────────────┘   │         ┌────────────────────────────┐
                      │         │                            │
    ┌─────────────┐   │         │   UNCERTAINTY ENGINE       │    ┌─────────┐
    │   EXPERT    │───┼────────►│                            │───►│ MULTI-  │
    │  AGREEMENT  │   │         │ • Epistemic Analysis       │    │ DIMEN-  │
    └─────────────┘   │         │ • Aleatory Analysis        │    │ SIONAL  │
                      │         │ • Model Uncertainty        │    │ UNCERT- │
    ┌─────────────┐   │         │ • Calibration              │    │ AINTY   │
    │ ASSUMPTION  │───┘         │                            │    │ PROFILE │
    │   CATALOG   │             └────────────────────────────┘    └─────────┘
    └─────────────┘

═══════════════════════════════════════════════════════════════════════════════
```

---

## 2. Uncertainty Dimensions

### 2.1 Epistemic Uncertainty

```yaml
epistemic_uncertainty:
  definition: |
    Uncertainty due to lack of knowledge. Can be reduced with more
    information, analysis, or expertise.

  sources:
    incomplete_information:
      description: "Missing data or context"
      examples:
        - "Threat model not fully specified"
        - "System dependencies unknown"
        - "Historical data unavailable"
      reducibility: "Can be reduced by gathering more information"

    limited_analysis:
      description: "Analysis scope insufficient"
      examples:
        - "Not all code paths analyzed"
        - "Limited test coverage"
        - "Time-bounded verification"
      reducibility: "Can be reduced by deeper analysis"

    knowledge_gaps:
      description: "Expertise limitations"
      examples:
        - "Novel domain with limited precedent"
        - "Cutting-edge technology"
        - "Expert disagreement"
      reducibility: "Can be reduced by acquiring expertise"

  quantification:
    method: "Bayesian inference with prior and evidence"
    representation: "Probability distribution over possible states"
    reporting:
      point_estimate: "Most likely value"
      credible_interval: "Range containing true value with P probability"
      distribution: "Full probability distribution if needed"
```

### 2.2 Aleatory Uncertainty

```yaml
aleatory_uncertainty:
  definition: |
    Uncertainty due to inherent randomness or variability.
    Cannot be reduced with more information.

  sources:
    natural_variability:
      description: "Genuine randomness in system"
      examples:
        - "Network latency variability"
        - "User behavior variation"
        - "Physical measurement noise"
      reducibility: "Cannot reduce, only characterize"

    adversary_behavior:
      description: "Unpredictable adversary choices"
      examples:
        - "Which attack vector adversary chooses"
        - "Timing of attacks"
        - "Novel attack methods"
      reducibility: "Cannot reduce, but can bound"

    environmental_variation:
      description: "Deployment environment differences"
      examples:
        - "Different hardware configurations"
        - "Different usage patterns"
        - "Different threat environments"
      reducibility: "Cannot reduce, can model scenarios"

  quantification:
    method: "Statistical modeling of variability"
    representation: "Probability distribution of outcomes"
    reporting:
      expected_value: "Average outcome"
      variance: "Spread of outcomes"
      quantiles: "Specific percentiles (p95, p99)"
```

### 2.3 Model Uncertainty

```yaml
model_uncertainty:
  definition: |
    Uncertainty about whether our models and assumptions
    accurately represent reality.

  sources:
    model_assumptions:
      description: "Assumptions may be wrong"
      examples:
        - "Threat model may be incomplete"
        - "Behavioral assumptions may be violated"
        - "Adversary may be more capable"

    abstraction_loss:
      description: "Abstraction loses important details"
      examples:
        - "Formal model misses implementation detail"
        - "Simplified threat model misses attack"
        - "Testing doesn't cover deployment environment"

    specification_errors:
      description: "Specification doesn't match intent"
      examples:
        - "Requirement ambiguity"
        - "Missing requirements"
        - "Conflicting requirements"

  quantification:
    method: "Sensitivity analysis and model comparison"
    representation:
      assumption_sensitivity: "Impact if assumption violated"
      model_comparison: "Difference across model variations"
    reporting:
      key_assumptions: "List of critical assumptions"
      sensitivity_ranking: "Which assumptions matter most"
      alternative_models: "Results under alternative models"
```

---

## 3. Uncertainty Aggregation

### 3.1 Component Uncertainty Combination

```yaml
uncertainty_combination:
  independent_components:
    method: "Combine independent uncertainty sources"
    formula: |
      For independent random variables:
      Var(X + Y) = Var(X) + Var(Y)

      For confidence:
      P(all correct) = P(X correct) × P(Y correct)

  dependent_components:
    method: "Account for correlations"
    formula: |
      Var(X + Y) = Var(X) + Var(Y) + 2×Cov(X,Y)

    correlation_estimation:
      - "Common assumptions create positive correlation"
      - "Adversarial diversity creates negative correlation"
      - "Shared data sources create positive correlation"

  hierarchical_aggregation:
    process:
      1: "Combine uncertainties within each claim"
      2: "Combine claim uncertainties within component"
      3: "Combine component uncertainties for system"

    aggregation_rules:
      conservative: "Take maximum uncertainty"
      mean: "Average uncertainties"
      weighted: "Weight by importance"
```

### 3.2 Chain Agreement to Uncertainty

```yaml
chain_to_uncertainty:
  agreement_mapping:
    unanimous_agreement:
      epistemic: "Low"
      interpretation: "High confidence in finding"

    supermajority:
      epistemic: "Low-Moderate"
      interpretation: "Good confidence, minor uncertainty"

    majority:
      epistemic: "Moderate"
      interpretation: "Reasonable confidence, notable uncertainty"

    split:
      epistemic: "High"
      interpretation: "Significant uncertainty, disagreement"

  disagreement_analysis:
    when_chains_disagree:
      1: "Identify source of disagreement"
      2: "Classify as epistemic vs aleatory"
      3: "Determine if reducible"
      4: "Report appropriately"
```

---

## 4. Calibration

### 4.1 Confidence Calibration

```yaml
confidence_calibration:
  goal: |
    Ensure stated confidence matches actual accuracy.
    When we say 90% confident, we should be correct 90% of the time.

  calibration_measurement:
    method: "Compare predicted confidence to observed accuracy"
    process:
      1: "Collect predictions with confidence levels"
      2: "Group by confidence bucket (e.g., 80-85%, 85-90%)"
      3: "Calculate actual accuracy per bucket"
      4: "Compare predicted vs actual"

    metrics:
      expected_calibration_error:
        formula: "Σ |predicted_confidence - observed_accuracy| × bucket_weight"
        target: "< 0.05"

      reliability_diagram:
        description: "Plot of predicted vs actual accuracy"
        ideal: "45-degree line"

  calibration_adjustment:
    when_overconfident:
      detection: "Accuracy < stated confidence"
      adjustment: "Reduce confidence scores"

    when_underconfident:
      detection: "Accuracy > stated confidence"
      adjustment: "Increase confidence scores"

    adjustment_method:
      isotonic_regression: "Non-parametric calibration"
      platt_scaling: "Logistic calibration"
      temperature_scaling: "Simple divisor adjustment"
```

### 4.2 Calibration Monitoring

```yaml
calibration_monitoring:
  continuous_tracking:
    data_collection:
      - "All confidence predictions"
      - "Outcome data where available"
      - "User feedback on accuracy"

    analysis_frequency: "Weekly aggregate analysis"

    alert_thresholds:
      drift_warning: "ECE > 0.05"
      drift_critical: "ECE > 0.10"

  calibration_refresh:
    trigger: "Drift exceeds threshold"
    process:
      1: "Collect recent prediction-outcome pairs"
      2: "Fit new calibration curve"
      3: "Validate on held-out data"
      4: "Deploy updated calibration"
```

---

## 5. Uncertainty Reporting

### 5.1 Uncertainty Profile

```yaml
uncertainty_profile:
  structure:
    overall_confidence:
      value: 0.87
      calibrated: true
      interpretation: "High confidence in overall finding"

    epistemic_uncertainty:
      level: "Low-Moderate"
      sources:
        - source: "Limited historical precedent"
          reducible: true
          reduction_method: "Gather more case studies"
        - source: "Incomplete threat model"
          reducible: true
          reduction_method: "Expand threat analysis"

    aleatory_uncertainty:
      level: "Moderate"
      sources:
        - source: "Adversary behavior variability"
          characterization: "Bounded by adversary capability"
        - source: "Environmental variation"
          characterization: "Covered by scenario analysis"

    model_uncertainty:
      level: "Low"
      key_assumptions:
        - assumption: "Adversary limited to network access"
          sensitivity: "HIGH if violated"
          alternative: "Physical access changes conclusions"
        - assumption: "Cryptographic primitives secure"
          sensitivity: "CRITICAL if violated"
          validation: "Based on current cryptanalytic knowledge"

    confidence_breakdown:
      by_claim:
        - claim: "Protocol provides forward secrecy"
          confidence: 0.95
          uncertainty_type: "Mostly epistemic"
        - claim: "Implementation timing-safe"
          confidence: 0.78
          uncertainty_type: "Epistemic + Model"
```

### 5.2 Uncertainty Visualization

```
UNCERTAINTY VISUALIZATION FORMATS
═══════════════════════════════════════════════════════════════════════════════

CONFIDENCE METER:
  ▓▓▓▓▓▓▓▓▓░░░░░░░░░░  87% Confidence
           ↑
       Uncertainty zone

UNCERTAINTY DECOMPOSITION:
  Epistemic    ████░░░░░░  30%
  Aleatory     ██░░░░░░░░  15%
  Model        █░░░░░░░░░   8%
               ──────────
  Total Uncertainty: ~45%

CONFIDENCE INTERVAL:
  Point estimate: 87%
  80% CI: [79%, 93%]
  95% CI: [72%, 96%]

  ├───────[====●====]───────┤
  72%    79%  87%  93%    96%

ASSUMPTION SENSITIVITY:
  Assumption A ●────────────────── High sensitivity
  Assumption B ●──────────         Moderate sensitivity
  Assumption C ●────               Low sensitivity

═══════════════════════════════════════════════════════════════════════════════
```

### 5.3 Actionable Uncertainty Communication

```yaml
actionable_communication:
  principles:
    - "Express uncertainty in terms users can act on"
    - "Distinguish reducible from irreducible uncertainty"
    - "Identify what would change the assessment"

  templates:
    high_confidence:
      template: |
        Confidence: {confidence}%
        This assessment is highly confident. Key assumptions are well-validated.
        To increase confidence further: {reduction_actions}

    moderate_confidence:
      template: |
        Confidence: {confidence}%
        This assessment has moderate uncertainty due to: {uncertainty_sources}
        These uncertainties could be reduced by: {reduction_actions}
        If these assumptions are violated: {violation_consequences}

    low_confidence:
      template: |
        Confidence: {confidence}%
        WARNING: This assessment has significant uncertainty.
        Key sources of uncertainty: {uncertainty_sources}
        Critical assumptions that may not hold: {risky_assumptions}
        Before acting on this, consider: {recommendations}
```

---

## 6. Uncertainty-Aware Decision Support

### 6.1 Decision Thresholds

```yaml
decision_thresholds:
  purpose: "Map uncertainty to action recommendations"

  threshold_framework:
    high_confidence_action:
      threshold: "Confidence > 90%, Low epistemic"
      recommendation: "Act on assessment"

    moderate_confidence_action:
      threshold: "Confidence 70-90%"
      recommendation: "Consider acting with monitoring"
      caveats: "Document assumptions, plan for alternatives"

    low_confidence_caution:
      threshold: "Confidence 50-70%"
      recommendation: "Gather more information before acting"
      alternatives: "Consider reversible actions only"

    high_uncertainty_pause:
      threshold: "Confidence < 50% or High model uncertainty"
      recommendation: "Do not act on assessment"
      required: "Further analysis or accept high risk"
```

### 6.2 Value of Information Analysis

```yaml
value_of_information:
  purpose: "Determine if gathering more information is worthwhile"

  voi_calculation:
    expected_value_with_info: "E[outcome | perfect information]"
    expected_value_without_info: "E[outcome | current information]"
    cost_of_information: "Resources to gather information"

    voi: "E[with] - E[without] - cost"

    decision:
      positive_voi: "Worth gathering more information"
      negative_voi: "Act on current information"

  practical_application:
    for_each_reducible_uncertainty:
      - "Estimate how much reduction possible"
      - "Estimate cost to reduce"
      - "Estimate value of reduction"
      - "Recommend if VOI positive"
```

---

## 7. False Confidence Detection

### 7.1 Overconfidence Indicators

```yaml
overconfidence_indicators:
  structural_indicators:
    too_few_chains:
      description: "High confidence with limited verification"
      detection: "Confidence > 90% with < 4 chains"
      response: "Flag for review, require more chains"

    unanimous_too_fast:
      description: "Quick unanimous agreement"
      detection: "All chains agree in < 2 iterations"
      response: "Force adversarial challenge"

    no_assumptions_documented:
      description: "No explicit assumptions despite complexity"
      detection: "Zero model assumptions for complex analysis"
      response: "Require assumption documentation"

  behavioral_indicators:
    expert_overconfidence:
      description: "Experts historically overconfident"
      detection: "Expert's past predictions poorly calibrated"
      response: "Discount expert's confidence"

    complexity_blindness:
      description: "Underestimating complex system issues"
      detection: "Simple analysis of complex system"
      response: "Require deeper analysis"
```

### 7.2 Hidden Assumption Detection

```yaml
hidden_assumption_detection:
  purpose: "Find assumptions not explicitly documented"

  detection_methods:
    negative_space_analysis:
      method: "Identify what's NOT being questioned"
      process:
        - "List all potential assumptions"
        - "Identify which are validated"
        - "Flag unvalidated assumptions"

    devil_advocate:
      method: "Force challenges to consensus"
      process:
        - "Assign expert to challenge every conclusion"
        - "Identify defensive responses indicating hidden assumptions"

    cross_domain_challenge:
      method: "Apply different domain's assumptions"
      process:
        - "Ask how different domain would view same problem"
        - "Identify assumptions that don't transfer"

  assumption_categories:
    environmental: "Assumptions about operating environment"
    adversarial: "Assumptions about adversary"
    technical: "Assumptions about technology"
    organizational: "Assumptions about people/process"
    temporal: "Assumptions about timing/sequence"
```

---

## 8. Integration Points

### 8.1 Verification Chains Integration

```yaml
verification_chains:
  receives: "Chain verdicts and per-chain confidence"
  produces: "Aggregated uncertainty from chain agreement"
```

### 8.2 Meta-Analysis Integration

```yaml
meta_analysis:
  agent: "MAL-QUALITY"
  tracks: "Calibration accuracy over time"
  proposes: "Calibration adjustments"

  agent: "MAL-CONVERGENCE"
  tracks: "Uncertainty reduction patterns"
  proposes: "Uncertainty reduction strategies"
```

### 8.3 Output Integration

```yaml
output_integration:
  all_outputs_include:
    - "Confidence score (calibrated)"
    - "Uncertainty type breakdown"
    - "Key assumptions"
    - "Sensitivity analysis"
```

---

## Appendix A: Uncertainty Quantification Quick Reference

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                USF 4.0 UNCERTAINTY QUANTIFICATION REFERENCE                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  DIMENSIONS:                                                                 ║
║    Epistemic: Knowledge gaps (reducible)                                     ║
║    Aleatory: Inherent randomness (irreducible)                              ║
║    Model: Assumption/abstraction errors                                      ║
║                                                                              ║
║  CALIBRATION: Ensure stated confidence matches actual accuracy               ║
║    Target: Expected Calibration Error < 5%                                   ║
║                                                                              ║
║  REPORTING: Uncertainty profile with sources and reduction options           ║
║                                                                              ║
║  FALSE CONFIDENCE: Detect overconfidence and hidden assumptions              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## Appendix B: Change Log

| Version | Date | Changes |
|---------|------|---------|
| 4.0.0 | 2025-12-10 | Initial USF 4.0 uncertainty quantification specification |

---

*This document is part of the USF 4.0 specification suite. See MASTER-SPECIFICATION.md for framework overview.*
