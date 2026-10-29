---
id:              TMPL-CODE-REVIEW
domain_match:    [T.DEV.*, T.AI]
precision_floor: PL2
panel:           [ARC-AD (breakage, lead), ARC-IM (senior engineer), ARC-QA (test lead), ARC-TH (cs theory), ARC-ST (architect)]
---

# Code Review

**Purpose.** Turn a diff or codebase into a prioritized review: verified findings
with fixes, not a wall of nitpicks. Use for PR review, audits, refactors.

## Phases
0. **Scope** — identify changed surface, entry points, trust boundaries.
1. **Read** — ARC-IM walks intent; ARC-TH checks invariants/complexity.
2. **Attack** — ARC-AD hunts correctness bugs, edge cases, injection, resource leaks.
3. **Fix** — propose minimal, idiomatic fixes matching surrounding style.
4. **Verify** — ARC-QA confirms each finding reproduces and each fix holds (no regression).
5. **Prioritize** — rank by severity × confidence; drop the unverified.

## Verification
Chains A (static), B (dynamic/run the test), F (TDD — write a failing test first),
H (debug). A finding ships only if B or F **reproduces** it — no speculative bugs.
PL rises with blast radius (prod/irreversible → PL4).

## Output (codified grammar)
```
[FINDING] <bug/smell>  file:line   [STAT:severity=HIGH,confidence=0.9]
[CLAIM] reproduces via <test/input>   [VERDICT:conf=0.95]
<proposed fix — minimal, in-style>
[LIMITATION] <what wasn't covered; assumptions>
```
Final product: summary (counts by severity) → verified findings w/ fixes →
nice-to-haves (clearly separated) → what was out of scope.
