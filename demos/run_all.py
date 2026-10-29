#!/usr/bin/env python3
"""
USF 8.0 REBORN — demo runner.

One script that exercises the whole forge:
  1. BREADTH   — the same planner routes 5 different domains (the gallery receipts)
  2. CONVERGE  — the red-team cycle harness (paper replay + live bounded run)
  3. VAMPIRIZE — ingest an external framework through the governed pipeline

Run:  python3 demos/run_all.py      (from the repo root)
"""

import pathlib
import sys

_ENGINE = pathlib.Path(__file__).resolve().parent.parent / "engine"
for _p in (str(_ENGINE), str(_ENGINE / "evolution")):
    sys.path.insert(0, _p)

import usf
import verification
from module import build_default_registry
from version_lineage import VersionLineage
import redteam_cycle
from vampirize import VampirizePipeline, ExternalSource, CandidatePattern


def breadth() -> None:
    print("=" * 78)
    print("  1. BREADTH — one forge, five domains (the gallery receipts)")
    print("=" * 78)
    visions = [
        ("security", "audit the crypto key-exchange for nation-state adversaries"),
        ("research", "write a comprehensive research report synthesizing fixed-point theory"),
        ("code",     "review this authentication module for correctness bugs"),
        ("product",  "turn our 'AI meeting notes' idea into a complete product spec"),
        ("decision", "recommend build vs buy for our vector database, high stakes"),
    ]
    print(f"  {'tag':<10}{'detected':<14}{'PL':<4}{'compute':<12}{'lead expert':<22}agents")
    for tag, v in visions:
        p = usf.plan(v)
        lead = p.expert_panel[0]["persona"]
        print(f"  {tag:<10}{p.domain:<14}{p.precision_level:<4}{p.compute_type:<12}{lead:<22}{p.total_agents}")
    print("  → same pipeline, different domain/precision/panel each time. Universality.")


def vampirize_demo() -> None:
    print("\n" + "=" * 78)
    print("  3. VAMPIRIZE — assimilate an external framework (governed)")
    print("=" * 78)
    reg = build_default_registry()
    reg.register(verification.as_module())
    lin = VersionLineage()
    lin.genesis("8.0.0", reg.scope_hash(), "20261029000000")
    pipe = VampirizePipeline(reg, lin, phase=3)
    src = ExternalSource(
        name="SuperClaude-Framework", kind="repo",
        url="https://github.com/example/superclaude/tree/a1b2c3d",
        patterns=[
            CandidatePattern("SC-01", "token-budget heuristic", "plan.planner", 0.82, "LOW"),
            CandidatePattern("SC-02", "stricter Sybil threshold", "verify.chains", 0.78, "MEDIUM"),
            CandidatePattern("SC-03", "new bioinformatics domain", "domain.bioinformatics", 0.90, "HIGH",
                             adds_capabilities=frozenset({"domain.bioinformatics"})),
            CandidatePattern("SC-04", "half-baked idea", "plan.planner", 0.40, "LOW"),
        ])
    rep = pipe.ingest(src)
    print("  " + rep.summary())
    for f in rep.folded:            print("    folded   :", f)
    for q in rep.queued_for_human:  print("    queued   :", q)
    for r in rep.rejected:          print("    rejected :", r)
    print(f"  scope_hash unchanged (expansion NOT auto-applied): {reg.scope_hash()}")


if __name__ == "__main__":
    breadth()
    print()
    redteam_cycle.replay()
    redteam_cycle.live()
    vampirize_demo()
    print("\n" + "=" * 78)
    print("  USF 8.0 REBORN — forge demonstrated end to end.")
    print("=" * 78)
