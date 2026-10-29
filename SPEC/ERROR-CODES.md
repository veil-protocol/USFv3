# USF 4.0 Error Code Registry

> **Version**: 4.0.3 (See VERSION.yaml)
> **Purpose**: Centralized error code definitions for USF 4.0 operations
> **Status**: Skeleton (to be expanded during implementation)
> **Last Updated**: 2025-12-10

---

## Error Code Format

```
{CATEGORY}-{SEVERITY}{NUMBER}

Categories:
  DET - Detection (Domain Detector)
  CLS - Classification (Domain Classification)
  GEN - Generation (Expert Generator)
  EXE - Execution (Execution Engine)
  VER - Verification (Verification Chains)
  CAL - Calibration (Precision Calibrator)
  MAL - Meta-Analysis (MAL Agents)
  IMP - Improvement (Improvement Protocol)
  VLN - Version Lineage
  SYS - System (General/Infrastructure)

Severity:
  1 - INFO (Informational, no action required)
  2 - WARN (Warning, may need attention)
  3 - ERROR (Error, operation may continue with degradation)
  4 - FATAL (Fatal, operation cannot continue)
  5 - CRITICAL (Critical, system-wide impact)

Number: 3-digit unique identifier within category
```

**Example**: `DET-3001` = Detection Error #001

---

## Detection Errors (DET-*)

| Code | Severity | Name | Description | Recovery |
|------|----------|------|-------------|----------|
| DET-1001 | INFO | Low Confidence Detection | Domain detected but confidence < 70% | Proceed with caveats |
| DET-2001 | WARN | Ambiguous Domain | Multiple domains equally likely | Request clarification |
| DET-3001 | ERROR | Domain Unrecognized | Cannot classify input domain | Fallback to generic |
| DET-3002 | ERROR | Signal Extraction Failed | Cannot extract domain signals | Request reformulation |
| DET-4001 | FATAL | Detector Unavailable | Domain detection service down | Cannot proceed |

---

## Classification Errors (CLS-*)

| Code | Severity | Name | Description | Recovery |
|------|----------|------|-------------|----------|
| CLS-1001 | INFO | Taxonomy Leaf | Classified to deepest taxonomy level | None needed |
| CLS-2001 | WARN | Shallow Classification | Could only classify to high level | Continue with broader scope |
| CLS-3001 | ERROR | Taxonomy Gap | Domain not in taxonomy | Log for MAL-COVERAGE |
| CLS-3002 | ERROR | Classification Conflict | Signals indicate conflicting domains | Use primary, note conflict |

---

## Generation Errors (GEN-*)

| Code | Severity | Name | Description | Recovery |
|------|----------|------|-------------|----------|
| GEN-2001 | WARN | Reduced Panel | Could not generate full panel size | Proceed with smaller panel |
| GEN-2002 | WARN | Archetype Imbalance | Panel doesn't match target distribution | Document deviation |
| GEN-3001 | ERROR | Persona Validation Failed | Generated persona inconsistent | Regenerate |
| GEN-3002 | ERROR | Knowledge Injection Failed | Could not inject domain knowledge | Use generic patterns |
| GEN-4001 | FATAL | Generator Unavailable | Expert generation service down | Cannot proceed |

---

## Execution Errors (EXE-*)

| Code | Severity | Name | Description | Recovery |
|------|----------|------|-------------|----------|
| EXE-1001 | INFO | Early Convergence | Converged before minimum iterations | Verify not premature |
| EXE-2001 | WARN | Slow Convergence | Approaching iteration limit | Consider precision upgrade |
| EXE-2002 | WARN | Resource Warning | 80% of budget consumed | Prepare graceful degradation |
| EXE-3001 | ERROR | Convergence Failure | Could not converge within limits | Force synthesis |
| EXE-3002 | ERROR | Gate Failure | Phase failed gate criteria | Return to phase |
| EXE-3003 | ERROR | Stall Detected | No progress for 3+ iterations | Intervention required |
| EXE-4001 | FATAL | Resource Exhaustion | Budget fully consumed | Graceful degradation |
| EXE-5001 | CRITICAL | Deadlock | System cannot proceed | Human intervention |

---

## Verification Errors (VER-*)

| Code | Severity | Name | Description | Recovery |
|------|----------|------|-------------|----------|
| VER-1001 | INFO | Chain Agreement | All chains agree | None needed |
| VER-2001 | WARN | Chain Disagreement | Chains disagree within tolerance | Use majority |
| VER-2002 | WARN | Insufficient Chains | Fewer chains than required | Document limitation |
| VER-3001 | ERROR | Chain Failure | Verification chain failed | Use remaining chains |
| VER-3002 | ERROR | Circularity Detected | Chain dependency violation | Invalidate affected chain |
| VER-3003 | ERROR | Confidence Below Target | Cannot achieve precision target | Downgrade precision or escalate |
| VER-4001 | FATAL | All Chains Failed | No verification possible | Cannot verify |

---

## Calibration Errors (CAL-*)

| Code | Severity | Name | Description | Recovery |
|------|----------|------|-------------|----------|
| CAL-1001 | INFO | Precision Override | User/rule override applied | Document override |
| CAL-2001 | WARN | Calibration Drift | Calibration accuracy degraded | Trigger recalibration |
| CAL-3001 | ERROR | Factor Scoring Failed | Cannot score precision factors | Use domain default |
| CAL-3002 | ERROR | Invalid Override | Override violates constraints | Reject override |

---

## Meta-Analysis Errors (MAL-*)

| Code | Severity | Name | Description | Recovery |
|------|----------|------|-------------|----------|
| MAL-1001 | INFO | No Findings | Agent found no issues | Log healthy state |
| MAL-2001 | WARN | Agent Degraded | Agent accuracy below threshold | Flag for review |
| MAL-2002 | WARN | Low Finding Acceptance | Proposals not being accepted | Review agent calibration |
| MAL-3001 | ERROR | Agent Conflict | Agents generating contradictions | Scope clarification |
| MAL-3002 | ERROR | Analysis Failed | Agent could not complete analysis | Skip agent, document |
| MAL-4001 | FATAL | Agent Unhealthy | Agent consistently failing | Propose replacement |
| MAL-5001 | CRITICAL | Self-Modification Violation | Agent tried to modify itself | Block and alert |

---

## Improvement Errors (IMP-*)

| Code | Severity | Name | Description | Recovery |
|------|----------|------|-------------|----------|
| IMP-1001 | INFO | Proposal Queued | Improvement queued for validation | None needed |
| IMP-2001 | WARN | Validation Partial | Some validation checks failed | Review manually |
| IMP-3001 | ERROR | Validation Failed | Improvement failed validation | Reject proposal |
| IMP-3002 | ERROR | Integration Failed | Could not apply improvement | Rollback |
| IMP-3003 | ERROR | A/B Test Inconclusive | Cannot determine improvement value | Extend test or reject |
| IMP-4001 | FATAL | Rollback Failed | Could not rollback bad improvement | Human intervention |
| IMP-5001 | CRITICAL | Bootstrap Violation | Attempted to modify protected component | Block and alert |

---

## Version Lineage Errors (VLN-*)

| Code | Severity | Name | Description | Recovery |
|------|----------|------|-------------|----------|
| VLN-2001 | WARN | Storage Warning | Lineage storage approaching capacity | Archive old versions |
| VLN-3001 | ERROR | Version Not Found | Requested version doesn't exist | Return error |
| VLN-3002 | ERROR | Reconstruction Failed | Could not reconstruct version | Try from alternate snapshot |
| VLN-3003 | ERROR | Hash Mismatch | Version content hash invalid | Attempt recovery |
| VLN-4001 | FATAL | Corruption Detected | Lineage data corrupted | Initiate recovery |

---

## System Errors (SYS-*)

| Code | Severity | Name | Description | Recovery |
|------|----------|------|-------------|----------|
| SYS-2001 | WARN | Performance Degraded | System running slow | Monitor, consider scaling |
| SYS-3001 | ERROR | Component Unavailable | Required component down | Retry or degrade |
| SYS-3002 | ERROR | Configuration Invalid | Configuration error detected | Use defaults |
| SYS-4001 | FATAL | System Failure | Core system failure | Emergency shutdown |
| SYS-5001 | CRITICAL | Security Violation | Security constraint violated | Halt and alert |

---

## Error Response Protocol

```yaml
error_response:
  severity_1_INFO:
    logging: "Standard log"
    notification: "None"
    action: "Continue"

  severity_2_WARN:
    logging: "Warning log with context"
    notification: "Aggregate in reports"
    action: "Continue with monitoring"

  severity_3_ERROR:
    logging: "Error log with full trace"
    notification: "Real-time to operators"
    action: "Attempt recovery, may degrade"

  severity_4_FATAL:
    logging: "Fatal log with full state dump"
    notification: "Immediate alert"
    action: "Graceful shutdown of affected operation"

  severity_5_CRITICAL:
    logging: "Critical log with audit trail"
    notification: "Emergency alert to all operators"
    action: "System-wide halt, human intervention required"
```

---

## Implementation Notes

This error code registry is a skeleton to be expanded during USF 4.0 implementation. Each error code should be:

1. **Unique** - No duplicate codes within category
2. **Descriptive** - Name clearly indicates the issue
3. **Actionable** - Recovery guidance provided
4. **Traceable** - Can be linked to specific code locations

---

## Appendix: Change Log

| Version | Date | Changes |
|---------|------|---------|
| 4.0.3 | 2025-12-10 | Initial error code skeleton per Cycle 3 red team |

---

*This document is part of the USF 4.0 specification suite. See MASTER-SPECIFICATION.md for framework overview.*
