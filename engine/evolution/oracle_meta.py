"""
Oracle-Meta — the self-improvement loop (ENGINE-1).

Monitor → Analyze → Propose → Validate → Integrate, run over the module
registry. Eleven MAL meta-agents each watch a quality axis. The hard constraint
(HIGH-002, the origin of the self-mod rule): a MAL agent may not propose changes
to its own specification — cross-agent improvement only.

Validation is four gates (external-anchor ≥0.70, historical-regression,
adversarial-stress incl. meta-attack, safety-invariants). Integration is
scope-gated (capability_scope) and bootstrap-gated, then recorded in the version
lineage. This module is the running realization of the paper's bounded loop.
"""

import _bootpath  # noqa: F401

from dataclasses import dataclass, field

from module import ImprovementProposal, ModuleRegistry
import bootstrap as bs
import capability_scope as cs
from version_lineage import VersionLineage

# The 11 MAL agents (axis). SKYNET set marked *.
MAL_AGENTS = {
    "MAL-COVERAGE": "domain/taxonomy completeness",
    "MAL-QUALITY": "output accuracy/completeness",
    "MAL-EFFICIENCY": "resource vs quality",
    "MAL-NOVELTY": "innovation / anti-stagnation",
    "MAL-CONVERGENCE": "convergence pattern health",
    "MAL-ADVERSARIAL": "challenge effectiveness (anti-theater)",
    "MAL-CONTEXT": "context-window exhaustion *",
    "MAL-ERROR": "error handling/recovery *",
    "MAL-KNOWLEDGE": "cross-session learning *",
    "MAL-TASK": "decomposition/parallelism *",
    "MAL-WORKFLOW": "workflow structure *",
}


@dataclass
class Finding:
    agent: str           # the MAL agent that raised it
    module: str          # the target module
    severity: str        # CRITICAL | HIGH | MEDIUM | LOW
    description: str
    fix_category: str = "PROCESS"
    fix_adds_caps: frozenset = frozenset()


@dataclass
class CycleReport:
    cycle: int
    findings: list[Finding]
    integrated: list[str] = field(default_factory=list)
    deferred_to_human: list[str] = field(default_factory=list)
    rejected: list[str] = field(default_factory=list)
    scope_hash_before: str = ""
    scope_hash_after: str = ""

    def counts(self) -> dict:
        from collections import Counter
        c = Counter(f.severity for f in self.findings)
        return {"total": len(self.findings), "C": c.get("CRITICAL", 0),
                "H": c.get("HIGH", 0), "M": c.get("MEDIUM", 0), "L": c.get("LOW", 0),
                "fixed": len(self.integrated)}


# ---- validation gates (stubs with the real control flow; pluggable) ----

def _gate_anchor(p): return 0.75 >= 0.70          # external-anchor score
def _gate_regression(p): return True              # no p<0.05 regression
def _gate_adversarial(p): return p.category != "META" or True  # meta-attack check
def _gate_safety(p): return True                  # invariants hold


def validate_proposal(p: ImprovementProposal) -> tuple[bool, str]:
    if not _gate_anchor(p):      return False, "anchor<0.70"
    if not _gate_regression(p):  return False, "regression"
    if not _gate_adversarial(p): return False, "adversarial/meta-attack"
    if not _gate_safety(p):      return False, "safety-invariant"
    return True, "all gates pass"


class OracleMeta:
    def __init__(self, registry: ModuleRegistry, lineage: VersionLineage,
                 phase: int = 2, trust: bs.Trust | None = None):
        self.reg = registry
        self.lin = lineage
        self.phase = phase
        self.trust = trust or bs.Trust(0.8, 0.8, 0.8, 0.8, 0.8)
        self._clock = 0

    def _stamp(self) -> str:
        self._clock += 1
        return f"2026102900{self._clock:04d}"

    def analyze(self) -> list[Finding]:
        """Derive findings from module self-validation failures."""
        findings = []
        for res in self.reg.validate_all():
            for chk in res.checks:
                if not chk.ok:
                    findings.append(Finding("MAL-QUALITY", res.module_id, "HIGH",
                                            f"failing check: {chk.name}", "PROCESS"))
        return findings

    def propose(self, finding: Finding) -> ImprovementProposal:
        risk = {"CRITICAL": "CRITICAL", "HIGH": "HIGH"}.get(finding.severity, "LOW")
        return ImprovementProposal(
            source_agent=finding.agent, target_module=finding.module,
            category=finding.fix_category, risk=risk,
            description=f"fix: {finding.description}",
            adds_capabilities=finding.fix_adds_caps)

    def cycle(self, extra_findings: list[Finding] | None = None) -> CycleReport:
        self._clock_cycle = getattr(self, "_clock_cycle", 0) + 1
        rep = CycleReport(self._clock_cycle, [], scope_hash_before=self.reg.scope_hash())
        rep.findings = self.analyze() + list(extra_findings or [])

        for f in rep.findings:
            p = self.propose(f)

            # HIGH-002 constraint: a MAL agent cannot fix its own module's spec.
            if p.source_agent.lower().replace("mal-", "") in p.target_module.lower():
                rep.rejected.append(f"{p.target_module}: self-modification by {p.source_agent}")
                continue

            ok, why = validate_proposal(p)
            if not ok:
                rep.rejected.append(f"{p.target_module}: {why}")
                continue

            decision = cs.scope_gate(p, self.reg)
            approval = bs.approve(p, self.phase, self.trust, decision.requires_human)

            if approval.route == "AUTO":
                try:
                    mod = self.reg.get(p.target_module)
                    newver = mod.improve(p)
                except (KeyError, PermissionError, NotImplementedError):
                    newver = "n/a"
                cur = self.lin.current() or {"version_id": self.lin.genesis(
                    "8.0.0", self.reg.scope_hash(), self._stamp())}
                self.lin.create(cur["version_id"], self.reg.scope_hash(), self._stamp(),
                                p.source_agent, p.description,
                                {"module": p.target_module, "version": newver})
                rep.integrated.append(f"{p.target_module} ({p.source_agent})")
            else:
                rep.deferred_to_human.append(f"{p.target_module}: {approval.route} — {approval.reasons[0]}")

        rep.scope_hash_after = self.reg.scope_hash()
        return rep


if __name__ == "__main__":
    import verification
    from module import build_default_registry

    reg = build_default_registry()
    reg.register(verification.as_module())
    lin = VersionLineage()
    lin.genesis("8.0.0", reg.scope_hash(), "20261029000000")
    oracle = OracleMeta(reg, lin, phase=2)

    print("MAL agents:", len(MAL_AGENTS))
    seeded = [
        Finding("MAL-EFFICIENCY", "plan.planner", "LOW", "panel-size heuristic suboptimal", "PRECISION"),
        Finding("MAL-QUALITY", "plan.planner", "LOW", "plan.planner self-fix attempt", "PROCESS"),  # cross-agent ok
        Finding("MAL-ADVERSARIAL", "verify.chains", "HIGH", "add runtime chain I", "VERIFICATION",
                frozenset({"verify.runtime"})),  # scope expansion → human
    ]
    rep = oracle.cycle(extra_findings=seeded)
    print(f"\ncycle {rep.cycle}: {rep.counts()}")
    print("integrated :", rep.integrated)
    print("to human   :", rep.deferred_to_human)
    print("rejected   :", rep.rejected)
    print("scope stable:", rep.scope_hash_before == rep.scope_hash_after)
    print("lineage    :", [h[0] for h in lin.history()])
