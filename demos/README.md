# USF 8.0 — Demos

```bash
python3 demos/run_all.py        # the full tour (from repo root)
```

Three acts:

1. **Breadth** — the same planner routes five different domains (security,
   research, code, product, decision), each getting its own precision level,
   compute type, and synthesized expert panel. One forge, many products.

2. **Convergence** — the red-team cycle harness. Replays the recorded cycle log
   (matches the paper's 49 findings / 20 fixes) and runs the bounded loop live on
   the module registry, showing defects fall to a fixed point until a capability-
   scope expansion (watch `scope_hash` change) spikes them, then re-converge.

3. **Vampirize** — ingests a fictional external framework: tuning patterns fold
   in automatically with pinned provenance, a new-capability pattern is queued for
   human approval (scope unchanged), a low-confidence pattern is rejected.

Individual pieces are runnable too:

```bash
python3 engine/usf.py --show-interface
python3 engine/usf.py "your vision here" [--precision N] [--json]
python3 engine/calibrator.py
python3 engine/verification.py
python3 engine/codex.py
python3 engine/vampirize.py
python3 engine/evolution/redteam_cycle.py
```
