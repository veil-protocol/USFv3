---
id:              TMPL-PRODUCT-SPEC
domain_match:    [B.BIZ, T.DEV.product]
precision_floor: PL2
panel:           [ARC-ST (strategist, lead), ARC-IM (operator), ARC-AD (devil's advocate), ARC-TH (strategy theory), ARC-QA (diligence)]
---

# Product Spec

**Purpose.** Turn a rough idea into a complete, decision-ready specification —
the most literal "vision in → finished product out" exhibit. Use for feature
specs, PRDs, proposals.

## Phases
0. **Frame** — crisp problem statement; who hurts, how much, why now.
1. **Define** — users, jobs-to-be-done, success metrics, non-goals.
2. **Design** — the solution; alternatives considered and rejected (with reasons).
3. **Red-team** — ARC-AD attacks: riskiest assumption, failure modes, what kills it.
4. **De-risk** — mitigations, phasing, the smallest valuable first slice.
5. **Diligence** — ARC-QA checks feasibility, dependencies, cost, measurability.

## Verification
Chains D (empirical — is there evidence of the need?), E (expert review),
G (review). The "riskiest assumption" must be named and have a validation plan;
a spec with no stated risk fails ARC-AD.

## Output (codified grammar)
```
[FINDING] problem + why-now
[CLAIM] users will <behaviour> because <evidence>   [VERDICT:conf=0.xx]
[DATA] success metrics / targets
[STAT:riskiest_assumption=…] + validation plan
[LIMITATION] non-goals; open decisions; what we're betting on
```
Final product: one-pager → users & JTBD → solution & alternatives → metrics →
risks & mitigations → phased plan → open questions.
