# USF 8.0 — Vampirize Protocol

How USF absorbs outside repos, research, and content — safely.

> *"Every modular aspect of USF can be built upon, improved, and accept outside
> repos/research/content to be vampirized upon."*

This is the governed path that makes assimilation a feature instead of a risk.
It is the operational generalization of the RAPTOR-cannibalization playbook
(extract strengths, reject weaknesses) wired to PATTERN-PROVENANCE and the
capability-scope safety bound.

## The pipeline (`engine/vampirize.py`)

```
ExternalSource (repo | paper | content, pinned URL)
    │
    ▼
[1] EXTRACT     module.vampirize(source) → CandidatePattern[]
[2] CONFIDENCE  drop anything below the extractor floor (default 0.60)
[3] TARGET      resolve the module to fold into (or flag a new capability)
[4] VALIDATE    improvement-protocol gates: anchor ≥0.70 · regression ·
                adversarial/meta-attack · safety invariants
[5] PROVENANCE  pin {source permalink (NOT HEAD), ingest date, confidence, id}
[6] SCOPE GATE  does it add a capability?
       ├─ no  → TUNING  → bootstrap approval (auto if phase allows) → module.improve()
       └─ yes → EXPANSION → QUEUE for human Phase-1 (scope_hash unchanged until approved)
[7] LINEAGE     every applied pattern = a new content-hashed version node
```

## The safety asymmetry

A contribution that **tunes** an existing capability can flow in automatically
(subject to the bootstrap phase and risk tier). A contribution that **adds** a
capability is *always* human-gated, because it changes `scope_hash` and therefore
leaves the bounded-self-improvement fixed point — exactly the cycle-4 event
(absorbing 47 external patterns at once re-opened attack surface, findings 5→14).

Worked example (`python3 vampirize.py`), ingesting a fictional framework:

| Pattern | Effect | Outcome |
|---|---|---|
| `SC-01` token-budget heuristic | tunes `plan.planner` | **folded** (auto) |
| `SC-02` stricter Sybil threshold | tunes `verify.chains` | **folded** (auto) |
| `SC-03` whole new bioinformatics domain | **adds capability** | **queued for human** — scope_hash unchanged |
| `SC-04` half-baked idea (conf 0.40) | below floor | **rejected** |

## Provenance is mandatory

Every absorbed pattern records where it came from — a *pinned* permalink (a
commit SHA, not a moving branch), the ingest date, and the confidence at ingest.
This is what lets a vampirized pattern be audited, drift-reviewed, and rolled
back per-pattern. External provenance is a first-class field on every `Module`.

## Why this is the keystone

With this, USF stops being a fixed artifact and becomes a *platform that grows by
eating*: new frameworks, papers, and research become modules or module
improvements through one contract — and the capability-scope gate guarantees the
growth stays bounded and auditable rather than runaway.
