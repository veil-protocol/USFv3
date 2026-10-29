# USF 4.0: Domain Detector

> **Version**: 4.0.0
> **Component**: Domain Adaptation / Domain Detector
> **Status**: Specification
> **Dependencies**: core/DOMAIN-TAXONOMY.md, MASTER-SPECIFICATION.md

---

## 1. Overview

The Domain Detector automatically classifies any input task into the USF domain taxonomy without requiring manual configuration. It uses multi-signal analysis to identify primary and secondary domains with calibrated confidence scores.

```
DOMAIN DETECTION PIPELINE
═══════════════════════════════════════════════════════════════════════════════

    INPUT: Task Description / Problem Statement
                        │
                        ▼
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                      SIGNAL EXTRACTION                                   │
    │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                  │
    │  │   LEXICAL    │  │  STRUCTURAL  │  │   SEMANTIC   │                  │
    │  │   SIGNALS    │  │   SIGNALS    │  │   SIGNALS    │                  │
    │  │              │  │              │  │              │                  │
    │  │ Terminology  │  │ Doc patterns │  │ Embeddings   │                  │
    │  │ Jargon       │  │ Format cues  │  │ Similarity   │                  │
    │  │ Keywords     │  │ References   │  │ Clustering   │                  │
    │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘                  │
    │         │                 │                 │                           │
    │         └─────────────────┼─────────────────┘                           │
    │                           ▼                                             │
    └─────────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                      DOMAIN CLASSIFICATION                               │
    │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                  │
    │  │  HIERARCHY   │  │  CONFIDENCE  │  │  SECONDARY   │                  │
    │  │  TRAVERSAL   │  │  CALCULATION │  │  DETECTION   │                  │
    │  └──────────────┘  └──────────────┘  └──────────────┘                  │
    └─────────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ OUTPUT: DomainProfile                                                    │
    │   primary: "T.SEC.CRY.SYM"                                              │
    │   secondary: ["T.NET.PRO", "T.DEV.SYS"]                                 │
    │   confidence: 0.92                                                      │
    │   signals: { lexical: 0.95, structural: 0.88, semantic: 0.91 }         │
    └─────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════
```

---

## 2. Signal Extraction

### 2.1 Lexical Analysis

```yaml
lexical_analysis:
  purpose: "Identify domain through terminology and jargon"

  components:
    keyword_detection:
      method: "Match against domain-specific keyword dictionaries"
      dictionaries:
        T.SEC.CRY: ["encryption", "cipher", "key exchange", "hash", "signature"]
        T.SEC.NET: ["firewall", "IDS", "packet", "intrusion", "SIEM"]
        T.SEC.APP: ["XSS", "SQL injection", "CSRF", "authentication"]
        T.DEV.WEB: ["API", "REST", "frontend", "backend", "HTTP"]
        T.DEV.SYS: ["kernel", "driver", "memory", "syscall", "process"]
        B.FIN.TRD: ["portfolio", "arbitrage", "hedge", "derivative"]
        S.MED.DIA: ["symptom", "diagnosis", "pathology", "etiology"]
        # ... comprehensive dictionaries for all domains
      scoring:
        match_weight: "Count × term specificity"
        specificity: "Inverse document frequency across domains"

    jargon_recognition:
      method: "Identify domain-specific phrases and acronyms"
      patterns:
        T.SEC: ["APT", "CVE", "0-day", "threat actor", "IOC"]
        T.DEV: ["CI/CD", "microservice", "container", "K8s"]
        L.LEG: ["plaintiff", "defendant", "pursuant to", "prima facie"]
        S.MED: ["prognosis", "contraindicated", "etiology"]
      scoring:
        jargon_density: "Jargon terms / total terms"
        jargon_consistency: "Single domain vs mixed jargon"

    entity_extraction:
      method: "Extract named entities relevant to domains"
      entity_types:
        technology: ["product names", "protocol names", "tool names"]
        organization: ["company names", "regulatory bodies"]
        standards: ["ISO", "NIST", "RFC", "IEEE"]
      mapping:
        entity_to_domain: "Map extracted entities to likely domains"

  output:
    lexical_scores:
      per_domain: "Score for each domain based on lexical signals"
      top_candidates: "Top 5 domains by lexical score"
      confidence: "How distinctive the lexical signal is"
```

### 2.2 Structural Analysis

```yaml
structural_analysis:
  purpose: "Identify domain through document structure and format"

  components:
    document_pattern_detection:
      patterns:
        security_assessment:
          indicators:
            - "Vulnerability findings section"
            - "Risk ratings (Critical/High/Medium/Low)"
            - "Remediation recommendations"
            - "Executive summary + technical details"
          domain: "T.SEC.*"

        legal_document:
          indicators:
            - "Numbered paragraphs/sections"
            - "Case citations"
            - "Whereas clauses"
            - "Party definitions"
          domain: "L.*"

        scientific_paper:
          indicators:
            - "Abstract"
            - "Introduction/Methods/Results/Discussion"
            - "References section"
            - "Figures and tables with captions"
          domain: "S.*"

        business_report:
          indicators:
            - "Executive summary"
            - "Market analysis section"
            - "Financial projections"
            - "Recommendations"
          domain: "B.*"

        code_review:
          indicators:
            - "Code blocks"
            - "File paths"
            - "Function signatures"
            - "Line number references"
          domain: "T.DEV.*"

    reference_analysis:
      method: "Analyze cited sources and references"
      signals:
        academic_papers: "Scientific domains"
        rfcs_standards: "Technology/networking domains"
        case_law: "Legal domains"
        regulatory_docs: "Compliance/regulatory domains"
        code_repos: "Development domains"

    format_cues:
      method: "Detect format-specific patterns"
      patterns:
        threat_model_format: "STRIDE, Attack Trees → T.SEC"
        uml_diagrams: "Class/sequence diagrams → T.DEV"
        circuit_diagrams: "Schematic notation → E.ENG.ELE"
        chemical_formulas: "Molecular notation → S.CHE"

  output:
    structural_scores:
      per_domain: "Score based on structural patterns"
      pattern_matches: "Which patterns were detected"
      confidence: "How clear the structural signal is"
```

### 2.3 Semantic Analysis

```yaml
semantic_analysis:
  purpose: "Deep semantic understanding for domain classification"

  components:
    embedding_similarity:
      method: "Compare input embedding to domain prototype embeddings"
      process:
        1: "Generate embedding of input text"
        2: "Compare to pre-computed domain prototype embeddings"
        3: "Calculate cosine similarity to each domain"
        4: "Rank domains by similarity"
      domain_prototypes:
        source: "Representative texts from each domain"
        update_frequency: "Monthly or on taxonomy change"

    topic_modeling:
      method: "Extract topics and map to domains"
      process:
        1: "Extract latent topics from input"
        2: "Match topics to domain topic distributions"
        3: "Calculate domain probability"
      topic_domain_mapping:
        pre_trained: "Topic→Domain mapping from training data"

    cross_domain_detection:
      method: "Identify inputs spanning multiple domains"
      indicators:
        - "Distinct topic clusters in single input"
        - "Mixed vocabulary from different domains"
        - "Explicit multi-domain references"
      output: "List of secondary domains"

    context_understanding:
      method: "Understand task context beyond literal text"
      aspects:
        task_type: "Analysis, design, review, implementation"
        depth_required: "Overview vs deep dive"
        output_expected: "Report, code, recommendation"
      influence: "Refines domain classification"

  output:
    semantic_scores:
      per_domain: "Semantic similarity score"
      embedding_distances: "Distance to domain prototypes"
      topic_alignment: "Topic-based domain probability"
      confidence: "Semantic signal strength"
```

---

## 3. Classification Algorithm

### 3.1 Signal Fusion

```yaml
signal_fusion:
  purpose: "Combine multiple signals into unified domain classification"

  fusion_weights:
    lexical: 0.35
    structural: 0.25
    semantic: 0.40

  dynamic_weight_adjustment:
    conditions:
      - condition: "High lexical specificity (rare terms)"
        adjustment: "Increase lexical weight to 0.45"

      - condition: "Clear document structure"
        adjustment: "Increase structural weight to 0.35"

      - condition: "Ambiguous lexical signals"
        adjustment: "Increase semantic weight to 0.50"

      - condition: "Short input (< 100 words)"
        adjustment: "Decrease structural, increase lexical"

  fusion_algorithm:
    ```
    FOR EACH domain IN taxonomy:
      raw_score[domain] = (
        lexical_score[domain] × lexical_weight +
        structural_score[domain] × structural_weight +
        semantic_score[domain] × semantic_weight
      )

    // Normalize scores
    total = SUM(raw_score)
    normalized_score[domain] = raw_score[domain] / total

    // Apply hierarchy constraints
    final_score = apply_hierarchy_consistency(normalized_score)
    ```

  output:
    fused_scores: "Per-domain combined scores"
    signal_contributions: "Which signals drove classification"
```

### 3.2 Hierarchy Traversal

```yaml
hierarchy_traversal:
  purpose: "Navigate taxonomy to find most specific applicable domain"

  algorithm:
    ```
    START at taxonomy root

    WHILE can_go_deeper:
      current_level_scores = scores for all children of current node
      best_child = argmax(current_level_scores)

      IF best_child.score > threshold AND
         best_child.score - second_best.score > margin:
        DESCEND to best_child
      ELSE:
        STOP at current level

    RETURN current node as primary domain
    ```

  thresholds:
    category_threshold: 0.3   # Minimum to select category
    subcategory_threshold: 0.4  # Minimum to select subcategory
    specific_threshold: 0.5   # Minimum to select specific domain
    margin_requirement: 0.1   # Minimum lead over second choice

  confidence_calculation:
    base_confidence: "Highest normalized score"
    depth_adjustment:
      shallow: "+0.05 (easier to classify broadly)"
      deep: "-0.05 (harder to be specific)"
    margin_adjustment: "Higher margin → higher confidence"
    signal_agreement: "Agreement across signals → higher confidence"
```

### 3.3 Secondary Domain Detection

```yaml
secondary_domain_detection:
  purpose: "Identify additional relevant domains beyond primary"

  detection_criteria:
    score_threshold: 0.3  # Minimum score to consider
    primary_ratio: 0.5    # Must be at least 50% of primary score
    maximum_secondary: 3  # Maximum secondary domains

  detection_algorithm:
    ```
    primary = classify_primary(input)
    candidates = []

    FOR EACH domain IN taxonomy:
      IF domain != primary AND
         domain.score >= score_threshold AND
         domain.score >= primary.score × primary_ratio AND
         NOT ancestor_of(domain, primary) AND
         NOT descendant_of(domain, primary):
        candidates.append(domain)

    secondary = top_k(candidates, k=maximum_secondary)
    RETURN secondary
    ```

  cross_domain_patterns:
    detected_patterns:
      security_development:
        primary: "T.SEC.*"
        secondary: ["T.DEV.*"]
        trigger: "Secure coding, security in SDLC"

      legal_technology:
        primary: "L.*"
        secondary: ["T.*"]
        trigger: "Technology law, IP, privacy regulation"

      medical_ai:
        primary: "S.MED.*"
        secondary: ["T.DAT.ML"]
        trigger: "Medical AI, diagnostic algorithms"
```

---

## 4. Domain Profile Output

### 4.1 Profile Structure

```yaml
domain_profile:
  structure:
    primary:
      domain_id: "Full domain identifier (e.g., T.SEC.CRY.SYM)"
      domain_name: "Human-readable name"
      domain_path: ["T", "SEC", "CRY", "SYM"]

    secondary:
      - domain_id: "Secondary domain 1"
        relevance: 0.7  # Relevance to task
      - domain_id: "Secondary domain 2"
        relevance: 0.5

    confidence:
      overall: 0.92  # Overall classification confidence
      per_signal:
        lexical: 0.95
        structural: 0.88
        semantic: 0.91
      calibrated: true  # Whether confidence is calibrated

    metadata:
      classification_time_ms: 45
      signals_used: ["lexical", "structural", "semantic"]
      ambiguity_flags: []  # Any classification concerns

    recommendations:
      template: "TMPL-SEC"  # Suggested phase template
      precision_default: "PL3"  # Suggested precision level
      expert_emphasis: ["ARC-AD", "ARC-TH"]  # Key archetypes
```

### 4.2 Confidence Calibration

```yaml
confidence_calibration:
  purpose: "Ensure confidence scores match actual accuracy"

  calibration_method:
    training:
      - "Collect classified tasks with known ground truth"
      - "Group by confidence bucket (0.5-0.6, 0.6-0.7, etc.)"
      - "Calculate accuracy per bucket"
      - "Fit calibration curve"

    application:
      - "Raw confidence from classifier"
      - "Apply calibration curve"
      - "Output calibrated confidence"

  calibration_validation:
    metric: "Expected Calibration Error (ECE)"
    target: "ECE < 0.05"
    frequency: "Recalibrate monthly"

  confidence_interpretation:
    "[0.9, 1.0]": "Very high confidence - classification reliable"
    "[0.8, 0.9)": "High confidence - likely correct"
    "[0.7, 0.8)": "Moderate confidence - may need verification"
    "[0.5, 0.7)": "Low confidence - recommend human review"
    "[0, 0.5)": "Very low - classification uncertain"
```

---

## 5. Edge Cases and Fallbacks

### 5.1 Ambiguous Inputs

```yaml
ambiguous_handling:
  detection:
    indicators:
      - "Primary and secondary very close in score"
      - "Signals disagree significantly"
      - "Low confidence across all signals"
      - "Input matches multiple disjoint domains"

  strategies:
    close_scores:
      threshold: "Primary - secondary < 0.1"
      action:
        - "Flag as ambiguous"
        - "Return both as co-primary"
        - "Reduce confidence"
        - "Recommend clarification"

    signal_disagreement:
      threshold: "Max signal difference > 0.3"
      action:
        - "Investigate disagreement cause"
        - "Weight toward most reliable signal for input type"
        - "Document uncertainty"

    low_confidence:
      threshold: "Confidence < 0.5"
      action:
        - "Flag for human review"
        - "Suggest possible domains"
        - "Request additional context"
```

### 5.2 Novel Domains

```yaml
novel_domain_handling:
  detection:
    indicators:
      - "No domain score exceeds threshold"
      - "Semantic embedding far from all prototypes"
      - "Unfamiliar terminology pattern"
      - "Structural pattern not recognized"

  response:
    immediate:
      - "Classify to nearest domain (with low confidence)"
      - "Flag as potential novel domain"
      - "Log for taxonomy review"

    follow_up:
      - "Trigger MAL-COVERAGE analysis"
      - "Collect similar novel inputs"
      - "Propose taxonomy expansion if pattern emerges"

  fallback_classification:
    method: "Classify to broadest matching category"
    example:
      input: "Quantum computing security analysis"
      novel_aspect: "Quantum computing not in taxonomy"
      fallback: "T.SEC (security, broad category)"
      flag: "Potential new domain: T.SEC.QUA or similar"
```

### 5.3 Minimal Input

```yaml
minimal_input_handling:
  detection:
    threshold: "Input < 50 words"

  adjusted_processing:
    lexical:
      weight_increase: "+0.15"
      reason: "Each word more significant"

    structural:
      weight_decrease: "-0.15"
      reason: "Limited structure to analyze"

    semantic:
      unchanged: true
      but: "Higher variance expected"

  confidence_adjustment:
    method: "Reduce confidence proportional to input length"
    formula: "confidence × min(1, input_length / 100)"

  enhancement_request:
    trigger: "Confidence < 0.6 with minimal input"
    action: "Request additional context from user"
```

---

## 6. Performance Optimization

### 6.1 Caching

```yaml
caching:
  domain_prototypes:
    storage: "In-memory"
    update: "On taxonomy change"
    format: "Pre-computed embeddings"

  keyword_indices:
    storage: "Trie-based index"
    update: "On dictionary change"
    lookup: "O(k) where k = keyword length"

  recent_classifications:
    storage: "LRU cache"
    size: "1000 entries"
    key: "Hash of input text"
    ttl: "1 hour"
    benefit: "Avoid re-classification of same input"
```

### 6.2 Parallel Processing

```yaml
parallel_processing:
  signal_extraction:
    parallelizable: true
    strategy: "Run lexical, structural, semantic in parallel"
    merge: "Join before fusion"

  large_input_handling:
    chunking:
      trigger: "Input > 5000 words"
      method: "Split into overlapping chunks"
      merge: "Aggregate chunk classifications"
```

### 6.3 Latency Targets

```yaml
latency_targets:
  typical_input:
    definition: "100-1000 words"
    target: "< 100ms"
    p99: "< 200ms"

  large_input:
    definition: "> 5000 words"
    target: "< 500ms"
    p99: "< 1000ms"

  minimal_input:
    definition: "< 50 words"
    target: "< 50ms"
    p99: "< 100ms"
```

---

## 7. Integration Points

### 7.1 Input Interface

```yaml
input_interface:
  primary_input:
    type: "Text"
    format: "UTF-8 string"
    required: true

  optional_inputs:
    context_hints:
      type: "List of domain hints"
      purpose: "Bias classification toward hinted domains"

    previous_classification:
      type: "DomainProfile"
      purpose: "For reclassification with new context"

    output_type_hint:
      type: "String"
      values: ["report", "code", "recommendation", "analysis"]
      purpose: "Refine classification based on expected output"
```

### 7.2 Output Interface

```yaml
output_interface:
  domain_profile:
    format: "Structured DomainProfile object"
    includes: "Primary, secondary, confidence, metadata"

  downstream_consumers:
    template_selector:
      receives: "domain_profile.primary"
      uses_for: "Template selection"

    expert_generator:
      receives: "domain_profile"
      uses_for: "Expert persona synthesis"

    precision_calibrator:
      receives: "domain_profile"
      uses_for: "Precision level default"
```

### 7.3 Feedback Loop

```yaml
feedback_loop:
  classification_correction:
    trigger: "Human or system corrects classification"
    action:
      - "Log correction"
      - "Update calibration data"
      - "Flag for prototype update if pattern emerges"

  accuracy_monitoring:
    frequency: "Weekly aggregate"
    metrics:
      - "Classification accuracy (where ground truth available)"
      - "Confidence calibration"
      - "Novel domain rate"
```

---

## 8. Domain Detection Examples

### 8.1 Clear Classification

```yaml
example_clear:
  input: |
    Analyze the security of the AES-256-GCM implementation in our
    TLS 1.3 handshake. Focus on timing side-channels and key
    derivation correctness. Consider nation-state adversaries.

  lexical_signals:
    matches: ["AES-256-GCM", "TLS 1.3", "timing side-channels",
              "key derivation", "nation-state adversaries"]
    domain_hints: ["T.SEC.CRY", "T.SEC.PRO", "T.SEC.OFF"]

  structural_signals:
    pattern: "Security analysis request"
    domain_hint: "T.SEC.*"

  semantic_signals:
    embedding_similarity:
      T.SEC.CRY: 0.94
      T.SEC.PRO: 0.82
      T.NET.SEC: 0.71

  classification:
    primary: "T.SEC.CRY.SYM"
    secondary: ["T.SEC.PRO.TLS"]
    confidence: 0.96
```

### 8.2 Multi-Domain Classification

```yaml
example_multi:
  input: |
    We need to assess whether our AI-based diagnostic system
    complies with FDA regulations and HIPAA requirements.
    Consider both the machine learning model accuracy and
    the data privacy implications.

  lexical_signals:
    matches: ["AI-based diagnostic", "FDA regulations", "HIPAA",
              "machine learning model", "data privacy"]
    domain_hints: ["S.MED", "L.REG", "T.DAT.ML", "T.SEC.PRV"]

  structural_signals:
    pattern: "Compliance assessment"
    domain_hints: ["L.REG.*"]

  classification:
    primary: "L.REG.HEA"  # Healthcare regulation
    secondary:
      - domain: "S.MED.DIA"
        relevance: 0.8
      - domain: "T.DAT.ML"
        relevance: 0.7
      - domain: "T.SEC.PRV"
        relevance: 0.6
    confidence: 0.88
```

### 8.3 Ambiguous Classification

```yaml
example_ambiguous:
  input: |
    Review the system and provide recommendations.

  lexical_signals:
    matches: ["system", "recommendations"]
    domain_hints: "Too generic, no clear domain"

  structural_signals:
    pattern: "None clear"

  semantic_signals:
    embedding_similarity: "Low similarity to all prototypes"

  classification:
    primary: "X.GEN"  # Generic/cross-domain
    secondary: []
    confidence: 0.35
    flags: ["ambiguous_input", "request_clarification"]

  follow_up:
    system_response: |
      Classification is ambiguous. Please provide more context:
      - What type of system? (software, business, medical, etc.)
      - What aspect to review? (security, performance, compliance, etc.)
      - Who is the audience for recommendations?
```

---

## Appendix A: Domain Detector Quick Reference

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    USF 4.0 DOMAIN DETECTOR REFERENCE                         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  SIGNALS: Lexical (35%) + Structural (25%) + Semantic (40%)                 ║
║                                                                              ║
║  OUTPUT: DomainProfile { primary, secondary[], confidence }                  ║
║                                                                              ║
║  CONFIDENCE LEVELS:                                                          ║
║    0.9-1.0: Very high    0.8-0.9: High    0.7-0.8: Moderate                 ║
║    0.5-0.7: Low          0.0-0.5: Very low (flag for review)                ║
║                                                                              ║
║  LATENCY: <100ms typical, <500ms large inputs                               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## Appendix B: Change Log

| Version | Date | Changes |
|---------|------|---------|
| 4.0.0 | 2025-12-10 | Initial USF 4.0 domain detector specification |

---

*This document is part of the USF 4.0 specification suite. See MASTER-SPECIFICATION.md for framework overview.*
