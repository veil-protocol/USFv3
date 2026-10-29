"""
Capability Scope — the fixed-point safety bound.

Bounded self-improvement converges to a stable fixed point ONLY while capability
scope stays constant (the paper's core claim; the "cycle-4 spike" is what happens
when it doesn't — absorbing 47 external patterns at once re-opened attack surface
and findings jumped 5 → 14).

So scope is an explicit, hashed, gated object. A proposal that merely TUNES within
the current scope may flow automatically (subject to bootstrap phase). A proposal
that EXPANDS scope (adds a capability / module / chain) always goes to the human
Phase-1 path and triggers a dedicated red-team cycle.
"""

import _bootpath  # noqa: F401  (sets up import path)

from dataclasses import dataclass, field

from module import ImprovementProposal, ModuleRegistry


# Capabilities that may never be removed (self-improvement invariants).
PROTECTED = frozenset({
    "evolution.meta_analysis", "evolution.rollback", "evolution.version_lineage",
    "governance.human_override", "governance.audit_log",
})

# How many newly-added capabilities in one event counts as a "spike" (cycle-4 class).
# The real cycle-4 event was 8 sources / 47 patterns; default here is deliberately low.
SCOPE_SPIKE_THRESHOLD = 3


@dataclass
class ScopeDecision:
    kind: str                      # TUNING | EXPANSION | REMOVAL_FORBIDDEN
    requires_human: bool
    risk_floor: str                # LOW | HIGH | CRITICAL
    added: tuple[str, ...] = ()
    removed: tuple[str, ...] = ()
    reasons: list[str] = field(default_factory=list)

    @property
    def allowed_automatically(self) -> bool:
        return self.kind == "TUNING" and not self.requires_human


def scope_gate(proposal: ImprovementProposal, registry: ModuleRegistry) -> ScopeDecision:
    """Classify a proposal's effect on capability scope and gate accordingly."""
    current = registry.capability_scope()
    added = tuple(sorted(set(proposal.adds_capabilities) - set(current)))
    reasons: list[str] = []

    # Invariant: protected capabilities cannot be removed. (Proposals don't carry
    # removals explicitly here; a META proposal touching protected caps is caught.)
    if proposal.category == "META" and proposal.target_module.startswith("evolution"):
        if proposal.adds_capabilities & PROTECTED:
            pass  # adding is fine; removal is what's forbidden (handled by registry invariants)

    if not added:
        reasons.append("no new capabilities → TUNING cycle (converges within scope)")
        # Even tuning is gated by risk: CRITICAL/META always need a human.
        human = proposal.risk == "CRITICAL" or proposal.category == "META"
        if human:
            reasons.append(f"{proposal.category}/{proposal.risk} forces human review")
        return ScopeDecision("TUNING", human, proposal.risk, reasons=reasons)

    # --- EXPANSION: a cycle-4-class event ---
    reasons.append(f"adds {len(added)} capabilities → SCOPE EXPANSION (leaves the fixed point)")
    risk = "CRITICAL" if len(added) >= SCOPE_SPIKE_THRESHOLD else "HIGH"
    if len(added) >= SCOPE_SPIKE_THRESHOLD:
        reasons.append(f"bulk expansion (≥{SCOPE_SPIKE_THRESHOLD}) → CRITICAL + dedicated red-team cycle required")
    reasons.append("expansion always takes the human Phase-1 path, regardless of bootstrap phase")
    return ScopeDecision("EXPANSION", True, risk, added=added, reasons=reasons)


def scope_hash(registry: ModuleRegistry) -> str:
    return registry.scope_hash()


if __name__ == "__main__":
    import verification
    from module import build_default_registry

    reg = build_default_registry()
    reg.register(verification.as_module())
    print("current scope hash:", scope_hash(reg))

    tune = ImprovementProposal("MAL-EFFICIENCY", "plan.planner", "PRECISION", "LOW",
                               "retune panel-size heuristic")
    exp = ImprovementProposal("MAL-COVERAGE", "vampirize", "TAXONOMY", "MEDIUM",
                              "absorb an external domain module",
                              adds_capabilities=frozenset({"domain.bioinformatics",
                                                           "template.bioinformatics",
                                                           "archetype.wetlab"}))
    for p in (tune, exp):
        d = scope_gate(p, reg)
        print(f"\n[{p.target_module}] -> {d.kind}  human={d.requires_human}  risk={d.risk_floor}")
        for r in d.reasons:
            print("   -", r)
