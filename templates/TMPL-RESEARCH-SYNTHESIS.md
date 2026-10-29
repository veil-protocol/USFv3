---
id:              TMPL-RESEARCH-SYNTHESIS
domain_match:    [S.SCI.*, T.AI, default-research]
precision_floor: PL3
panel:           [ARC-TH (lead), ARC-AD (skeptic), ARC-IM (experimentalist), ARC-ST (PI), ARC-QA (peer review)]
---

# Research Synthesis

**Purpose.** Turn a research question into a cited, adversarially-checked report.
Use for literature synthesis, state-of-the-art surveys, deep-dive analyses.

## Phases
0. **Frame** — sharpen the question; define scope, inclusion/exclusion criteria.
1. **Gather** — multi-modal source sweep (by-topic, by-author, by-time, by-method); record each source with a pinned reference.
2. **Extract** — per source, emit `[CLAIM]`/`[DATA]`/`[STAT:…]` with provenance.
3. **Synthesize** — cluster claims; build the narrative; ARC-ST frames implications.
4. **Adversarial pass** — ARC-AD attacks every load-bearing claim; weak ones are cut or hedged.
5. **Peer review** — ARC-QA checks coverage gaps, citation integrity, overclaiming.

## Verification
Chains A (source trace), D (empirical corroboration), E (expert review), G (review);
at PL4+ add C (formal/quantitative where applicable). A claim survives only on
**4/5 agreement**. Disagreement-rate sanity check: if independent chains agree
>95%, suspect circularity — widen sources.

## Output (codified grammar)
```
[FINDING] <synthesized conclusion>
[CLAIM] <supporting claim>   (cite: <pinned ref>)   [VERDICT:conf=0.xx]
[STAT:effect=…,n=…] <quantitative result>
[LIMITATION] <what this does NOT establish; open questions>
```
Final product: executive summary → thematic synthesis → evidence table →
limitations → references. Honest "no strong finding" is a valid result.
