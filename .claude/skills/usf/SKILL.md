---
name: usf
description: Run a vision through the USF 8.0 forge — configurable, staged, verified, multi-expert execution that turns a goal in any domain into a fully fleshed-out product. Use when the user says "use usf", invokes /usf, or wants USF's planning/execution applied.
argument-hint: <the vision / goal, any domain>
---

# USF 8.0 — forge a vision into a product

USF is a universal product-forge: a vision in any domain → a fully fleshed-out
product, via meta-prompting + staged, verified, multi-expert execution. Zero
external dependencies — the engine is plain Python.

## Steps

1. **Plan.** Configure the run:
   ```bash
   python3 engine/usf.py "$ARGUMENTS"
   # options: --precision N · --compute TYPE · --json · --show-interface
   ```
   This calibrates the Precision Level (CS/DC/AE/VA/TC factor model), picks the
   compute type, and meta-prompts the expert panel for the detected domain.

2. **Gate on precision.** If **PL3+**, enter plan mode (read-only explore → plan
   document → approval via ExitPlanMode) before doing the work. If PL1–2, proceed.

3. **Execute the pipeline** the plan prints:
   `DETECT → CALIBRATE → META-PROMPT → ELABORATE → VERIFY → RENDER`
   - spin up the synthesized **expert panel** (archetypes × domain) as the voices;
   - draft → run **Attack-Fix-Verify** (ARC-AD attacks, ARC-IM fixes, ARC-QA verifies);
   - **verify** with the plan's chains (see `engine/verification.py` for the
     dependency-aware, blind-vote, Sybil-hardened consensus rules);
   - **render** in the codified grammar (`[FINDING] [STAT:k=v] [VERDICT:conf=…]
     [LIMITATION]`) and assemble context efficiently (`engine/codex.py`).

4. **Pick a template** if one fits the domain (`templates/`), e.g. the
   `TMPL-SEC-AUTONOMOUS` exhibit for vulnerability research.

## Notes
- Magic keywords in the vision steer precision: `ultrathink`→PL5, `think`→PL2, `eco`→PL1.
- For maximum rigor on high-stakes work, pass `--precision 5` (9 chains, 99.9% target).
- To absorb an external repo/paper into USF, use `engine/vampirize.py` (see SPEC/VAMPIRIZE-PROTOCOL.md).
- USF improves itself, bounded: `engine/evolution/` runs the Oracle-Meta loop gated by capability scope.
---
