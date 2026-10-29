# USF Lineage — the three generations

**USF v3** is the third *generation* of the framework, not a step down from the
internal build numbers. Public history runs by generation:

| Gen | Public identity | What it was |
|-----|-----------------|-------------|
| **gen 1** | prototype | the original hardcoded expert-panel + Attack-Fix-Verify idea |
| **gen 2** | **USF 4.1.1 SKYNET-HARDENED** (+ USF-2) | the specification framework the paper *"Bounded Self-Improvement in AI Reasoning"* references: 5 archetypes, PL1–5, N-chain verification, self-evolution — mostly **spec** |
| **gen 3** | **USF v3 "REBORN"** (this repo) | the consolidation, **made to actually run** |

## What happened between gen 2 and gen 3

After the gen-2 public release, development continued privately and fragmented
across several repos:

| Internal | Added | Fate |
|---|---|---|
| 5.0–5.3 PROMETHEUS/TITAN/FORGE/APEX | re-cast as a 15-engine layered architecture; agent factory, triage, prompt forge, hardening | internal |
| 6.0–6.9 OMEGA | wired what 4–5 only specified; a hardened, ~95%-integrated spine | internal (the stable base) |
| 7.0 | ingested 16 ecosystem patterns (SONA router, TLDR, learning daemon, continuity ledger, Byzantine consensus…) | **reverted** — broken wiring + security regressions + entanglement with a pentest engine |

**USF v3** consolidates all of that into one running product.

## What v3 is

The audit that produced v3 found every prior version was ~80% specification,
~20% wired. v3's commitment is the inverse — *specification that runs*:

- the **precision calibrator** (CS/DC/AE/VA/TC), specced in every version and
  never coded, now exists and self-tests;
- the **efficiency layer** that reported 1.0× now reduces ~4×;
- the **plan-mode hook** that was only ever a design doc now fires;
- the paper's **bounded-self-improvement** claim is re-runnable
  (`engine/evolution/redteam_cycle.py` replays the 49/20 figure and reproduces
  the convergence signature live), with `scope_hash` as the fixed-point boundary.

## The running lineage

Going forward, every improvement is a content-hashed node in the version tree
described in `SPEC/self-evolution/VERSION-LINEAGE.md`, created by the Oracle-Meta
loop and gated by capability scope. v3 is the genesis of that running lineage.

OMEGA (the offensive-security engine that 7.0 entangled) is **not** part of USF —
it is a separate product and is excluded here by design.
