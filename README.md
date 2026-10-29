<h1 align="center">USF 8.0 — REBORN</h1>
<p align="center"><strong>Unified Superintelligence Framework</strong></p>
<p align="center"><em>A universal product-forge: a vision in any domain goes in — a fully fleshed-out product comes out.</em></p>

---

## What USF is

USF is **not** a tool for one domain. It is a *methodology* that takes a rough
vision — a one-line goal in security, research, code, law, medicine, engineering,
science, anything — and transforms it, through meta-prompting and staged,
verified, multi-expert execution, into a finished artifact. Better than a single
pass ever could.

The template gallery and domain taxonomy are not the product. They are the
**receipts** — evidence that the same machinery produces a defensible product
whatever you point it at.

> This repository is the running realization of the published paper
> **"Bounded Self-Improvement in AI Reasoning — The USF Framework."**
> The paper is the *why*. This repo is *it actually runs*.

## The thesis: bounded self-improvement

The paper's contribution is that a sufficiently well-structured reasoning system
possesses **discoverable fixed points under self-analysis — provided its
capability scope stays constant.** Improvement converges to stability instead of
diverging. Expanding capability resets the equilibrium (the "cycle-4 spike":
adding 47 patterns from 8 sources at once re-opened attack surface and findings
jumped 5 → 14). So in USF 8.0, **capability scope is an explicit, versioned,
human-gated boundary** — the safety lever that makes self-improvement bounded.

## The pipeline (the heart)

```
  YOUR VISION  (any domain, any fidelity)
        │
        ▼
  [1] DETECT      read the intent, place it in the domain taxonomy
  [2] CALIBRATE   score CS/DC/AE/VA/TC → Precision Level (PL1–PL5) + compute + panel
  [3] META-PROMPT synthesize an expert panel from 5 archetypes × the domain
  [4] ELABORATE   draft → Attack-Fix-Verify → synthesize
  [5] VERIFY      independent chains, dependency-aware consensus, early-exit
  [6] RENDER      codified-output grammar, efficiency-tiered
        │
        ▼
  FULLY FLESHED-OUT PRODUCT
```

Steps 1–3 are the meta-prompting core: **USF writes the experts and the plan
from your seed.** Steps 4–5 harden a rough draft into something defensible.

## What's in the box

```
engine/          the wiring (the whole point — these actually run)
  calibrator.py    CS/DC/AE/VA/TC → PL. First real implementation of a model
                   that was specced in every prior version and never coded.
  usf.py           the planner: vision → configured, staged execution plan
  registry.yaml    207 synthesized agents across 6 domains
  archetypes/      the 5 universal archetypes (ARC-TH/AD/IM/ST/QA)
  domain_detector.py · spawner.py
  efficiency/      context tiering · dedup · token budget · TLDR
  evolution/       self-improvement patterns (SONA · ledger · consensus · …)
SPEC/            the specification (core · precision · self-evolution · …)
  evolution-log/   the reproducible red-team cycle log (the paper's data)
  net-new-methods/ orthogonal-chain verification, uncertainty quant, cross-domain transfer
templates/       the domain gallery (TMPL-SEC-AUTONOMOUS = the security exhibit)
.claude/         Claude Code integration: hooks + skills
demos/           worked runs, incl. the convergence-table reproduction
```

## Quickstart

```bash
python3 engine/usf.py "audit the key-exchange in our auth service"      # auto-configures
python3 engine/usf.py "write a deep research report on X" --precision 4 --json
python3 engine/usf.py --show-interface                                  # the control panel
python3 engine/calibrator.py                                            # calibrator self-test
```

Magic keywords steer precision inline: `ultrathink` → PL5, `think` → PL2, `eco` → PL1.

## Status

This is a **consolidation + wiring** release. The defining finding of the audit
was that every prior USF was ~80% specification and ~20% wired (efficiency
reported 0×, the calibrator was never coded, the template dir was empty, the
plan-mode hooks never existed). 8.0's commitment is the inverse: **specification
that runs** — every feature is either connected or honestly cut.

All components are built, wired, and pass the self-test gate (`run_tests.py`,
10/10). Zero third-party dependencies — Python 3.10+ standard library only.

| Component | State |
|---|---|
| Precision calibrator (CS/DC/AE/VA/TC) | ✅ built + tested (was never coded before) |
| Canonical specs + 207-agent registry + archetypes | ✅ consolidated |
| Planner / staged pipeline | ✅ wired + tested |
| Verification chains + consensus | ✅ wired + tested |
| Self-evolution loop + capability-scope gate + cycle harness | ✅ wired + reproduces the paper's convergence |
| Codified-output grammar + efficiency wiring | ✅ wired (4.74× vs old 1.0×) |
| Plan-mode hook (the glue that never existed) | ✅ wired + tested |

Reference implementations harvested from prior versions (not on the wired path)
are kept under `engine/_harvested/` for provenance.

## Lineage

Public identity (this repo + the paper) is **4.1.1 SKYNET-HARDENED**. Internal
work reached 6.9 (hardened spine) and a 7.0 build that was abandoned. **8.0 REBORN
reclaims the aspirational "ASCENSION" name — and, unlike it, runs.** OMEGA (the
pentest engine) is a separate solution and is deliberately excluded.

MIT licensed.
