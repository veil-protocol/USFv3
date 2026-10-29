# USF v3 — Template Gallery

The gallery is the **breadth receipts**: the same forge pipeline, pointed at
different domains, each producing a finished product. Security is one exhibit,
not the museum.

Every template is the *same shape* — only the domain, panel, and phases change.
That sameness is the point: it shows USF is a universal methodology.

## Template contract

```
---
id:              TMPL-<DOMAIN>-<VARIANT>
domain_match:    [taxonomy keys, e.g. S.SCI.*]
precision_floor: PLn            # minimum precision for this domain
panel:           [archetype emphasis]
---
# <title>
Purpose · when to use
## Phases        (the staged elaboration for this domain)
## Verification  (which chains, what "done" means here)
## Output        (codified-grammar shape of the finished product)
```

A template plugs into the planner: `usf.py` detects the domain → selects the
template → the panel + phases below drive the ELABORATE and VERIFY stages.

## The gallery

| Template | Domain | Product it forges |
|---|---|---|
| `TMPL-SEC-AUTONOMOUS` | security / vuln research | validated findings + benign PoC + report (the flagship exhibit) |
| `TMPL-RESEARCH-SYNTHESIS` | science / research | a cited, adversarially-checked research report |
| `TMPL-CODE-REVIEW` | software | a prioritized review with verified findings + fixes |
| `TMPL-PRODUCT-SPEC` | business / product | a vision → complete, decision-ready specification |
| `TMPL-DECISION-ANALYSIS` | cross-domain | a defensible recommendation from competing options |

New domains arrive via the **Vampirize** pipeline — ingest an external
methodology, and it becomes a new template/module (capability-scope-gated).
