# USF 8.0 — Codified Output Grammar

One grammar, unifying conventions that were scattered across prior versions
(7.0 structured markers + the role-tag persona format from `CONTEXT-OPTIMIZATION`
+ `ARC-id@domain` refs) and never written down together. Implemented in
`engine/codex.py`.

## 1. Structured markers

Agents emit findings as single-line markers so downstream stages can parse
without NLP. Grammar:

```
[KIND]              text
[KIND:k=v,k=v]      text
```

| Marker | Use |
|---|---|
| `[FINDING]` | a discovered issue / result |
| `[CLAIM]` | an assertion to be verified |
| `[STAT:k=v]` | a measured statistic (e.g. `[STAT:validated=1,false_positive=5]`) |
| `[DATA]` | a raw data payload |
| `[LIMITATION]` | an honest scope/limitation note |
| `[VERDICT:conf=0.95]` | a verification outcome with confidence |

Round-trips: `codex.emit(...)` ↔ `codex.parse(...)`.

## 2. Role-tag personas

A full expert persona (~1 KB) collapses to a two-line tag (~150 chars, −85%):

```
Role: <persona> | Focus: <primary_mode>
Key approach: <behaviour>; <behaviour>
```

Full detail is loaded from cache only in verbose mode. The even-more-compact
form is an **archetype reference**: `ARC-AD@security` (archetype × domain),
expanded on demand.

## 3. Efficiency — tiered, deduped context assembly (now actually wired)

Prior versions shipped `tiered_loader`/`deduplication` but the executor still
hard-truncated context at 8000 chars — a **measured 1.0×**. `codex.assemble_context`
replaces that: it de-duplicates, routes each chunk to a tier by relevance, and
fills a token budget by descending relevance.

| Relevance | Tier | Rendering |
|---|---|---|
| ≥ 0.70 | L1 | full text |
| ≥ 0.40 | L2 | lead sentence(s) per paragraph |
| < 0.40 | L3 | headers / first line only |

Measured on the self-test corpus: **4.74× reduction** with the duplicate dropped.
This is the single biggest efficiency fix in the consolidation — turning a
designed-but-unwired capability into a running one.

## Where it applies

- agent **prompts** (role-tag personas, archetype refs)
- the **shared context** injected into each spawned agent (tiered assembly)
- agent **outputs** (structured markers → machine-parseable aggregation)
