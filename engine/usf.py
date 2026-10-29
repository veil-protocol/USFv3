#!/usr/bin/env python3
"""
USF 8.0 REBORN — Planner
========================

The front door of the forge. Turns a vision (any domain) into a configured,
staged execution plan: Precision Level, compute type, a synthesized expert
panel, verification depth, and the 6-stage pipeline that elaborates a seed into
a finished product.

This is the wired version of the "beautiful USF" planning dashboard: the
calibrator (calibrator.py) is a real dependency, not a keyword regex stub.

    python3 usf.py "audit the key-exchange in our auth service"
    python3 usf.py "write a deep research report on X" --precision 4 --json
    python3 usf.py --show-interface

Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass, field

import calibrator as cal


# --------------------------------------------------------------------------
# Compute types — the 8 that are genuinely implemented (5 dead ones from the
# old registry were cut). Each maps to an aggregation method.
# --------------------------------------------------------------------------

COMPUTE_TYPES: dict[str, dict] = {
    "sequential":  {"agg": "last_result",                 "desc": "one agent after another"},
    "parallel":    {"agg": "confidence_weighted_average", "desc": "all agents at once (default)"},
    "swarm":       {"agg": "best_of_n",                   "desc": "many agents, same problem, best wins"},
    "hivemind":    {"agg": "majority_vote",               "desc": "consensus voting (quorum)"},
    "pipeline":    {"agg": "chain_refinement",            "desc": "each output feeds the next"},
    "tournament":  {"agg": "elimination",                 "desc": "agents compete, winner takes all"},
    "critic_loop": {"agg": "refined",                     "desc": "generate, then critique"},
    "ensemble":    {"agg": "weighted_combination",        "desc": "multiple approaches combined"},
}

# Keyword → compute auto-selection (highest-specificity first).
_COMPUTE_SIGNALS: list[tuple[tuple[str, ...], str]] = [
    (("security", "audit", "vulnerab", "attack", "exploit", "pentest", "threat"), "hivemind"),
    (("max", "comprehensive", "thorough", "exhaustive", "complete"),              "swarm"),
    (("compare", "evaluate", "benchmark", "versus", " vs ", "best option"),       "tournament"),
    (("draft", "refine", "critique", "polish", "improve"),                        "critic_loop"),
    (("quick", "simple", "basic", "explain", "fast", "trivial"),                  "sequential"),
    (("analyze", "review", "assess", "research", "investigate", "report"),        "parallel"),
]


def auto_compute(task: str) -> str:
    t = task.lower()
    for signals, compute in _COMPUTE_SIGNALS:
        if any(s in t for s in signals):
            return compute
    return "parallel"


# --------------------------------------------------------------------------
# Archetype synthesis — the meta-prompting core. 5 universal archetypes get
# synthesized into domain-specific experts.
# --------------------------------------------------------------------------

ARCHETYPES: dict[str, tuple[str, str]] = {
    "ARC-TH": ("Theoretical", "constructive_analysis"),
    "ARC-AD": ("Adversarial", "destructive_analysis"),
    "ARC-IM": ("Implementation", "constructive_engineering"),
    "ARC-ST": ("Strategic", "holistic_synthesis"),
    "ARC-QA": ("Quality Assurance", "verification_validation"),
}

# taxonomy key prefix → coarse family used for persona synthesis.
def domain_family(domain: str) -> str:
    if domain.startswith("T.SEC") or domain == "T.DEV.SEC":
        return "security"
    if domain.startswith("T.DEV") or domain == "T.AI":
        return "software"
    if domain.startswith("S.SCI"):
        return "science"
    if domain.startswith("L.LAW"):
        return "legal"
    if domain.startswith("M.MED"):
        return "medicine"
    if domain.startswith("F.FIN"):
        return "finance"
    if domain.startswith("E.ENG"):
        return "engineering"
    if domain.startswith("B.BIZ"):
        return "business"
    return "general"


# family × archetype → concrete expert persona.
_PERSONA: dict[str, dict[str, str]] = {
    "security":    {"ARC-TH": "Security Researcher", "ARC-AD": "Red Team Operator", "ARC-IM": "Security Engineer", "ARC-ST": "Security Architect", "ARC-QA": "Security Auditor"},
    "software":    {"ARC-TH": "Computer Scientist", "ARC-AD": "Breakage Engineer", "ARC-IM": "Senior Engineer", "ARC-ST": "Principal Architect", "ARC-QA": "QA / Test Lead"},
    "science":     {"ARC-TH": "Theorist", "ARC-AD": "Skeptical Reviewer", "ARC-IM": "Experimentalist", "ARC-ST": "Principal Investigator", "ARC-QA": "Peer Reviewer"},
    "legal":       {"ARC-TH": "Legal Scholar", "ARC-AD": "Opposing Counsel", "ARC-IM": "Drafting Attorney", "ARC-ST": "General Counsel", "ARC-QA": "Compliance Officer"},
    "medicine":    {"ARC-TH": "Clinical Researcher", "ARC-AD": "Differential Skeptic", "ARC-IM": "Attending Physician", "ARC-ST": "Chief Medical Officer", "ARC-QA": "Safety Reviewer"},
    "finance":     {"ARC-TH": "Quant / Economist", "ARC-AD": "Short Seller", "ARC-IM": "Financial Analyst", "ARC-ST": "Portfolio Strategist", "ARC-QA": "Risk & Audit Officer"},
    "engineering": {"ARC-TH": "Design Theorist", "ARC-AD": "Failure-Mode Analyst", "ARC-IM": "Lead Engineer", "ARC-ST": "Systems Architect", "ARC-QA": "Reliability Engineer"},
    "business":    {"ARC-TH": "Strategy Theorist", "ARC-AD": "Devil's Advocate", "ARC-IM": "Operator", "ARC-ST": "Executive Strategist", "ARC-QA": "Diligence Reviewer"},
    "general":     {"ARC-TH": "Theorist", "ARC-AD": "Adversary", "ARC-IM": "Implementer", "ARC-ST": "Strategist", "ARC-QA": "Quality Reviewer"},
}

# Panel composition priority. Adversarial first — the Attack-Fix-Verify loop
# needs it. Security domains get a second adversary when the panel grows.
_PANEL_PRIORITY = ["ARC-AD", "ARC-TH", "ARC-IM", "ARC-QA", "ARC-ST", "ARC-AD", "ARC-TH"]


def compose_panel(domain: str, size: int) -> list[dict]:
    fam = domain_family(domain)
    size = max(3, min(7, size))
    panel = []
    for i in range(size):
        arc = _PANEL_PRIORITY[i]
        name, mode = ARCHETYPES[arc]
        panel.append({
            "archetype": arc,
            "mode": mode,
            "persona": _PERSONA[fam][arc],
            "role": "LEAD" if i == 0 else ("SYNTHESIZER" if arc == "ARC-ST" else "CONTRIBUTOR"),
        })
    return panel


# --------------------------------------------------------------------------
# The 6-stage pipeline — the forge itself.
# --------------------------------------------------------------------------

def build_pipeline(domain: str, panel: list[dict], chains: tuple[str, ...]) -> list[dict]:
    fam = domain_family(domain)
    return [
        {"stage": 1, "name": "DETECT",      "detail": f"domain = {domain} ({fam})"},
        {"stage": 2, "name": "CALIBRATE",   "detail": "factor model → precision, compute, panel size"},
        {"stage": 3, "name": "META-PROMPT", "detail": f"synthesize {len(panel)}-expert panel from archetypes × domain"},
        {"stage": 4, "name": "ELABORATE",   "detail": "draft → Attack-Fix-Verify → synthesize"},
        {"stage": 5, "name": "VERIFY",      "detail": f"{len(chains)} chains ({', '.join(chains)}) → dependency-aware consensus, early-exit"},
        {"stage": 6, "name": "RENDER",      "detail": "codified-output grammar, efficiency-tiered"},
    ]


# --------------------------------------------------------------------------
# Plan assembly
# --------------------------------------------------------------------------

@dataclass
class Plan:
    task: str
    domain: str
    precision_level: int
    precision_label: str
    confidence_target: float
    compute_type: str
    compute_desc: str
    aggregation: str
    verification_chains: list[str]
    expert_panel: list[dict]
    pipeline: list[dict]
    total_agents: int
    factors: dict
    calibration_reasons: list[str] = field(default_factory=list)


def plan(task: str,
         compute: str | None = None,
         precision: int | None = None,
         domain: str | None = None) -> Plan:
    c = cal.calibrate(task, domain=domain)
    pl = precision if precision is not None else c.final_pl
    if precision is not None:
        c.chains = cal.PL_CHAINS[pl]
        c.reasons.append(f"precision overridden by flag -> PL{pl}")

    compute_type = compute or auto_compute(task)
    panel_size = min(pl + 2, 7)
    panel = compose_panel(c.domain, panel_size)
    chains = list(c.chains)
    pipeline = build_pipeline(c.domain, panel, c.chains)

    return Plan(
        task=task,
        domain=c.domain,
        precision_level=pl,
        precision_label=cal.PL_LABEL[pl],
        confidence_target=cal.PL_CONFIDENCE_TARGET[pl],
        compute_type=compute_type,
        compute_desc=COMPUTE_TYPES[compute_type]["desc"],
        aggregation=COMPUTE_TYPES[compute_type]["agg"],
        verification_chains=chains,
        expert_panel=panel,
        pipeline=pipeline,
        total_agents=len(chains) + len(panel),
        factors=asdict(c.factors),
        calibration_reasons=c.reasons,
    )


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------

def render_human(p: Plan) -> str:
    bar = "═" * 72
    lines = [
        bar,
        f"  USF 8.0 REBORN · EXECUTION PLAN",
        bar,
        f"  vision        : {p.task[:60]}",
        f"  domain        : {p.domain}",
        f"  precision     : PL{p.precision_level}  [{p.precision_label}]  → {p.confidence_target:.1%} target",
        f"  compute       : {p.compute_type}  ({p.compute_desc})",
        f"  aggregation   : {p.aggregation}",
        f"  total agents  : {p.total_agents}  ({len(p.verification_chains)} chains + {len(p.expert_panel)} experts)",
        bar,
        "  EXPERT PANEL (meta-prompted from archetypes × domain)",
    ]
    for e in p.expert_panel:
        lines.append(f"    · {e['archetype']}  {e['persona']:<22} [{e['role']}]")
    lines.append(f"  VERIFICATION CHAINS : {', '.join(p.verification_chains)}")
    lines.append(bar)
    lines.append("  PIPELINE")
    for s in p.pipeline:
        lines.append(f"    [{s['stage']}] {s['name']:<11} {s['detail']}")
    lines.append(bar)
    return "\n".join(lines)


def render_interface() -> str:
    bar = "═" * 72
    out = [bar, "  USF 8.0 REBORN · CONTROL PANEL", bar, "", "  COMPUTE TYPES"]
    for name, meta in COMPUTE_TYPES.items():
        mark = "*" if name == "parallel" else "o"
        out.append(f"    {mark} {name:<12} {meta['desc']}")
    out += ["", "  PRECISION LEVELS  (chains · confidence target)"]
    for lvl in range(1, 6):
        mark = "*" if lvl == 3 else "o"
        out.append(f"    {mark} PL{lvl}  {len(cal.PL_CHAINS[lvl])} chains · {cal.PL_CONFIDENCE_TARGET[lvl]:.1%}  [{cal.PL_LABEL[lvl]}]")
    out += ["", "  MAGIC KEYWORDS   ultrathink→PL5 · think→PL2 · eco→PL1",
            "  ARCHETYPES       ARC-TH · ARC-AD · ARC-IM · ARC-ST · ARC-QA", "",
            "  USAGE   usf.py \"<vision>\" [--compute T] [--precision N] [--json]", bar]
    return "\n".join(out)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="usf", description="USF 8.0 REBORN planner")
    ap.add_argument("task", nargs="?", help="the vision / goal, any domain")
    ap.add_argument("--compute", choices=list(COMPUTE_TYPES), help="override compute type")
    ap.add_argument("--precision", type=int, choices=[1, 2, 3, 4, 5], help="override precision level")
    ap.add_argument("--domain", help="override detected domain (taxonomy key)")
    ap.add_argument("--json", action="store_true", help="emit machine-readable plan")
    ap.add_argument("--show-interface", action="store_true", help="show the control panel")
    args = ap.parse_args(argv)

    if args.show_interface:
        print(render_interface())
        return 0
    if not args.task:
        ap.error("a vision/task is required (or use --show-interface)")

    p = plan(args.task, compute=args.compute, precision=args.precision, domain=args.domain)
    print(json.dumps(asdict(p), indent=2) if args.json else render_human(p))
    return 0


if __name__ == "__main__":
    sys.exit(main())
