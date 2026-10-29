"""
Bootstrap — graduated-autonomy ladder.

The system earns autonomy over cycles. Early on a human approves everything;
later, low-risk tuning auto-approves while high-risk and all scope-expansion stay
human-gated. CRITICAL and META are human-gated in every phase, forever.
"""

import _bootpath  # noqa: F401

from dataclasses import dataclass

from module import ImprovementProposal

PHASES = {
    1: {"name": "Full Human Oversight",     "auto": set()},
    2: {"name": "Risk-Stratified",          "auto": {"LOW"}},
    3: {"name": "Exception-Based",          "auto": {"LOW", "MEDIUM"}},
    4: {"name": "Autonomous w/ Safeguards", "auto": {"LOW", "MEDIUM", "HIGH"}},
}

# Never auto, any phase.
ALWAYS_HUMAN_RISK = {"CRITICAL"}
ALWAYS_HUMAN_CATEGORY = {"META"}


@dataclass
class Trust:
    improvement_success: float = 0.5
    validation_accuracy: float = 0.5
    stability: float = 0.5
    calibration: float = 0.5
    anomaly_absence: float = 0.5

    def score(self) -> float:
        return (0.25 * self.improvement_success + 0.25 * self.validation_accuracy
                + 0.20 * self.stability + 0.15 * self.calibration
                + 0.15 * self.anomaly_absence)


@dataclass
class ApprovalDecision:
    route: str          # AUTO | SPOT_CHECK | HUMAN_REQUIRED
    reasons: list[str]


def approve(proposal: ImprovementProposal, phase: int, trust: Trust,
            scope_requires_human: bool) -> ApprovalDecision:
    reasons = []
    if scope_requires_human:
        return ApprovalDecision("HUMAN_REQUIRED", ["capability-scope expansion (Phase-1 path)"])
    if proposal.risk in ALWAYS_HUMAN_RISK:
        return ApprovalDecision("HUMAN_REQUIRED", [f"{proposal.risk} risk is always human-gated"])
    if proposal.category in ALWAYS_HUMAN_CATEGORY:
        return ApprovalDecision("HUMAN_REQUIRED", [f"{proposal.category} category is always human-gated"])

    auto = PHASES[phase]["auto"]
    if proposal.risk in auto:
        if trust.score() < 0.5:
            return ApprovalDecision("SPOT_CHECK", [f"phase {phase} auto, but trust {trust.score():.2f} < 0.5"])
        reasons.append(f"phase {phase} ({PHASES[phase]['name']}) auto-approves {proposal.risk}")
        return ApprovalDecision("AUTO", reasons)
    return ApprovalDecision("HUMAN_REQUIRED",
                            [f"phase {phase} does not auto-approve {proposal.risk}"])


if __name__ == "__main__":
    t = Trust(0.9, 0.9, 0.9, 0.8, 0.9)
    print("trust score:", round(t.score(), 3))
    cases = [
        ("phase2 LOW tune",  ImprovementProposal("MAL-EFFICIENCY", "plan.planner", "PRECISION", "LOW", "x"), 2, False),
        ("phase2 HIGH",      ImprovementProposal("MAL-QUALITY", "verify.chains", "VERIFICATION", "HIGH", "x"), 2, False),
        ("phase4 HIGH",      ImprovementProposal("MAL-QUALITY", "verify.chains", "VERIFICATION", "HIGH", "x"), 4, False),
        ("any CRITICAL",     ImprovementProposal("MAL-ADVERSARIAL", "verify.chains", "VERIFICATION", "CRITICAL", "x"), 4, False),
        ("META always",      ImprovementProposal("MAL-COVERAGE", "evolution.oracle", "META", "LOW", "x"), 4, False),
        ("scope expansion",  ImprovementProposal("MAL-COVERAGE", "vampirize", "TAXONOMY", "HIGH", "x", adds_capabilities=frozenset({"domain.new"})), 4, True),
    ]
    for label, p, phase, scope_human in cases:
        d = approve(p, phase, t, scope_human)
        print(f"  {label:<18} -> {d.route}   ({d.reasons[0]})")
