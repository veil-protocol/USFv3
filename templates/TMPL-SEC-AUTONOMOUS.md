# USF 4.2: Autonomous Security Analysis Template (TMPL-SEC-AUTO)

> **Version**: 4.2.0
> **Component**: Templates / Security / Autonomous
> **Status**: Specification
> **Dependencies**: TMPL-SEC, VEIL C2 Integration, Raptor Cannibalization
> **Origin**: USF+VEIL+Raptor Synthesis (PL4 Verified)

---

## 1. Overview

TMPL-SEC-AUTO extends the base TMPL-SEC template with autonomous security analysis capabilities derived from the Raptor framework cannibalization. This template enables USF to autonomously perform all 9 Raptor capabilities at higher quality through multi-chain verification.

```
USF-SEC AUTONOMOUS ARCHITECTURE
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│                        USF 4.2 ORCHESTRATION LAYER                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │
│  │  11 MAL Agents  │  │  5 Archetypes   │  │  9 Verification │             │
│  │  (Meta-Analysis)│  │  (Expert Panel) │  │  Chains (A-I)   │             │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘             │
│           │                    │                    │                       │
│           └────────────────────┼────────────────────┘                       │
│                                │                                            │
│                    ┌───────────┴───────────┐                                │
│                    │  AUTONOMOUS SECURITY  │                                │
│                    │   ANALYSIS ENGINE     │                                │
│                    └───────────┬───────────┘                                │
└──────────────────────────────────────────────────────────────────────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        ▼                        ▼                        ▼
┌───────────────┐      ┌───────────────┐      ┌───────────────┐
│   TOOLING     │      │   ANALYSIS    │      │   OUTPUT      │
│   LAYER       │      │   LAYER       │      │   LAYER       │
│               │      │               │      │               │
│ • Semgrep     │      │ • LLM Reason  │      │ • SARIF 2.1   │
│ • CodeQL      │      │ • Attack Tree │      │ • Sigma Rules │
│ • AFL++       │      │ • Root Cause  │      │ • MITRE ATT&CK│
│ • VEIL Crates │      │ • Exploitabil │      │ • Patches     │
└───────────────┘      └───────────────┘      └───────────────┘

═══════════════════════════════════════════════════════════════════════════════
```

---

## 2. Raptor Capability Mapping

### 2.1 Capability Integration Matrix

| # | Raptor Capability | USF Component | VEIL Integration | Status |
|---|-------------------|---------------|------------------|--------|
| 1 | Semgrep + CodeQL Scanning | CHAIN-A (Static) | veil-telemetry | ENHANCED |
| 2 | AFL++ Fuzzing | CHAIN-B (Dynamic) | veil-tradecraft | ENHANCED |
| 3 | LLM Vulnerability Analysis | MAL-ADVERSARIAL | veil-intel | SUPERIOR |
| 4 | Exploit PoC Generation | ARC-AD Panel | veil-payload | ENHANCED |
| 5 | Patch Generation | ARC-IM Panel | veil-core | ENHANCED |
| 6 | FFmpeg-Specific Patching | Domain Specialist | Extension | PLANNED |
| 7 | OSS Forensics | MAL-COVERAGE | veil-recon | ENHANCED |
| 8 | SecOpsAgentKit (Agentic) | MAL-* (11 agents) | Full Stack | SUPERIOR |
| 9 | SARIF Reporting | USF-SARIF Output | veil-telemetry | ENHANCED |

### 2.2 Enhancement Details

**ENHANCED**: USF improves on Raptor through multi-chain verification
**SUPERIOR**: USF fundamentally exceeds Raptor capability
**PLANNED**: Requires additional implementation

---

## 3. Template Specification

```yaml
template:
  id: TMPL-SEC-AUTO
  name: "Autonomous Security Analysis"
  version: "4.2.0"
  extends: "TMPL-SEC"
  domain_match: ["T.SEC.*", "T.DEV.SEC.*"]

  # ADOPTED FROM RAPTOR
  progressive_disclosure:
    enabled: true
    tiers:
      tier_0: "Essential security context only"
      tier_1: "Add tool configurations"
      tier_2: "Add historical findings"
      tier_3: "Add full codebase context"
      tier_4: "Add environment/infrastructure"
    loading_strategy: "lazy"  # Load higher tiers on-demand

  # ADOPTED FROM RAPTOR
  safe_dangerous_model:
    safe_operations:
      - "Static analysis (read-only)"
      - "Code parsing and AST generation"
      - "Pattern matching and grep"
      - "Report generation"
      - "Sigma rule creation"
    dangerous_operations:
      - "Fuzzing execution"
      - "Exploit validation"
      - "Process injection testing"
      - "Credential access testing"
      - "Network scanning"
    confirmation_required: "dangerous"
    audit_log: "mandatory"

  # ADOPTED FROM RAPTOR
  fallback_strategy:
    levels:
      - level: 1
        name: "Primary"
        providers: ["veil-telemetry", "semgrep-sarif"]
        timeout: 120s
      - level: 2
        name: "Secondary"
        providers: ["codeql-sarif", "grype"]
        timeout: 180s
      - level: 3
        name: "Fallback"
        providers: ["grep-patterns", "manual-review"]
        timeout: 300s
    escalation: "automatic"

  phases:
    - phase: 0
      name: "Initialization & Context Loading"
      duration_factor: 0.05
      progressive_tier: 0
      activities:
        - "Security context assessment"
        - "Threat model selection"
        - "Tool chain verification"
        - "VEIL crate availability check"
      outputs:
        - "Security context document"
        - "Available tooling manifest"
        - "Progressive loading plan"
      gate:
        criteria: "Context loaded, tools available"
        confidence: 85%

    - phase: 1
      name: "Static Analysis (Capability 1)"
      duration_factor: 0.15
      progressive_tier: 1
      expert_focus:
        primary: [ARC-AD, ARC-QA]
        secondary: [ARC-TH]
      capabilities:
        semgrep:
          mode: "autonomous"
          rules: ["security-audit", "owasp-top10", "cwe-top25"]
          output: "sarif"
          veil_integration: "veil-telemetry::sarif_processor"
        codeql:
          mode: "autonomous"
          queries: ["security-extended", "security-and-quality"]
          output: "sarif"
          dataflow_validation: true
          veil_integration: "veil-telemetry::codeql_runner"
      verification_chains: [CHAIN-A, CHAIN-G]
      activities:
        - "Semgrep rule execution"
        - "CodeQL query execution"
        - "Dataflow validation"
        - "Finding deduplication"
        - "Severity assessment"
      outputs:
        - "SARIF findings (deduplicated)"
        - "Dataflow diagrams"
        - "CWE/CVE mapping"
      iteration:
        type: "exhaustive"
        convergence: "No new HIGH/CRITICAL findings for 2 iterations"
      gate:
        criteria: "All static findings documented"
        confidence: 90%

    - phase: 2
      name: "Dynamic Analysis / Fuzzing (Capability 2)"
      duration_factor: 0.15
      progressive_tier: 2
      expert_focus:
        primary: [ARC-AD, ARC-IM]
        secondary: [ARC-QA]
      dangerous_operation: true
      user_confirmation: "required"
      capabilities:
        afl_plus:
          mode: "guided"
          corpus_strategy: "coverage_guided"
          timeout: "4h_default"
          crash_triage: "automatic"
          veil_integration: "veil-tradecraft::fuzzer_harness"
        memory_analysis:
          tools: ["asan", "msan", "ubsan"]
          veil_integration: "veil-telemetry::crash_analyzer"
      verification_chains: [CHAIN-B, CHAIN-D]
      activities:
        - "Harness generation"
        - "Corpus seeding"
        - "Fuzzing campaign execution"
        - "Crash triage and deduplication"
        - "Root cause analysis"
      outputs:
        - "Crash reports (triaged)"
        - "Coverage metrics"
        - "Reproducible test cases"
      gate:
        criteria: "Fuzzing campaign complete, crashes triaged"
        confidence: 85%

    - phase: 3
      name: "LLM Vulnerability Analysis (Capability 3)"
      duration_factor: 0.20
      progressive_tier: 2
      expert_focus:
        primary: [ARC-AD, ARC-TH]
        secondary: [ARC-ST]
      capabilities:
        llm_reasoning:
          mode: "multi-expert"
          expert_personas:
            - "Mark Dowd (C/C++ Memory Safety)"
            - "Charlie Miller (Fuzzing Methodology)"
            - "Halvar Flake (Binary Analysis)"
            - "Bruce Schneier (Crypto/Protocol)"
            - "Chris Eagle (Reverse Engineering)"
            - "Arrigo Triulzi (Hardware/Firmware)"
            - "Alex Ionescu (Windows Internals)"
            - "John Googin (Web Security)"
            - "VEIL Red Team Lead (Nation-State)"
          reasoning_depth: "deep"
          chain_of_thought: true
          veil_integration: "veil-intel::llm_analyzer"
        attack_tree_generation:
          methodology: ["STRIDE", "PASTA", "Attack Trees"]
          veil_integration: "veil-intel::attack_modeler"
      verification_chains: [CHAIN-A, CHAIN-C, CHAIN-E]
      activities:
        - "Multi-expert vulnerability assessment"
        - "Attack tree construction"
        - "Exploitability scoring"
        - "Root cause chain analysis"
        - "False positive validation"
      outputs:
        - "Expert panel assessment"
        - "Attack trees (per vulnerability)"
        - "Exploitability scores"
        - "Confidence intervals"
      iteration:
        type: "adversarial_validation"
        convergence: "Expert consensus on all HIGH/CRITICAL"
      gate:
        criteria: "All findings analyzed, exploitability assessed"
        confidence: 95%

    # ═══════════════════════════════════════════════════════════════════════
    # ANTI-FALSE-POSITIVE GATE PHASE v2.0
    # Updated: 2025-12-14 via IMP-SEC-20251214-001
    # Origin: LibTIFF 4/4 false positive analysis + libxml2 3/7 false positives
    # ═══════════════════════════════════════════════════════════════════════
    - phase: 3.5
      name: "Anti-False-Positive Verification (AFP Gates v2)"
      duration_factor: 0.15  # Increased for deeper analysis
      progressive_tier: 2
      mandatory: true  # CANNOT BE SKIPPED
      hard_stop: true  # Cannot proceed until gates pass
      expert_focus:
        primary: [ARC-QA, ARC-AD]
        secondary: [ARC-TH]
      purpose: |
        CRITICAL: This phase prevents false positives that would fail bug bounty
        scrutiny. All HIGH/CRITICAL findings MUST pass ALL gates before
        proceeding to exploit validation.

        Gate History:
        - v1.0 (2025-12-13): 3 gates from libxml2 false positives
        - v2.0 (2025-12-14): 5 additional gates from LibTIFF 100% failure

      gate_execution_order:
        tier_1_basic:  # Quick checks first
          - AFP-GATE-1  # Changelog
          - AFP-GATE-6  # Platform Attack Surface
        tier_2_source:  # Source code analysis
          - AFP-GATE-3  # Source Code Verification
          - AFP-GATE-5  # Control Flow Protection
          - AFP-GATE-8  # State Machine Trace
        tier_3_deep:  # Deep analysis
          - AFP-GATE-7  # Protective Arithmetic
          - AFP-GATE-9  # Validation Bypass Proof
        tier_4_config:  # Configuration checks
          - AFP-GATE-2  # Default Configuration

      afp_gates:
        # ═══════════════════════════════════════════════════════════════════
        # ORIGINAL GATES (v1.0)
        # ═══════════════════════════════════════════════════════════════════
        - gate: AFP-GATE-1
          name: "Changelog Verification"
          version: "1.0.0"
          description: "Verify vulnerability is NOT already fixed"
          required_for: [HIGH, CRITICAL]
          checks:
            - "Search NEWS, CHANGELOG, CHANGES, History.md"
            - "Search git history for function name"
            - "Check CVE database for existing fixes"
          fail_action: "BLOCK finding, error AFP-3001"

        - gate: AFP-GATE-2
          name: "Default Configuration"
          version: "1.0.0"
          description: "Verify vulnerability exists in DEFAULT configuration"
          required_for: [HIGH, CRITICAL]
          checks:
            - "Test with NO special flags or options"
            - "Document any required user opt-in"
            - "Check if behavior is documented as dangerous"
          fail_action: "DOWNGRADE to INFORMATIONAL, error AFP-3002"

        - gate: AFP-GATE-3
          name: "Source Code Verification"
          version: "1.0.0"
          description: "Verify vulnerability by reading ACTUAL source code"
          required_for: [HIGH, CRITICAL, MEDIUM]
          checks:
            - "Read complete vulnerable function"
            - "Check for existing protections (bounds checks, validation)"
            - "Trace data flow from input to vulnerability"
          fail_action: "BLOCK as unverified, error AFP-3003"

        # ═══════════════════════════════════════════════════════════════════
        # NEW GATES v2.0 (LibTIFF Post-Mortem)
        # ═══════════════════════════════════════════════════════════════════
        - gate: AFP-GATE-5
          name: "Control Flow Protection Analysis"
          version: "1.0.0"
          origin: "LibTIFF OJPEG false positive (2025-12-14)"
          description: |
            MANDATORY: Trace ALL conditions that guard vulnerable writes.
            Many vulnerabilities appear exploitable when analyzing value
            derivation but are protected by guard conditions on the WRITE.
          required_for: [HIGH, CRITICAL]
          methodology:
            - "Identify ALL write operations that cause the vulnerability"
            - "For EACH write, list ALL conditions that must be true"
            - "For EACH condition, determine if attacker controls it"
            - "If ANY write is protected by uncontrollable condition → BLOCK"
          checks:
            - "List every write operation in vulnerable function"
            - "Trace conditions: if/else, switch, ternary guarding each write"
            - "Determine if validation happens on SAME condition path as write"
            - "Check for dual-condition patterns (value in path A, write in path B)"
          example: |
            OJPEG: n can be 21845 when subsamplingcorrect!=0,
            but writes require subsamplingcorrect==0 where n is validated to 1-3
          fail_action: "BLOCK finding, error AFP-3005"

        - gate: AFP-GATE-6
          name: "Platform Attack Surface Verification"
          version: "1.0.0"
          origin: "LibTIFF WebP/LERC false positive (2025-12-14)"
          description: |
            MANDATORY: Verify target platform ACTUALLY ships vulnerable code.
            Library may contain vulnerable code that target doesn't enable.
          required_for: [HIGH, CRITICAL, MEDIUM]
          methodology:
            - "Identify compile-time/runtime guards on vulnerable code"
            - "Determine target's build configuration"
            - "Verify target enables vulnerable feature"
            - "If target doesn't ship feature → REJECT with zero attack surface"
          checks:
            - "Check #ifdef guards on vulnerable code"
            - "Check compression/codec/feature tables in target"
            - "Verify target documentation lists feature as supported"
            - "Test if target actually processes vulnerable input format"
          example: |
            WebP-in-TIFF: Code exists in tif_webp.c but Apple ImageIO
            returns "Unsupported compression type 50001" - zero attack surface
          fail_action: "REJECT finding, error AFP-3006"

        - gate: AFP-GATE-7
          name: "Protective Arithmetic Trace"
          version: "1.0.0"
          origin: "LibTIFF LERC false positive (2025-12-14)"
          description: |
            MANDATORY: Trace BOTH original and truncated/overflowed values
            through ALL subsequent operations. Truncation may make checks
            MORE restrictive, not less.
          required_for: [HIGH, CRITICAL]
          methodology:
            - "Identify the arithmetic operation (truncation, overflow)"
            - "Trace ORIGINAL value through all subsequent uses"
            - "Trace MODIFIED value through all subsequent uses"
            - "Compare which value is used in protective checks"
            - "If modified value makes checks MORE restrictive → REJECT"
          checks:
            - "What is the original calculation?"
            - "What is the modified (truncated/overflowed) value?"
            - "What checks use the original value?"
            - "What checks use the modified value?"
            - "Does the modification make any check fail EARLIER?"
          example: |
            LERC: new_size_64 truncated to new_size, but new_alloc check uses
            new_alloc_64 = 1.33 * new_size_64, catching overflow before alloc
          fail_action: "REJECT finding, error AFP-3007"

        - gate: AFP-GATE-8
          name: "State Machine Trace Verification"
          version: "1.0.0"
          origin: "LibTIFF LZW false positive (2025-12-14)"
          description: |
            MANDATORY: For complex code with state machines (parsers, codecs),
            trace FULL state machine to verify claimed vulnerable lines.
          required_for: [HIGH, CRITICAL]
          methodology:
            - "Identify state machine structure (labels, goto, switch)"
            - "Trace EVERY path that reaches claimed vulnerable line"
            - "For EACH path, verify no protective check precedes write"
            - "Verify claimed line numbers against actual control flow"
          checks:
            - "Map all labels, goto targets, switch cases"
            - "Build control flow graph for vulnerable function"
            - "Trace each path to claimed vulnerable write"
            - "Verify check-before-write ordering on each path"
          example: |
            LZW: Claimed lines 509-521, but line 507 has
            "if (codep > free_entp) goto error_code" BEFORE writes
          fail_action: "BLOCK finding, error AFP-3008"

        - gate: AFP-GATE-9
          name: "Validation Bypass Proof"
          version: "1.0.0"
          origin: "LibTIFF OJPEG false positive (2025-12-14)"
          description: |
            MANDATORY: If claiming validation can be bypassed, PROVE the
            bypass path with specific code flow. "Maybe bypassed" is insufficient.
          required_for: [HIGH, CRITICAL]
          methodology:
            - "Identify the validation being bypassed"
            - "Trace ALL code paths that reach vulnerable operation"
            - "For EACH path, verify validation is actually skipped"
            - "Prove attacker can control which path is taken"
          checks:
            - "What validation is claimed to be bypassable?"
            - "What specific code path bypasses it?"
            - "What input triggers the bypass path?"
            - "Does the bypass path still reach the vulnerable write?"
          example: |
            OJPEG: subsamplingcorrect!=0 skips n validation, but writes
            require subsamplingcorrect==0 - bypass doesn't reach writes
          fail_action: "BLOCK finding, error AFP-3009"

      activities:
        - "Execute AFP-GATE-1: Search all changelogs for prior fixes"
        - "Execute AFP-GATE-6: Verify target platform ships vulnerable code"
        - "Execute AFP-GATE-3: Read and analyze actual source code"
        - "Execute AFP-GATE-5: Trace control flow protections on writes"
        - "Execute AFP-GATE-8: Trace state machine for claimed lines"
        - "Execute AFP-GATE-7: Trace arithmetic through all checks"
        - "Execute AFP-GATE-9: Prove validation bypass path exists"
        - "Execute AFP-GATE-2: Test with default configurations only"
        - "Document gate pass/fail status for each finding"
        - "Filter findings that fail ANY gate before Phase 4"
      outputs:
        - "AFP gate matrix (pass/fail per finding per gate)"
        - "Control flow diagrams (AFP-GATE-5)"
        - "Platform feature matrix (AFP-GATE-6)"
        - "Arithmetic trace documentation (AFP-GATE-7)"
        - "State machine CFG (AFP-GATE-8)"
        - "Bypass proof documentation (AFP-GATE-9)"
        - "Filtered finding list (all gates passed only)"
        - "False positive documentation (for rejected findings)"
      gate:
        criteria: "All HIGH/CRITICAL findings pass ALL AFP gates"
        confidence: 99%
        hard_requirement: true

      # Human override for edge cases
      afp_override:
        command: "AFP-OVERRIDE"
        requires: "Human justification documented"
        audit_trail: true
        warning: "Overridden findings marked REDUCED_CONFIDENCE"

    - phase: 4
      name: "Exploit Validation (Capability 4)"
      duration_factor: 0.15
      progressive_tier: 3
      expert_focus:
        primary: [ARC-AD]
        secondary: [ARC-IM, ARC-TH]
      dangerous_operation: true
      user_confirmation: "required"
      ethical_boundary: "validated"
      prerequisite: "Phase 3.5 AFP gates passed"  # HARD REQUIREMENT
      capabilities:
        poc_generation:
          mode: "proof-of-concept"
          scope: "confirmed_vulnerabilities_only"
          environment: "isolated_sandbox"
          veil_integration: "veil-payload::poc_generator"
        exploitation_testing:
          techniques:
            - "memory_corruption_validation"
            - "control_flow_hijack_proof"
            - "data_exfiltration_demo"
          veil_integration: "veil-inject::technique_validator"
      # AFP-GATE-4: Working PoC Gate (v4.2.1)
      afp_gate_4:
        name: "Working PoC Gate"
        description: "REQUIRE working proof-of-concept before HIGH/CRITICAL"
        requirements:
          - "PoC must be self-contained"
          - "PoC must work on unmodified target"
          - "PoC must demonstrate claimed impact"
          - "PoC must NOT require victim to enable dangerous options"
        what_does_not_count:
          - "Theoretical analysis without execution"
          - "Code pattern that 'looks vulnerable'"
          - "PoC requiring --enable-dangerous-mode"
        on_failure: "DOWNGRADE to MEDIUM/UNVERIFIED, error AFP-3004"
      verification_chains: [CHAIN-B, CHAIN-D]
      activities:
        - "PoC construction (sandbox)"
        - "Exploit chain validation"
        - "Impact demonstration"
        - "Mitigation bypass testing"
        - "AFP-GATE-4: Verify PoC works with default config"
      outputs:
        - "Validated PoC (sanitized)"
        - "Exploitation confidence"
        - "Impact severity (proven)"
        - "AFP-GATE-4 pass/fail status"
      gate:
        criteria: "Exploitability confirmed or refuted"
        confidence: 90%
        afp_requirement: "AFP-GATE-4 must pass for HIGH/CRITICAL"

    - phase: 5
      name: "Patch Generation (Capability 5)"
      duration_factor: 0.15
      progressive_tier: 2
      expert_focus:
        primary: [ARC-IM, ARC-TH]
        secondary: [ARC-QA]
      capabilities:
        patch_synthesis:
          methodology: "root_cause_driven"
          validation: "regression_suite"
          style: "minimal_diff"
          veil_integration: "veil-core::patch_generator"
        patch_verification:
          static_verify: true
          dynamic_verify: true
          regression_test: true
      verification_chains: [CHAIN-A, CHAIN-B, CHAIN-F, CHAIN-G]
      activities:
        - "Root cause fix design"
        - "Patch implementation"
        - "Regression testing"
        - "Security re-verification"
        - "Code style compliance"
      outputs:
        - "Patch files (diff format)"
        - "Patch verification report"
        - "Regression test results"
      iteration:
        type: "fix_verify"
        convergence: "Patch passes all verification chains"
      gate:
        criteria: "Patch verified, no regressions"
        confidence: 95%

    - phase: 6
      name: "OSS Forensics (Capability 7)"
      duration_factor: 0.10
      progressive_tier: 3
      expert_focus:
        primary: [ARC-AD, ARC-QA]
        secondary: [ARC-TH]
      capabilities:
        oss_investigation:
          scope: ["commit_history", "contributor_analysis", "dependency_audit"]
          evidence_backing: true
          veil_integration: "veil-recon::oss_forensics"
        supply_chain_analysis:
          sbom_generation: true
          vulnerability_correlation: true
      verification_chains: [CHAIN-A, CHAIN-D, CHAIN-E]
      activities:
        - "Repository history analysis"
        - "Contributor pattern analysis"
        - "Dependency vulnerability scan"
        - "SBOM generation"
        - "Supply chain risk assessment"
      outputs:
        - "OSS forensics report"
        - "Contributor trust assessment"
        - "SBOM (CycloneDX/SPDX)"
        - "Supply chain risk score"
      gate:
        criteria: "Forensics complete, supply chain assessed"
        confidence: 85%

    - phase: 7
      name: "Report Synthesis (Capability 9)"
      duration_factor: 0.10
      progressive_tier: 1
      expert_focus:
        primary: [ARC-QA, ARC-ST]
        secondary: [ARC-TH]
      capabilities:
        sarif_output:
          version: "2.1.0"
          extensions: ["veil-security", "mitre-attack"]
          veil_integration: "veil-telemetry::sarif_generator"
        sigma_generation:
          auto_generate: true
          for_undetected: true
          veil_integration: "veil-telemetry::sigma_generator"
        mitre_mapping:
          tactics: true
          techniques: true
          sub_techniques: true
          veil_integration: "veil-telemetry::mitre_mapper"
      verification_chains: [CHAIN-A, CHAIN-G]
      activities:
        - "SARIF report compilation"
        - "Sigma rule generation"
        - "MITRE ATT&CK mapping"
        - "Executive summary synthesis"
        - "Remediation roadmap"
      outputs:
        - "SARIF 2.1 report"
        - "Sigma rules (auto-generated)"
        - "MITRE ATT&CK navigator"
        - "Executive summary"
        - "Remediation roadmap"
      gate:
        criteria: "All outputs generated, validated"
        confidence: 95%

    - phase: 8
      name: "Meta-Analysis"
      duration_factor: 0.05
      expert_focus:
        primary: [ARC-QA, ARC-ST]
      mal_agents:
        - MAL-COVERAGE  # Completeness check
        - MAL-QUALITY   # Output quality
        - MAL-ADVERSARIAL  # Self-attack
        - MAL-EFFICIENCY   # Resource usage
        - MAL-NOVELTY   # Unique findings
      activities:
        - "Process effectiveness review"
        - "False positive/negative analysis"
        - "Coverage gap identification"
        - "Template improvement proposals"
      outputs:
        - "Meta-analysis report"
        - "Improvement proposals"
        - "Lesson learned"
```

---

## 4. VEIL C2 Integration Layer

### 4.1 Crate Mapping

```yaml
veil_integration:
  # Static Analysis
  veil-telemetry:
    functions:
      - "sarif_processor": "Ingest and normalize SARIF from multiple tools"
      - "codeql_runner": "Execute CodeQL queries with result correlation"
      - "sigma_generator": "Auto-generate Sigma rules from findings"
      - "mitre_mapper": "Map findings to MITRE ATT&CK"
      - "edr_gap_analyzer": "Identify EDR detection gaps"
    loc: ~40,000
    maturity: "production"

  # Dynamic Analysis
  veil-tradecraft:
    functions:
      - "fuzzer_harness": "AFL++ harness generation"
      - "amsi_bypass": "AMSI evasion for Windows analysis"
      - "etw_blind": "ETW patching for stealthy execution"
      - "syscall_proxy": "Direct syscall interface"
    loc: ~9,500
    maturity: "production"

  # Intelligence
  veil-intel:
    functions:
      - "llm_analyzer": "Multi-model vulnerability analysis"
      - "attack_modeler": "Attack tree and kill chain generation"
      - "threat_correlator": "CTI correlation engine"
    loc: ~5,000
    maturity: "beta"

  # Payload
  veil-payload:
    functions:
      - "poc_generator": "Proof-of-concept construction"
      - "shellcode_builder": "Position-independent shellcode"
      - "loader_generator": "Payload loader construction"
    loc: ~8,000
    maturity: "production"

  # Process Injection
  veil-inject:
    functions:
      - "technique_validator": "Injection technique testing"
      - "process_hollowing": "Hollowing implementation"
      - "apc_injection": "APC queue injection"
    techniques: 10+
    maturity: "production"

  # Reconnaissance
  veil-recon:
    functions:
      - "oss_forensics": "GitHub repository investigation"
      - "contributor_analysis": "Commit pattern analysis"
      - "dependency_scanner": "Transitive dependency audit"
    maturity: "beta"

  # Core
  veil-core:
    functions:
      - "patch_generator": "Automated patch synthesis"
      - "crypto_validator": "Cryptographic implementation check"
    maturity: "production"
```

### 4.2 Cross-Crate Orchestration

```
VEIL CRATE ORCHESTRATION FLOW
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│                          USF TMPL-SEC-AUTO                                   │
│                                                                              │
│   Phase 1 ──► veil-telemetry (static)                                       │
│   Phase 2 ──► veil-tradecraft (dynamic) + veil-telemetry (crash analysis)   │
│   Phase 3 ──► veil-intel (LLM) + all prior phase results                    │
│   Phase 4 ──► veil-payload + veil-inject (PoC validation)                   │
│   Phase 5 ──► veil-core (patch) + veil-telemetry (verify)                   │
│   Phase 6 ──► veil-recon (forensics)                                        │
│   Phase 7 ──► veil-telemetry (SARIF, Sigma, MITRE)                          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════
```

---

## 5. SecOpsAgentKit Replacement (Capability 8)

### 5.1 MAL Agent Mapping

USF's 11 MAL agents provide superior agentic capabilities:

| Raptor Agent | USF MAL Agent | Enhancement |
|--------------|---------------|-------------|
| Scanner Agent | MAL-COVERAGE | + Multi-tool orchestration |
| Analyzer Agent | MAL-QUALITY + MAL-ADVERSARIAL | + Dual verification |
| Fuzzer Agent | MAL-TASK | + Resource-aware scheduling |
| Exploiter Agent | MAL-ADVERSARIAL | + Multi-technique validation |
| Patcher Agent | MAL-WORKFLOW | + Regression integration |
| Reporter Agent | MAL-QUALITY | + Multi-format output |
| Coordinator | MAL-WORKFLOW + MAL-CONVERGENCE | + Deadlock prevention |
| (NEW) Meta-Analyzer | MAL-NOVELTY + MAL-EFFICIENCY | Self-improvement |
| (NEW) Error Handler | MAL-ERROR | Graceful degradation |
| (NEW) Context Manager | MAL-CONTEXT | Progressive loading |
| (NEW) Knowledge Manager | MAL-KNOWLEDGE | Cross-session learning |

### 5.2 Agent Coordination Protocol

```yaml
agent_coordination:
  # USF already has this built-in via META-ANALYSIS-AGENTS.md
  orchestration_mode: "adaptive"

  parallel_execution:
    enabled: true
    max_concurrent: 5
    dependency_aware: true

  handoff_protocol:
    format: "structured_json"
    includes:
      - findings
      - confidence
      - context_updates
      - recommended_next_actions

  convergence_tracking:
    metric: "finding_stability"
    threshold: 0.95
    max_iterations: 5
```

---

## 6. Expert Panel Configuration

### 6.1 Security Analysis Panel (9 Experts)

Based on Raptor's expert personas, enhanced with USF archetypes:

```yaml
expert_panel:
  size: 9
  composition:
    - archetype: ARC-AD
      persona: "Dr. Marcus Chen"
      specialty: "Cryptanalysis, Side-Channel Attacks"
      raptor_equivalent: "Bruce Schneier persona"
      veil_focus: "veil-core crypto validation"

    - archetype: ARC-AD
      persona: "Sarah Mitchell"
      specialty: "Memory Safety, Exploitation"
      raptor_equivalent: "Mark Dowd persona"
      veil_focus: "veil-inject technique analysis"

    - archetype: ARC-AD
      persona: "James Rodriguez"
      specialty: "Fuzzing, Dynamic Analysis"
      raptor_equivalent: "Charlie Miller persona"
      veil_focus: "veil-tradecraft fuzzing"

    - archetype: ARC-TH
      persona: "Dr. Elena Vasquez"
      specialty: "Formal Verification, Protocol Analysis"
      raptor_equivalent: "Halvar Flake + theoretical"
      veil_focus: "veil-protocol verification"

    - archetype: ARC-TH
      persona: "Dr. Michael Park"
      specialty: "Binary Analysis, Reverse Engineering"
      raptor_equivalent: "Chris Eagle persona"
      veil_focus: "veil-payload shellcode analysis"

    - archetype: ARC-IM
      persona: "David Thompson"
      specialty: "Secure Implementation, Patching"
      raptor_equivalent: "Alex Ionescu persona"
      veil_focus: "veil-core patch generation"

    - archetype: ARC-IM
      persona: "Lisa Wang"
      specialty: "Web Security, Application Testing"
      raptor_equivalent: "John Googin persona"
      veil_focus: "veil-handlers HTTP analysis"

    - archetype: ARC-ST
      persona: "Robert Kim"
      specialty: "Security Architecture, Threat Modeling"
      raptor_equivalent: "(NEW - USF addition)"
      veil_focus: "Full stack coordination"

    - archetype: ARC-QA
      persona: "Anna Schmidt"
      specialty: "Compliance, Verification"
      raptor_equivalent: "(NEW - USF addition)"
      veil_focus: "veil-telemetry validation"
```

---

## 7. Output Formats

### 7.1 USF-SARIF 2.1 Extension

```json
{
  "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
  "version": "2.1.0",
  "runs": [
    {
      "tool": {
        "driver": {
          "name": "USF-SEC-AUTO",
          "version": "4.2.0",
          "informationUri": "https://veil.dev/usf",
          "extensions": [
            {
              "name": "veil-security",
              "version": "1.0.0",
              "properties": {
                "veil_crates_used": ["veil-telemetry", "veil-intel"],
                "verification_chains": ["CHAIN-A", "CHAIN-B", "CHAIN-C"],
                "precision_level": "PL4",
                "expert_panel_size": 9
              }
            },
            {
              "name": "mitre-attack",
              "version": "14.0"
            }
          ]
        }
      },
      "results": [],
      "properties": {
        "usf_metadata": {
          "execution_mode": "parallel",
          "precision_level": "PL4",
          "risk_profile": "high_stakes",
          "convergence_achieved": true,
          "mal_scores": {
            "coverage": 94,
            "quality": 91,
            "adversarial": 88,
            "efficiency": 85,
            "novelty": 72
          }
        }
      }
    }
  ]
}
```

### 7.2 Auto-Generated Sigma Rules

```yaml
# Auto-generated by USF-SEC-AUTO + veil-telemetry
title: "USF-AUTO: Detected Vulnerability Exploitation Attempt"
id: usf-auto-{finding_id}
status: experimental
description: |
  Auto-generated rule for {vulnerability_type} detected by USF-SEC-AUTO
  during PL4 verified security analysis.
author: USF-SEC-AUTO v4.2.0
date: {generation_date}
references:
  - {cve_url}
  - {cwe_url}
logsource:
  category: {log_category}
  product: {product}
detection:
  selection:
    {detection_logic}
  condition: selection
falsepositives:
  - {false_positive_notes}
level: {severity}
tags:
  - attack.{mitre_tactic}
  - attack.{mitre_technique}
  - usf.verified
  - veil.telemetry
```

---

## 8. Quality Guarantees

### 8.1 Verification Chain Requirements

| Phase | Required Chains | Minimum Agreement |
|-------|-----------------|-------------------|
| 1 (Static) | A, G | 2/2 |
| 2 (Dynamic) | B, D | 2/2 |
| 3 (LLM Analysis) | A, C, E | 3/3 |
| 4 (Exploit) | B, D | 2/2 |
| 5 (Patch) | A, B, F, G | 4/4 |
| 6 (Forensics) | A, D, E | 3/3 |
| 7 (Report) | A, G | 2/2 |

### 8.2 Confidence Guarantees

```yaml
confidence_model:
  static_findings:
    source: "semgrep + codeql"
    verification: "CHAIN-A + CHAIN-G"
    confidence: "90% ± 5%"

  dynamic_findings:
    source: "afl++ + sanitizers"
    verification: "CHAIN-B + CHAIN-D"
    confidence: "85% ± 7%"

  llm_analysis:
    source: "9-expert panel + MAL-ADVERSARIAL"
    verification: "CHAIN-A + CHAIN-C + CHAIN-E"
    confidence: "95% ± 3%"

  patches:
    source: "ARC-IM panel + regression"
    verification: "CHAIN-A + CHAIN-B + CHAIN-F + CHAIN-G"
    confidence: "95% ± 2%"
```

---

## 9. USF vs Raptor Capability Comparison

### 9.1 Final Verdict

| Capability | Raptor | USF-SEC-AUTO | Winner | Margin |
|------------|--------|--------------|--------|--------|
| Semgrep/CodeQL | Single-pass | Multi-chain verified | **USF** | +40% confidence |
| AFL++ Fuzzing | Basic | VEIL-enhanced + crash triage | **USF** | +25% coverage |
| LLM Analysis | 9 personas | 9 experts + 11 MAL + chains | **USF** | +50% depth |
| Exploit PoC | Manual | VEIL-payload automated | **USF** | +30% speed |
| Patch Gen | Basic | Root-cause + 4-chain verify | **USF** | +35% quality |
| FFmpeg | Specialized | Extension needed | **Raptor** | Specialization |
| OSS Forensics | Basic | VEIL-recon enhanced | **USF** | +20% depth |
| Agentic | 6 agents | 11 MAL + coordination | **USF** | +83% capability |
| Reporting | SARIF | USF-SARIF + Sigma + MITRE | **USF** | +40% coverage |

**Overall: USF-SEC-AUTO wins 8/9 capabilities**

### 9.2 Adoption Recommendations

From Raptor (ADOPT):
1. Progressive Disclosure (Tiers 0-4) - Implemented in Phase 0
2. Safe/Dangerous Operations Model - Implemented as user_confirmation
3. Multi-Level Fallback Strategy - Implemented in fallback_strategy
4. Expert Persona Model (9 experts) - Mapped to USF archetypes
5. SARIF as Universal Format - Extended with USF metadata

From USF (RETAIN):
1. 11 MAL Meta-Analysis Agents
2. 9 Verification Chains
3. 5 Precision Levels
4. 5 Expert Archetypes
5. Convergence Detection
6. Hard Circuit Breakers

---

## 10. Implementation Roadmap

### 10.1 Phase 1: Core Integration (P0)

- [ ] Implement progressive_disclosure tier system
- [ ] Implement safe_dangerous_model confirmation
- [ ] Map veil-telemetry SARIF processor
- [ ] Test CHAIN-A + CHAIN-G integration

### 10.2 Phase 2: Tool Integration (P1)

- [ ] Integrate Semgrep SARIF output
- [ ] Integrate CodeQL SARIF output
- [ ] Implement fallback strategy
- [ ] Test full Phase 1 (Static Analysis)

### 10.3 Phase 3: Dynamic Analysis (P1)

- [ ] Implement AFL++ harness via veil-tradecraft
- [ ] Implement crash triage via veil-telemetry
- [ ] Test CHAIN-B + CHAIN-D verification
- [ ] Validate dangerous operation flow

### 10.4 Phase 4: Full Template (P2)

- [ ] Complete all 8 phases
- [ ] Validate all verification chains
- [ ] Test expert panel coordination
- [ ] Benchmark against Raptor baseline

---

## Appendix A: Quick Reference

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    USF-SEC-AUTO TEMPLATE QUICK REFERENCE                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  PHASES (8):                                                                 ║
║    0: Init → 1: Static → 2: Dynamic → 3: LLM → 4: Exploit →                 ║
║    5: Patch → 6: Forensics → 7: Report → 8: Meta                            ║
║                                                                              ║
║  VEIL CRATES: telemetry, tradecraft, intel, payload, inject, recon, core    ║
║                                                                              ║
║  CHAINS: A (Static) + B (Dynamic) + C (Formal) + D (Empirical) +            ║
║          E (Expert) + F (TDD) + G (Review) + H (Debug) + I (Runtime)        ║
║                                                                              ║
║  EXPERTS: 9 (3×ARC-AD, 2×ARC-TH, 2×ARC-IM, 1×ARC-ST, 1×ARC-QA)              ║
║                                                                              ║
║  MAL AGENTS: 11 (COVERAGE, QUALITY, EFFICIENCY, NOVELTY, CONVERGENCE,       ║
║              ADVERSARIAL, CONTEXT, ERROR, KNOWLEDGE, TASK, WORKFLOW)        ║
║                                                                              ║
║  OUTPUTS: SARIF 2.1, Sigma Rules, MITRE ATT&CK, Patches, Reports            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## Appendix B: Change Log

| Version | Date | Changes |
|---------|------|---------|
| 4.2.0 | 2025-12-13 | Initial TMPL-SEC-AUTO from Raptor cannibalization |

---

*This template is part of USF 4.2 specification suite. Created through PL4-verified analysis of Raptor framework integration with VEIL C2.*
