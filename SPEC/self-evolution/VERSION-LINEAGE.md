# USF 4.0: Version Lineage

> **Version**: 4.0.0
> **Component**: Self-Evolution / Version Lineage
> **Status**: Specification
> **Dependencies**: IMPROVEMENT-PROTOCOL.md, MASTER-SPECIFICATION.md

---

## 1. Overview

Version Lineage provides complete traceability of USF evolution, enabling rollback, audit, and understanding of how the system has changed over time. Every improvement creates a new version in the lineage, forming an immutable history of USF's self-evolution.

```
VERSION LINEAGE STRUCTURE
═══════════════════════════════════════════════════════════════════════════════

                          USF 4.0.0 (Genesis)
                                 │
                                 │ IMP-TAX-001: Add domain X
                                 ▼
                          USF 4.0.1
                                 │
                                 │ IMP-TEM-002: Optimize phase Y
                                 ▼
                          USF 4.0.2
                           /         \
        IMP-ARC-003     /             \  IMP-PRE-004
        (rolled back)  /               \
                      ▼                 ▼
               USF 4.0.3-rb       USF 4.0.3
                    │                   │
                    │                   │ IMP-VER-005
                    │                   ▼
                    │             USF 4.0.4
                    │                   │
                    └───────────────────┘
                                 │
                          (lineage merges)
                                 │
                                 ▼
                          USF 4.0.5

═══════════════════════════════════════════════════════════════════════════════
```

---

## 2. Version Identification

### 2.1 Version Number Schema

```yaml
version_schema:
  format: "MAJOR.MINOR.PATCH[-SUFFIX]"

  components:
    MAJOR:
      description: "Fundamental architecture changes"
      increment_trigger:
        - "Core execution model changes"
        - "Incompatible API changes"
        - "New self-evolution capabilities"
      current: 4

    MINOR:
      description: "Significant feature additions"
      increment_trigger:
        - "New domain categories"
        - "New phase templates"
        - "New archetypes"
      resets_on: "MAJOR increment"

    PATCH:
      description: "Individual improvements"
      increment_trigger:
        - "Any approved improvement"
        - "Bug fixes"
        - "Parameter tuning"
      resets_on: "MINOR increment"

  suffixes:
    -rb: "Rolled-back version"
    -dev: "Development/testing version"
    -rc{N}: "Release candidate"

  examples:
    - "4.0.0": "Initial USF 4.0 release"
    - "4.0.15": "15 improvements since 4.0.0"
    - "4.1.0": "First minor release with new features"
    - "4.0.15-rb": "Version 4.0.15 was rolled back"
```

### 2.2 Version Identifier Structure

```yaml
version_identifier:
  full_id: "USF-{VERSION}-{TIMESTAMP}-{HASH}"

  components:
    VERSION: "MAJOR.MINOR.PATCH format"
    TIMESTAMP: "YYYYMMDDHHmmss UTC"
    HASH: "SHA-256 of version content (first 8 chars)"

  example: "USF-4.0.15-20240115143022-a3f7b2c1"

  uniqueness_guarantee:
    primary: "VERSION + TIMESTAMP is globally unique"
    secondary: "HASH provides content verification"
```

---

## 3. Version Record Structure

### 3.1 Complete Version Record

```yaml
version_record:
  # Identification
  version_id: "Full version identifier"
  version_number: "MAJOR.MINOR.PATCH"
  created_at: "ISO8601 timestamp"
  created_by: "improvement_id or 'manual'"

  # Lineage
  parent_version: "Previous version identifier"
  child_versions: ["List of derived versions"]
  lineage_depth: "Distance from genesis"

  # Content
  content_hash: "SHA-256 of all specifications"
  specification_hashes:
    MASTER-SPECIFICATION: "SHA-256"
    core/DOMAIN-TAXONOMY: "SHA-256"
    core/EXPERT-ARCHETYPES: "SHA-256"
    # ... all specifications

  # Improvement Details (if applicable)
  improvement:
    improvement_id: "IMP-* identifier"
    category: "Improvement category"
    risk_level: "LOW|MEDIUM|HIGH|CRITICAL"
    description: "Brief description"
    diff: "Structured difference from parent"
    validation_results:
      external_anchor_score: 0.85
      regression_test_pass_rate: 1.0
      ab_test_results:
        quality_delta: 0.07
        p_value: 0.02
        effect_size: 0.15

  # Status
  status: "ACTIVE|ROLLED_BACK|SUPERSEDED|ARCHIVED"
  rollback_info:  # If status == ROLLED_BACK
    rolled_back_at: "Timestamp"
    reason: "Rollback reason"
    rolled_back_to: "Target version"

  # Metrics (post-deployment)
  deployment_metrics:
    tasks_executed: 1250
    average_quality_score: 0.87
    failure_rate: 0.02
    observation_period: "7 days"

  # Audit
  audit_log:
    - timestamp: "Event time"
      event: "Event type"
      actor: "Who/what triggered"
      details: "Event details"
```

### 3.2 Differential Storage

```yaml
differential_storage:
  approach: "Store diffs from parent, reconstruct on demand"

  diff_structure:
    specification: "Path to modified specification"
    modification_type: "ADD|MODIFY|REMOVE"
    hunks:
      - start_line: 100
        end_line: 110
        old_content: "Previous content"
        new_content: "New content"

  reconstruction:
    method: "Apply diffs in lineage order from nearest snapshot"
    snapshots: "Full copies at every 10th version"
    verification: "Hash check after reconstruction"

  storage_efficiency:
    typical_diff_size: "< 1% of full specification"
    snapshot_frequency: "Every 10 versions"
    total_overhead: "~10% vs storing full copies"
```

---

## 4. Lineage Operations

### 4.1 Version Creation

```
VERSION CREATION PROTOCOL
═══════════════════════════════════════════════════════════════════════════════

TRIGGER: Approved improvement ready for integration

Step 1: Pre-Creation Validation
  • Verify improvement approval status
  • Check no conflicting pending versions
  • Validate parent version is current ACTIVE version

Step 2: Prepare Version Record
  • Generate version number (increment PATCH)
  • Generate full version identifier
  • Calculate content hashes
  • Create diff from parent

Step 3: Atomic Creation
  • BEGIN TRANSACTION
  • Create version record
  • Update parent's child_versions
  • Mark new version as ACTIVE
  • Mark parent as SUPERSEDED
  • COMMIT TRANSACTION

Step 4: Post-Creation
  • Notify dependent systems
  • Begin monitoring period
  • Update lineage index

═══════════════════════════════════════════════════════════════════════════════
```

### 4.2 Version Query

```yaml
query_operations:
  get_current:
    description: "Get current active version"
    query: "SELECT * FROM versions WHERE status = 'ACTIVE'"
    cache: "Always cached, invalidated on new version"

  get_version:
    description: "Get specific version by identifier"
    query: "SELECT * FROM versions WHERE version_id = ?"
    cache: "LRU cache with TTL"

  get_lineage:
    description: "Get full lineage from genesis to version"
    query: "Recursive parent traversal"
    result: "Ordered list of versions"

  get_diff:
    description: "Get difference between two versions"
    query: "Reconstruct both, compute diff"
    optimization: "Use stored diffs if adjacent"

  search_versions:
    description: "Find versions matching criteria"
    criteria:
      - improvement_category
      - date_range
      - status
      - specification_modified
```

### 4.3 Rollback Operations

```
ROLLBACK EXECUTION
═══════════════════════════════════════════════════════════════════════════════

TRIGGER: Rollback decision from Improvement Protocol

Step 1: Identify Target
  • Current version: V_current
  • Target version: V_target (usually V_current.parent)

Step 2: Validate Rollback
  • Verify V_target exists and is valid
  • Verify V_target can be reconstructed
  • Check no circular rollback situation

Step 3: Execute Rollback
  • BEGIN TRANSACTION
  • Mark V_current as ROLLED_BACK
  • Record rollback reason and timestamp
  • Create new version V_new as child of V_target
  • Copy V_target content to V_new (with rollback marker)
  • Mark V_new as ACTIVE
  • COMMIT TRANSACTION

Step 4: Post-Rollback
  • Notify dependent systems
  • Clear caches
  • Trigger investigation workflow
  • Update monitoring

ROLLBACK VERSIONING:
  • Rollback creates new version (doesn't modify history)
  • Rolled-back version marked but preserved
  • Full audit trail maintained

═══════════════════════════════════════════════════════════════════════════════
```

### 4.4 Branch and Merge

```yaml
branching:
  purpose: "Parallel development and A/B testing"

  branch_creation:
    trigger: "Parallel improvement testing needed"
    process:
      - "Create branch point marker"
      - "Assign branch identifier"
      - "Allow independent versioning on branch"

  branch_identifier:
    format: "{parent_version}.branch.{branch_name}"
    example: "4.0.15.branch.experimental-precision"

  merge_operation:
    trigger: "Branch improvement validated, ready for main"
    process:
      - "Verify branch improvement passes validation"
      - "Check for conflicts with main line"
      - "Apply branch changes to current main version"
      - "Create merge commit with both parents"
      - "Archive branch"

  conflict_resolution:
    automatic: "Non-overlapping changes"
    manual: "Overlapping changes require human decision"
```

---

## 5. Lineage Analysis

### 5.1 Evolution Metrics

```yaml
evolution_metrics:
  velocity:
    improvements_per_week:
      calculation: "Count of new versions per week"
      healthy_range: [2, 10]

    improvement_acceptance_rate:
      calculation: "Accepted / (Accepted + Rejected)"
      healthy_range: [0.3, 0.7]

    rollback_rate:
      calculation: "Rolled-back / Total applied"
      healthy_range: [0, 0.1]

  quality_trajectory:
    quality_over_time:
      calculation: "Plot average_quality_score vs version"
      expectation: "Monotonically increasing (with noise)"

    stability_score:
      calculation: "1 - (rollbacks / improvements)"
      healthy_range: [0.9, 1.0]

  coverage_expansion:
    domain_coverage_growth:
      calculation: "New domains added over time"
      tracking: "Per major/minor version"

    template_coverage_growth:
      calculation: "New templates added over time"
      tracking: "Per major/minor version"
```

### 5.2 Lineage Visualization

```
LINEAGE VISUALIZATION FORMATS
═══════════════════════════════════════════════════════════════════════════════

LINEAR VIEW (main line only):
  4.0.0 ─► 4.0.1 ─► 4.0.2 ─► 4.0.3 ─► 4.0.4 ─► 4.0.5 (current)

TREE VIEW (with branches):
  4.0.0
    │
    ├── 4.0.1
    │     │
    │     ├── 4.0.2
    │     │     │
    │     │     ├── 4.0.3
    │     │     │     │
    │     │     │     └── 4.0.4 (current)
    │     │     │
    │     │     └── 4.0.3.branch.exp
    │     │           │
    │     │           └── (merged into 4.0.4)
    │     │
    │     └── 4.0.2-rb (rolled back)
    │
    └── 4.0.1.branch.hotfix
          │
          └── (merged into 4.0.2)

TIMELINE VIEW:
  ────────────────────────────────────────────────────────────►
  │        │        │        │        │        │
  4.0.0    4.0.1    4.0.2    4.0.3    4.0.4    now
  Jan 1    Jan 3    Jan 7    Jan 12   Jan 15

CATEGORY VIEW (grouped by improvement type):
  TAXONOMY:    [4.0.1, 4.0.5, 4.0.12]
  TEMPLATE:    [4.0.2, 4.0.7, 4.0.9]
  ARCHETYPE:   [4.0.3, 4.0.8]
  PRECISION:   [4.0.4, 4.0.11]
  PROCESS:     [4.0.6, 4.0.10]

═══════════════════════════════════════════════════════════════════════════════
```

### 5.3 Impact Analysis

```yaml
impact_analysis:
  forward_impact:
    description: "What was affected by this version?"
    analysis:
      - "Tasks executed under this version"
      - "Quality metrics during active period"
      - "Dependent versions"

  backward_impact:
    description: "What influenced this version?"
    analysis:
      - "Parent version chain"
      - "Improvement that created it"
      - "Meta-analysis findings that triggered improvement"

  change_propagation:
    description: "How did changes spread?"
    analysis:
      - "Which components were modified"
      - "Which dependent components were affected"
      - "Cross-specification impact"
```

---

## 6. Audit and Compliance

### 6.1 Audit Trail

```yaml
audit_trail:
  events_tracked:
    version_created:
      fields: [version_id, timestamp, improvement_id, creator]

    version_activated:
      fields: [version_id, timestamp, previous_active]

    version_rolled_back:
      fields: [version_id, timestamp, reason, target_version, actor]

    version_accessed:
      fields: [version_id, timestamp, accessor, purpose]

    lineage_queried:
      fields: [query_params, timestamp, requester, result_count]

    specification_reconstructed:
      fields: [version_id, specification, timestamp, requestor]

  retention:
    audit_logs: "Indefinite (compressed after 1 year)"
    version_records: "Indefinite"
    full_specifications: "Snapshots indefinite, diffs indefinite"

  access_control:
    read_audit: "Admin role required"
    export_audit: "Compliance role required"
    delete_audit: "Not permitted (immutable)"
```

### 6.2 Compliance Reports

```yaml
compliance_reports:
  evolution_report:
    description: "Summary of USF evolution over period"
    contents:
      - "Versions created"
      - "Improvements by category"
      - "Rollback events"
      - "Quality trajectory"
    frequency: "Monthly, on-demand"

  change_log:
    description: "Detailed log of all changes"
    contents:
      - "Per-version change description"
      - "Diff summaries"
      - "Approval records"
    frequency: "Per version, aggregated monthly"

  audit_summary:
    description: "Audit event summary"
    contents:
      - "Access patterns"
      - "Modification events"
      - "Anomaly detection"
    frequency: "Weekly, on-demand"
```

---

## 7. Storage and Retrieval

### 7.1 Storage Architecture

```yaml
storage_architecture:
  primary_store:
    type: "Immutable append-only log"
    implementation: "Content-addressed storage"
    redundancy: "3x replication"

  index:
    type: "B-tree index"
    keys:
      - version_id
      - version_number
      - created_at
      - status
      - improvement_category

  cache:
    current_version:
      strategy: "Always in memory"
      invalidation: "On new version creation"

    recent_versions:
      strategy: "LRU cache"
      size: "Last 100 versions"
      ttl: "1 hour"

    reconstructed_specs:
      strategy: "On-demand with TTL"
      ttl: "15 minutes"
```

### 7.2 Retrieval Optimization

```yaml
retrieval_optimization:
  snapshot_strategy:
    frequency: "Every 10 versions"
    storage: "Full specification copy"
    purpose: "Fast reconstruction"

  reconstruction_algorithm:
    1. "Find nearest snapshot ≤ target version"
    2. "Collect diffs from snapshot to target"
    3. "Apply diffs in order"
    4. "Verify hash"
    5. "Cache result"

  prefetching:
    trigger: "Access to version N"
    action: "Prefetch N-1, N+1 diffs"
    purpose: "Anticipate lineage browsing"
```

---

## 8. Recovery Procedures

### 8.1 Corruption Recovery

```yaml
corruption_recovery:
  detection:
    method: "Hash verification on access"
    frequency: "Every read operation"
    alert: "Immediate on mismatch"

  recovery_procedures:
    single_version_corruption:
      1. "Identify corrupted version"
      2. "Attempt reconstruction from parent + diff"
      3. "If diff corrupted, reconstruct from children"
      4. "If unrecoverable, mark version as CORRUPTED"
      5. "Alert administrators"

    multiple_version_corruption:
      1. "Identify corruption extent"
      2. "Find last known good snapshot"
      3. "Rebuild from snapshot"
      4. "Mark unrecoverable versions"
      5. "Full system audit"

  prevention:
    checksums: "SHA-256 on all content"
    redundancy: "3x replication across storage"
    backups: "Daily offsite backup"
```

### 8.2 Disaster Recovery

```yaml
disaster_recovery:
  rpo: "1 hour (Recovery Point Objective)"
  rto: "4 hours (Recovery Time Objective)"

  backup_strategy:
    continuous: "Real-time replication to secondary"
    periodic: "Hourly snapshots to tertiary"
    offsite: "Daily full backup offsite"

  recovery_procedure:
    1. "Assess damage extent"
    2. "Identify most recent valid backup"
    3. "Restore from backup"
    4. "Replay transaction log (if available)"
    5. "Verify integrity"
    6. "Resume operations"
```

---

## 9. Integration Points

### 9.1 Improvement Protocol Integration

```yaml
improvement_protocol:
  on_improvement_approved:
    action: "Create new version record"
    data: "Improvement details, validation results"

  on_rollback_triggered:
    action: "Execute rollback procedure"
    data: "Rollback reason, target version"

  version_query:
    purpose: "Get current version for improvement comparison"
```

### 9.2 Operational Layer Integration

```yaml
operational_layer:
  get_current_specifications:
    purpose: "Load active USF configuration"
    response: "Reconstructed specifications for current version"

  version_stamping:
    purpose: "Tag task outputs with USF version"
    data: "version_id included in all outputs"

  metrics_reporting:
    purpose: "Report deployment metrics"
    data: "Quality scores, failure rates per version"
```

---

## 10. Version Lineage Policies

### 10.1 Retention Policies

```yaml
retention_policies:
  version_records:
    active: "Indefinite"
    rolled_back: "Indefinite (for audit)"
    superseded: "Indefinite (for lineage)"

  diffs:
    all_versions: "Indefinite"
    compressed_after: "30 days"

  snapshots:
    frequency: "Every 10 versions"
    retention: "Indefinite"

  metrics:
    detailed: "90 days"
    aggregated: "Indefinite"

  audit_logs:
    retention: "7 years (compliance)"
    archival: "After 1 year"
```

### 10.2 Cleanup Policies

```yaml
cleanup_policies:
  abandoned_branches:
    definition: "Branch with no activity for 30 days"
    action: "Archive and remove from active index"

  failed_improvements:
    definition: "Improvements rejected before version creation"
    action: "Archive after 30 days"

  temporary_versions:
    definition: "Versions created for testing (-dev suffix)"
    action: "Delete after 7 days unless promoted"
```

---

## Appendix A: Version Lineage Quick Reference

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    USF 4.0 VERSION LINEAGE REFERENCE                         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  VERSION FORMAT: MAJOR.MINOR.PATCH[-suffix]                                  ║
║  FULL ID: USF-{VERSION}-{TIMESTAMP}-{HASH}                                   ║
║                                                                              ║
║  STATUSES: ACTIVE, ROLLED_BACK, SUPERSEDED, ARCHIVED                         ║
║                                                                              ║
║  OPERATIONS: Create, Query, Rollback, Branch, Merge                          ║
║                                                                              ║
║  STORAGE: Differential with periodic snapshots                               ║
║                                                                              ║
║  AUDIT: Complete trail, immutable, 7-year retention                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## Appendix B: Change Log

| Version | Date | Changes |
|---------|------|---------|
| 4.0.0 | 2025-12-10 | Initial USF 4.0 version lineage specification |

---

*This document is part of the USF 4.0 specification suite. See MASTER-SPECIFICATION.md for framework overview.*
