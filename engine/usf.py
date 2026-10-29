#!/usr/bin/env python3
"""
USF v3 REBORN — Planner
========================

The front door of the forge. Turns a vision (any domain) into a configured,
staged execution plan: execution profile, compute type, Precision Level, a
synthesized expert panel, verification depth, model tier, and the 6-stage
pipeline that elaborates a seed into a finished product.

This is the wired version of the "beautiful USF" planning dashboard: the
calibrator (calibrator.py) is a real dependency, not a keyword regex stub. Every
knob below is both PARSED (a CLI flag) and SHOWN (--show-interface + the plan).

    python3 usf.py "audit the key-exchange in our auth service"
    python3 usf.py "deep research report on X" --precision 4 --profile supervised --json
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
# Execution profiles — the "execution type": how much the forge checks in.
# --------------------------------------------------------------------------

PROFILES: dict[str, str] = {
    "interactive":     "confirm every step with the user",
    "supervised":      "confirm major steps; auto-run minor ones",
    "autonomous":      "run to completion, then report (default)",
    "fire_and_forget": "run async; deliver the product when done",
}

# --------------------------------------------------------------------------
# Model tiers — which model each run routes to.
# --------------------------------------------------------------------------

MODEL_TIERS: dict[str, str] = {
    "opus":   "deepest reasoning — security / high-stakes / PL4+",
    "sonnet": "balanced default",
    "haiku":  "fast / routine / PL1",
}


def auto_model(task: str, pl: int, domain: str) -> str:
    t = task.lower()
    if pl >= 4 or domain.startswith("T.SEC") or any(w in t for w in
                                                    ("critical", "nation-state", "safety")):
        return "opus"
    if pl <= 1 or any(w in t for w in ("quick", "simple", "eco", "trivial", "basic")):
        return "haiku"
    return "sonnet"


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

# The domains USF adapts to (family → one-line).
DOMAINS: dict[str, str] = {
    "security":    "vuln research, detection, red/blue",
    "software":    "code, systems, AI/ML",
    "science":     "research, experiment, theory",
    "legal":       "contracts, compliance, regulation",
    "medicine":    "clinical, diagnostic, safety-critical",
    "finance":     "markets, valuation, risk/audit",
    "engineering": "design, failure analysis, reliability",
    "business":    "strategy, product, operations",
    "general":     "anything else (domain-agnostic)",
}


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

_PANEL_PRIORITY = ["ARC-AD", "ARC-TH", "ARC-IM", "ARC-QA", "ARC-ST", "ARC-AD", "ARC-TH"]


def compose_panel(domain: str, size: int) -> list[dict]:
    fam = domain_family(domain)
    size = max(3, min(7, size))
    panel = []
    for i in range(size):
        arc = _PANEL_PRIORITY[i]
        name, mode = ARCHETYPES[arc]
        panel.append({
            "archetype": arc, "mode": mode, "persona": _PERSONA[fam][arc],
            "role": "LEAD" if i == 0 else ("SYNTHESIZER" if arc == "ARC-ST" else "CONTRIBUTOR"),
        })
    return panel


# --------------------------------------------------------------------------
# Verification chain legend (from the verification module; fallback inline).
# --------------------------------------------------------------------------

def chain_legend() -> list[tuple[str, str]]:
    try:
        import verification as v
        return [(k, v.CHAINS[k].name) for k in sorted(v.CHAINS)]
    except Exception:
        return [("A", "Static"), ("B", "Dynamic"), ("C", "Formal"), ("D", "Empirical"),
                ("E", "Expert Review"), ("F", "Test-Driven"), ("G", "Code Review"),
                ("H", "Debug"), ("I", "Runtime Env")]


# --------------------------------------------------------------------------
# The 6-stage pipeline — the forge itself.
# --------------------------------------------------------------------------

def build_pipeline(domain: str, panel: list[dict], chains: tuple[str, ...]) -> list[dict]:
    fam = domain_family(domain)
    meta = (f"synthesize {len(panel)}-expert panel from archetypes × domain"
            if panel else "chains-only (panel disabled)")
    return [
        {"stage": 1, "name": "DETECT",      "detail": f"domain = {domain} ({fam})"},
        {"stage": 2, "name": "CALIBRATE",   "detail": "factor model → precision, compute, panel size"},
        {"stage": 3, "name": "META-PROMPT", "detail": meta},
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
    profile: str
    profile_desc: str
    model: str
    use_archetypes: bool
    verification_chains: list[str]
    expert_panel: list[dict]
    pipeline: list[dict]
    total_agents: int
    factors: dict
    calibration_reasons: list[str] = field(default_factory=list)


def plan(task: str,
         compute: str | None = None,
         precision: int | None = None,
         domain: str | None = None,
         profile: str = "autonomous",
         model: str | None = None,
         use_archetypes: bool = True) -> Plan:
    c = cal.calibrate(task, domain=domain)
    pl = precision if precision is not None else c.final_pl
    if precision is not None:
        c.chains = cal.PL_CHAINS[pl]
        c.reasons.append(f"precision overridden by flag -> PL{pl}")

    compute_type = compute or auto_compute(task)
    panel = compose_panel(c.domain, min(pl + 2, 7)) if use_archetypes else []
    chains = list(c.chains)
    model = model or auto_model(task, pl, c.domain)

    return Plan(
        task=task, domain=c.domain,
        precision_level=pl, precision_label=cal.PL_LABEL[pl],
        confidence_target=cal.PL_CONFIDENCE_TARGET[pl],
        compute_type=compute_type, compute_desc=COMPUTE_TYPES[compute_type]["desc"],
        aggregation=COMPUTE_TYPES[compute_type]["agg"],
        profile=profile, profile_desc=PROFILES[profile],
        model=model, use_archetypes=use_archetypes,
        verification_chains=chains, expert_panel=panel,
        pipeline=build_pipeline(c.domain, panel, c.chains),
        total_agents=len(chains) + len(panel),
        factors=asdict(c.factors), calibration_reasons=c.reasons,
    )


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------

def render_human(p: Plan) -> str:
    bar = "═" * 72
    lines = [
        bar, "  USF v3 REBORN · EXECUTION PLAN", bar,
        f"  vision        : {p.task[:60]}",
        f"  domain        : {p.domain}  ({domain_family(p.domain)})",
        f"  precision     : PL{p.precision_level}  [{p.precision_label}]  → {p.confidence_target:.1%} target",
        f"  compute       : {p.compute_type}  ({p.compute_desc})",
        f"  aggregation   : {p.aggregation}",
        f"  profile       : {p.profile}  ({p.profile_desc})",
        f"  model tier    : {p.model}",
        f"  archetypes    : {'on' if p.use_archetypes else 'off (chains only)'}",
        f"  total agents  : {p.total_agents}  ({len(p.verification_chains)} chains + {len(p.expert_panel)} experts)",
        bar, "  EXPERT PANEL (meta-prompted from archetypes × domain)",
    ]
    for e in p.expert_panel:
        lines.append(f"    · {e['archetype']}  {e['persona']:<22} [{e['role']}]")
    if not p.expert_panel:
        lines.append("    (disabled — verification chains only)")
    lines.append(f"  VERIFICATION CHAINS : {', '.join(p.verification_chains)}")
    lines += [bar, "  PIPELINE"]
    for s in p.pipeline:
        lines.append(f"    [{s['stage']}] {s['name']:<11} {s['detail']}")
    lines.append(bar)
    return "\n".join(lines)


def render_interface() -> str:
    bar = "═" * 72
    out = [bar, "  USF v3 REBORN · CONTROL PANEL  (every knob is parsed + shown)", bar]

    out += ["", "  EXECUTION PROFILES  (--profile)"]
    for name, desc in PROFILES.items():
        out.append(f"    {'*' if name == 'autonomous' else 'o'} {name:<16} {desc}")

    out += ["", "  COMPUTE TYPES  (--compute)"]
    for name, meta in COMPUTE_TYPES.items():
        out.append(f"    {'*' if name == 'parallel' else 'o'} {name:<12} {meta['desc']}  → {meta['agg']}")

    out += ["", "  PRECISION LEVELS  (--precision · chains · confidence)"]
    for lvl in range(1, 6):
        out.append(f"    {'*' if lvl == 3 else 'o'} PL{lvl}  {len(cal.PL_CHAINS[lvl])} chains · "
                   f"{cal.PL_CONFIDENCE_TARGET[lvl]:.1%}  [{cal.PL_LABEL[lvl]}]")

    out += ["", "  VERIFICATION CHAINS  (selected by precision)"]
    legend = chain_legend()
    out.append("    " + " · ".join(f"{k}:{n}" for k, n in legend[:5]))
    if len(legend) > 5:
        out.append("    " + " · ".join(f"{k}:{n}" for k, n in legend[5:]))

    out += ["", "  MODEL TIERS  (--model; auto by default)"]
    for name, desc in MODEL_TIERS.items():
        out.append(f"    o {name:<7} {desc}")

    out += ["", "  DOMAINS  (auto-detected; --domain to override)"]
    for name, desc in DOMAINS.items():
        out.append(f"    o {name:<12} {desc}")

    out += ["", "  EXPERT ARCHETYPES  (--no-archetypes to disable the panel)"]
    for aid, (nm, mode) in ARCHETYPES.items():
        out.append(f"    o {aid}  {nm:<16} {mode}")

    out += ["", "  MAGIC KEYWORDS   ultrathink→PL5 · think→PL2 · eco→PL1",
            "",
            "  PIPELINE   DETECT → CALIBRATE → META-PROMPT → ELABORATE → VERIFY → RENDER",
            "",
            "  USAGE   usf.py \"<vision>\" [--precision N] [--compute T] [--profile P]",
            "                        [--model M] [--domain D] [--no-archetypes] [--json]",
            bar]
    return "\n".join(out)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="usf", description="USF v3 REBORN planner")
    ap.add_argument("task", nargs="?", help="the vision / goal, any domain")
    ap.add_argument("--precision", type=int, choices=[1, 2, 3, 4, 5], help="override precision level (PL)")
    ap.add_argument("--compute", choices=list(COMPUTE_TYPES), help="override compute type")
    ap.add_argument("--profile", choices=list(PROFILES), default="autonomous", help="execution profile")
    ap.add_argument("--model", choices=list(MODEL_TIERS), help="model tier (auto by default)")
    ap.add_argument("--domain", help="override detected domain (taxonomy key, e.g. T.SEC)")
    ap.add_argument("--no-archetypes", action="store_true", help="run verification chains only, no panel")
    ap.add_argument("--json", action="store_true", help="emit machine-readable plan")
    ap.add_argument("--show-interface", action="store_true", help="show the full control panel")
    args = ap.parse_args(argv)

    if args.show_interface:
        print(render_interface())
        return 0
    if not args.task:
        ap.error("a vision/task is required (or use --show-interface)")

    p = plan(args.task, compute=args.compute, precision=args.precision, domain=args.domain,
             profile=args.profile, model=args.model, use_archetypes=not args.no_archetypes)
    print(json.dumps(asdict(p), indent=2) if args.json else render_human(p))
    return 0


if __name__ == "__main__":
    sys.exit(main())
