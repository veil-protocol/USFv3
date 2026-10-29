# USF 8.0 — The Thesis, Running

> The published paper **"Bounded Self-Improvement in AI Reasoning — The USF
> Framework"** is the *why*. This repository is *it actually runs*.

## The claim

A sufficiently well-structured reasoning system possesses **discoverable fixed
points under self-analysis — provided its capability scope stays constant.**
Self-improvement converges to stability instead of diverging. The paper's
evidence is a self-applied red-team series whose defect counts fall
monotonically (18 → 10 → 5), spike when capability expands (→ 14, the SKYNET
event: 47 patterns from 8 sources ingested at once), then re-converge (→ 2).

The paper names its own weakness: a **"formal verification gap"** — the
convergence is empirical, not proven, and whether it generalizes "remains an open
question."

## How USF 8.0 answers both

**The verification gap → made operational.** The fixed point is no longer an
observation in a PDF; it is a quantity the running system tracks.
`ModuleRegistry.scope_hash()` *is* the capability scope. `engine/evolution/`
runs the real Monitor→Analyze→Propose→Validate→Integrate loop, and
`redteam_cycle.py` regenerates the convergence signature on demand — replaying
the recorded 49/20 figure *and* reproducing the shape live on the module set.
You can watch `scope_hash` change the instant scope expands. The claim is now
re-runnable, which is the strongest thing short of a proof.

**The generalization question → answered by construction.** Every engine is
domain-agnostic; "domain" is only what the forge is pointed at. The **template
gallery** (security, research, code, product, decision) is the empirical answer:
the same pipeline produces a finished product in each. The paper asks whether the
methodology generalizes; the gallery is the receipts that it does.

**The safety bound → a hard gate, not a hope.** Because convergence holds only at
constant scope, scope expansion is dangerous *by design*. So it is gated:
`capability_scope.scope_gate` forces any capability-adding change — whether from
the self-evolution loop or the **Vampirize** ingest pipeline — onto the human
Phase-1 path, and a bulk expansion escalates to CRITICAL with a dedicated
red-team cycle. Tuning within scope flows automatically; growth never does
silently. That asymmetry is the whole safety story.

## Why this is the product worth being proud of

Prior USF versions were ~80% specification, ~20% wired — a beautiful idea that
never quite ran. USF 8.0's commitment is the inverse: **specification that
runs.** The calibrator that was specced five times and never coded now exists and
self-tests. The efficiency layer that reported 1.0× now reduces 4.74×. The
plan-mode hook that was only ever a design document now fires. And the paper's
headline claim — bounded self-improvement — is not an assertion in the README; it
is a program you can execute.

USF is a universal product-forge that improves itself, bounded, and grows by
assimilating the outside world through a governed gate. That is the final product.
