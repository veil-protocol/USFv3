# `_harvested/` — reference implementations (NOT on the wired path)

These modules were harvested from prior USF versions (6.9 / 7.0) during the 8.0
consolidation. They are preserved for **provenance and future wiring** — none of
them is imported by the active product, and some do not import standalone (they
were package-internal in their origin tree, e.g. `efficiency/integration.py` and
`agents/spawner.py`, which expected an `omega`/`retrieval` package that is out of
scope here).

**Do not import from `_harvested/` in the wired product.** The active, tested
equivalents are:

| Harvested here | Wired replacement (active) |
|---|---|
| `efficiency/*` (tiered_loader, deduplication, token_counter, context_budget, integration) | `engine/codex.py` (tiering + dedup + token budget, stdlib) |
| `evolution/{sona_router,learning_daemon,consensus,circuit_breaker,task_claims,skill_extractor,tldr_analyzer,continuity_ledger}` | `engine/evolution/{oracle_meta,capability_scope,version_lineage,bootstrap}.py` |
| `agents/{spawner,domain_detector}` | `engine/usf.py` (domain detection + panel synthesis) + `engine/calibrator.py` |

They remain here as a menu of patterns to re-wire cleanly (each is a documented
7.0 capability). Re-wiring any of them is a capability-scope change and must go
through the self-evolution gate (see `SPEC/VAMPIRIZE-PROTOCOL.md`).
