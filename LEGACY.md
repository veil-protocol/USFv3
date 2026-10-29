# Legacy repositories — superseded by USF v3 REBORN

USF development had fragmented across five separate repositories with divergent
version numbers. USF v3 REBORN consolidates all of them into this one. The
others are archived; nothing unique was lost (every canonical asset was carried
forward into `engine/`, `SPEC/`, or `templates/`).

| Repo | Was | Status |
|---|---|---|
| `veil-protocol/usf` (this repo) | public 4.1.1 spec + the paper | **canonical — now v3 REBORN** |
| `veil-protocol/usf-2-prod` | the 6.9 heavy engine (~100K LOC) | archived — engine wiring harvested |
| `veil-protocol/usf-7` | the 7.0 build (reverted) | archived — tested patterns cherry-picked |
| `veil-protocol/USF-2` | an early 2.0 clean rebuild | archived — ancestor |
| `veil-protocol/omega-v6` | **OMEGA pentest engine** | **not archived — separate product**, intentionally out of scope |

## What was carried forward

- **Agents & archetypes** — the 207-agent registry + 5 archetypes (`engine/`)
- **Specs** — core, precision, domain-adaptation, integration, self-evolution,
  plus the richer `usf-spec` set (PATTERN-PROVENANCE, RAPTOR-CANNIBALIZATION,
  UNCERTAINTY-QUANTIFICATION, the IMP-* postmortems, the cycle log) → `SPEC/`
- **The security template** — `TMPL-SEC-AUTONOMOUS` → `templates/` (one exhibit)
- **Tested 7.0 patterns** — SONA router, TLDR, learning daemon, continuity
  ledger, consensus, circuit breaker → `engine/evolution/`

## What was deliberately left behind

The OMEGA offensive-security surface (attack MCP tools, OODA/genetic/C2,
TERROR-NEXUS, the red-team agent corpus) — it is a separate solution, not part of
the USF framework.

To toggle the GitHub archive flag on the three superseded USF repos, run
`gh repo archive veil-protocol/<name>` (an outward action — do only when ready).
