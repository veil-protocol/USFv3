# USF 8.0 — Module Architecture

The one abstraction that makes USF a platform instead of a script.

## The contract

Every aspect of USF — calibration, planning, verification, efficiency,
self-evolution, and every future capability — is a **Module** implementing a
uniform contract (`engine/module.py`):

| Method | Purpose |
|---|---|
| `run(*args)` | do the module's job |
| `validate() -> ValidationResult` | prove it still works; consumed by self-evolution and CI |
| `improve(proposal)` | accept a *validated, gated* self-evolution proposal |
| `vampirize(source) -> [patterns]` | extract candidate patterns from external content |

Plus declared metadata: `id`, `version`, `summary`, `capabilities`
(a set of strings), `provenance` (where its patterns came from), and the
`improvable` / `vampirizable` flags.

## Why this shape

The user's thesis: *every modular aspect of USF can be built upon, improved, and
accept outside repos/research/content to be vampirized upon.* The four contract
methods are exactly those four affordances:

- **built upon** — register new modules; they compose through the registry.
- **improved** — `improve()` is the hook the bounded self-evolution loop drives.
- **vampirize** — `vampirize()` is the extraction step of the ingest pipeline.
- **validated** — `validate()` is how any change is proven safe before it sticks.

## Capability scope = the safety bound

The **union of all modules' `capabilities`** is the system's *capability scope*.
The bounded-self-improvement guarantee (the paper's fixed-point claim) holds only
while that scope is constant — so `ModuleRegistry.scope_hash()` is the quantity
the evolution engine watches. Tuning within a fixed scope converges; **adding a
capability** (a new module, or a module declaring a new capability) changes
`scope_hash`, trips the capability-scope gate, and forces human Phase-1 approval.
This is the generalization of the "cycle-4 spike": absorbing 47 external patterns
at once expanded scope and re-opened attack surface.

## Registry

`ModuleRegistry` holds modules, exposes `capability_scope()` / `scope_hash()`,
and runs `validate_all()`. `build_default_registry()` wraps today's modules
(`precision.calibrator`, `plan.planner`) under the contract; verification,
efficiency, and evolution register as they land.

## Lifecycle of an external contribution (preview — see VAMPIRIZE-PROTOCOL)

```
external repo/research/content
    → module.vampirize(source)         # extract candidate patterns
    → PATTERN-PROVENANCE               # pin source, date, confidence, rollback handle
    → IMPROVEMENT-PROTOCOL validation  # anchors ≥0.7, regression, adversarial, safety
    → capability_scope gate            # scope expansion? → human Phase-1
    → module.improve(proposal)         # fold in; version bumps; lineage records
```

A contribution that merely tunes an existing capability flows through
automatically (subject to bootstrap phase); one that adds a capability is always
human-gated. That asymmetry is the whole safety story.
