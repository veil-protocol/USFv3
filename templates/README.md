# USF v3 — Template Library

A template supplies the domain-specific **phase structure** the forge runs during
ELABORATE. The library is the **breadth receipts**: the same pipeline, pointed at
any domain, each producing a finished product. Security is one exhibit, not the
museum.

## Two representations

- **`TEMPLATE-LIBRARY.yaml`** — the registry: all 16 template IDs + the
  domain→template routing the planner uses.
- **`TEMPLATE-DEFINITIONS.yaml`** — the full specs: each template's `name`,
  `extends`, phase list, and time budgets.
- **`TMPL-*.md`** — worked, human-readable *exhibits* for the most-used templates
  (prose phases + verification + codified-output shape).

The planner auto-selects a template by domain (`usf.py` → `select_template`;
override with `--template`). `usf.py --show-interface` lists the whole library.

## The 16-template library

| Template | Domain | Forges |
|---|---|---|
| `TMPL-SEC` | security | 7-phase security analysis |
| `TMPL-SEC-AUTO` | security / bug-bounty | autonomous vuln research + AFP gates (full `.md` exhibit: `TMPL-SEC-AUTONOMOUS.md`) |
| `TMPL-SEC-PQC` | crypto | post-quantum cryptography analysis (auto-selected for `T.SEC.CRY`) |
| `TMPL-SEC-PRO` | security | protocol analysis |
| `TMPL-SEC-APT` | security / CTI | APT campaign analysis |
| `TMPL-PENTEST` | security | penetration-testing structure |
| `TMPL-DSN` | engineering | system design |
| `TMPL-DSN-DIS` | engineering | distributed-systems design |
| `TMPL-SCI` | science | scientific research |
| `TMPL-SCI-EXP` | science | experimental design |
| `TMPL-LEG` | legal | legal analysis |
| `TMPL-BUS` | business / finance | business analysis |
| `TMPL-BUS-MA` | business | M&A due diligence |
| `TMPL-DEV-ENHANCED` | software | software development |
| `TMPL-X-SECBUS` | cross-domain | security × business |
| `TMPL-X-LEGTECH` | cross-domain | legal × tech |

## Worked `.md` exhibits (prose templates)

Complementary human-readable exhibits that show the pipeline end-to-end in a
domain: `TMPL-SEC-AUTONOMOUS` (the flagship), plus `TMPL-RESEARCH-SYNTHESIS`,
`TMPL-CODE-REVIEW`, `TMPL-PRODUCT-SPEC`, `TMPL-DECISION-ANALYSIS`.

## Adding templates

New domains arrive via the **Vampirize** pipeline — ingest an external
methodology and it becomes a new template/module entry, capability-scope-gated
(see `SPEC/VAMPIRIZE-PROTOCOL.md`). Adding a template is a scope expansion →
human Phase-1 approval.
