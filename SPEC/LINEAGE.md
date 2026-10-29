# USF Lineage — 4.1.1 → 8.0 REBORN

This repository's public history jumps from **4.1.1** (the SKYNET-HARDENED release
that the paper *"Bounded Self-Improvement in AI Reasoning — The USF Framework"*
references) to **8.0 REBORN**. This note makes that jump legible.

## What happened between 4.1.1 and 8.0

Public history shows two 4.1.1 commits. Development continued privately across
several iterations that were never published here:

| Version | What it added | Fate |
|---|---|---|
| **4.1.1** SKYNET-HARDENED | the published spine: 4 engines, 5 archetypes, PL1–5, N-chain verification, self-evolution | the paper's reference release (this repo's `main`) |
| 5.0–5.3 PROMETHEUS/TITAN/FORGE/APEX | re-cast as a 15-engine layered architecture; agent factory, triage, prompt forge, security hardening | internal |
| 6.0–6.9 OMEGA | wired what 4–5 only specified; reached a hardened, ~95%-integrated spine | internal (the stable base) |
| 7.0 | ingested 16 ecosystem patterns (SONA router, TLDR, learning daemon, continuity ledger, Byzantine consensus…) | **reverted** — broken wiring + security regressions + entanglement with a pentest engine |
| **8.0 REBORN** | consolidation + wiring: the spec made to actually run | **this branch** |

## What 8.0 REBORN is

The audit that produced 8.0 found that every prior version was ~80%
specification, ~20% wired. 8.0's commitment is the inverse — *specification that
runs*:

- the **precision calibrator** (CS/DC/AE/VA/TC), specced in every version and
  never coded, now exists and self-tests;
- the **efficiency layer** that reported 1.0× now reduces ~4×;
- the **plan-mode hook** that was only ever a design doc now fires;
- the paper's **bounded-self-improvement** claim is re-runnable
  (`engine/evolution/redteam_cycle.py` replays the 49/20 figure and reproduces
  the convergence signature live), with `scope_hash` as the fixed-point boundary.

It reclaims the aspirational "v8.0 ASCENSION" name — and, unlike that plan, runs.

## The self-evolution lineage mechanism

Going forward, every improvement is a content-hashed node in the version tree
described in `SPEC/self-evolution/VERSION-LINEAGE.md`, created by the Oracle-Meta
loop and gated by capability scope. 8.0 is the genesis of that running lineage.

OMEGA (the offensive-security engine that 7.0 entangled) is **not** part of USF —
it is a separate product and is excluded here by design.
