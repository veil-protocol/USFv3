---
id:              TMPL-DECISION-ANALYSIS
domain_match:    [cross-domain, L.LAW, F.FIN, M.MED, E.ENG]
precision_floor: PL3
panel:           [ARC-ST (lead), ARC-TH (first-principles), ARC-AD (opposing view), ARC-IM (feasibility), ARC-QA (risk)]
---

# Decision Analysis

**Purpose.** Turn a choice among options into a defensible recommendation. Use
for build-vs-buy, vendor selection, policy/strategy, any high-stakes decision.
Deliberately cross-domain — the clearest proof the forge generalizes.

## Phases
0. **Frame** — the decision, the decision-maker, the constraints, the deadline.
1. **Options** — enumerate real alternatives (incl. "do nothing"); no straw men.
2. **Criteria** — weighted decision criteria tied to the stated goal.
3. **Score** — each option × criterion, with evidence; ARC-TH checks the model.
4. **Steel-man + attack** — ARC-AD argues the *strongest* case for the runner-up, then attacks the leader.
5. **Recommend** — ARC-ST synthesizes; ARC-QA stress-tests the downside.

## Verification
Chains C (formal — is the scoring model coherent?), D (empirical evidence per
score), E (expert review). PL4+ for irreversible/high-consequence decisions
(the calibrator floors these via CS). Requires a stated **reversibility** and
**what-would-change-my-mind**.

## Output (codified grammar)
```
[FINDING] recommendation: <option>
[DATA] decision matrix (options × weighted criteria)
[CLAIM] <option> wins because <evidence>   [VERDICT:conf=0.xx]
[STAT:reversibility=…,confidence=…]
[LIMITATION] key uncertainties; what would change the recommendation
```
Final product: recommendation up front → options → weighted matrix → the case
against → risks & reversibility → what-would-change-my-mind.
