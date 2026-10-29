"""
Vampirize — the governed assimilation pipeline.

"Every modular aspect of USF can be built upon, improved, and accept outside
repos/research/content to be vampirized upon." This is that path, made safe.

An external source (repo / paper / content) is turned into candidate patterns,
each pinned with PROVENANCE, validated through the improvement-protocol gates,
and then either:

  * folded into an existing module automatically (TUNING within scope, subject to
    bootstrap phase), or
  * QUEUED for human Phase-1 approval if it expands capability scope (a cycle-4
    class event — the thing that breaks the convergence fixed point).

Built on the RAPTOR-CANNIBALIZATION methodology (extract strengths, reject
weaknesses) + PATTERN-PROVENANCE (pinned source, not HEAD) + capability_scope.
"""

import pathlib
import sys

_ENGINE = pathlib.Path(__file__).resolve().parent
for _p in (str(_ENGINE), str(_ENGINE / "evolution")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from dataclasses import dataclass, field

from module import ImprovementProposal, ModuleRegistry, Provenance
import bootstrap as bs
import capability_scope as cs
from oracle_meta import validate_proposal
from version_lineage import VersionLineage


@dataclass
class CandidatePattern:
    pattern_id: str
    description: str
    target_module: str              # module to fold into
    confidence: float               # extractor confidence 0..1
    risk: str = "LOW"               # LOW|MEDIUM|HIGH|CRITICAL
    adds_capabilities: frozenset = frozenset()   # non-empty => scope expansion


@dataclass
class ExternalSource:
    name: str
    url: str                        # pinned permalink, NOT HEAD
    kind: str                       # repo | paper | content
    patterns: list[CandidatePattern] = field(default_factory=list)


@dataclass
class VampirizeReport:
    source: str
    folded: list[str] = field(default_factory=list)       # auto-integrated
    queued_for_human: list[str] = field(default_factory=list)
    rejected: list[str] = field(default_factory=list)
    provenance: list[Provenance] = field(default_factory=list)

    def summary(self) -> str:
        return (f"vampirize '{self.source}': "
                f"{len(self.folded)} folded, {len(self.queued_for_human)} queued (human), "
                f"{len(self.rejected)} rejected")


# Minimum extractor confidence to even consider a pattern.
MIN_CONFIDENCE = 0.60


class VampirizePipeline:
    def __init__(self, registry: ModuleRegistry, lineage: VersionLineage,
                 phase: int = 2, trust: bs.Trust | None = None):
        self.reg = registry
        self.lin = lineage
        self.phase = phase
        self.trust = trust or bs.Trust(0.8, 0.8, 0.8, 0.8, 0.8)
        self.accepted_provenance: list[Provenance] = []
        self._clock = 0

    def _stamp(self) -> str:
        self._clock += 1
        return f"2026102901{self._clock:04d}"

    def ingest(self, source: ExternalSource, stamp_date: str = "2026-10-29") -> VampirizeReport:
        rep = VampirizeReport(source.name)

        for pat in source.patterns:
            # 1. confidence floor
            if pat.confidence < MIN_CONFIDENCE:
                rep.rejected.append(f"{pat.pattern_id}: confidence {pat.confidence:.2f} < {MIN_CONFIDENCE}")
                continue

            # 2. target must exist (or be an explicit new-capability module)
            try:
                target = self.reg.get(pat.target_module)
            except KeyError:
                if not pat.adds_capabilities:
                    rep.rejected.append(f"{pat.pattern_id}: unknown target '{pat.target_module}' and no new capability")
                    continue
                target = None

            # 3. improvement-protocol validation gates
            proposal = ImprovementProposal(
                source_agent="vampirize", target_module=pat.target_module,
                category="PROCESS" if not pat.adds_capabilities else "TAXONOMY",
                risk=pat.risk, description=f"vampirized: {pat.description}",
                adds_capabilities=pat.adds_capabilities)
            ok, why = validate_proposal(proposal)
            if not ok:
                rep.rejected.append(f"{pat.pattern_id}: failed gate ({why})")
                continue

            # 4. provenance — pin the source permalink, date, confidence
            prov = Provenance(source=source.url, ingested=stamp_date,
                              confidence=pat.confidence, note=pat.pattern_id)

            # 5. capability-scope gate + bootstrap approval
            decision = cs.scope_gate(proposal, self.reg)
            approval = bs.approve(proposal, self.phase, self.trust, decision.requires_human)

            if approval.route == "AUTO" and target is not None:
                target.improve(proposal)
                target.record_provenance(prov)
                self.accepted_provenance.append(prov)
                cur = self.lin.current() or {"version_id":
                    self.lin.genesis("3.0.0", self.reg.scope_hash(), self._stamp())}
                self.lin.create(cur["version_id"], self.reg.scope_hash(), self._stamp(),
                                "vampirize", proposal.description,
                                {"pattern": pat.pattern_id, "source": source.url})
                rep.folded.append(f"{pat.pattern_id} → {pat.target_module}")
                rep.provenance.append(prov)
            else:
                # scope expansion or non-auto risk → human queue (NOT integrated)
                rep.queued_for_human.append(
                    f"{pat.pattern_id} → {pat.target_module}  [{decision.kind}; {approval.route}]")
        return rep


if __name__ == "__main__":
    import verification
    from module import build_default_registry

    reg = build_default_registry()
    reg.register(verification.as_module())
    lin = VersionLineage()
    lin.genesis("3.0.0", reg.scope_hash(), "20261029000000")
    pipe = VampirizePipeline(reg, lin, phase=3)

    # A fictional external framework to cannibalize.
    src = ExternalSource(
        name="SuperClaude-Framework", kind="repo",
        url="https://github.com/example/superclaude/tree/a1b2c3d",  # pinned, not HEAD
        patterns=[
            CandidatePattern("SC-01", "token-budget heuristic for panels", "plan.planner", 0.82, "LOW"),
            CandidatePattern("SC-02", "stricter Sybil justification threshold", "verify.chains", 0.78, "MEDIUM"),
            CandidatePattern("SC-03", "whole new wetlab/bioinformatics domain", "domain.bioinformatics", 0.90, "HIGH",
                             adds_capabilities=frozenset({"domain.bioinformatics"})),
            CandidatePattern("SC-04", "half-baked idea", "plan.planner", 0.40, "LOW"),  # below confidence floor
        ])

    rep = pipe.ingest(src)
    print(rep.summary())
    print("  folded   :", rep.folded)
    print("  queued   :", rep.queued_for_human, "  (scope expansion → human Phase-1)")
    print("  rejected :", rep.rejected)
    print("  provenance pinned:", [f'{p.note}@{p.source.split("/")[-1]}' for p in rep.provenance])
    print("  scope hash (unchanged — expansion was NOT auto-applied):", reg.scope_hash())
