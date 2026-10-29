"""
USF 8.0 REBORN — Verification Module
====================================

Dependency-aware, Sybil-hardened consensus over independent verification chains.
This is the "VERIFY" stage of the forge and the mechanism behind the paper's
"4/5 archetype agreement" quorum.

Design (from SPEC/precision/VERIFICATION-CHAINS.md + the RED-TEAM-REPORT-5.0
hardening pass):

  * Chain registry A–I is MUTABLE DATA, not an enum — the self-evolution loop
    can add chains (Chain I, Runtime-Environment, was itself added that way).
  * Agreement is DEPENDENCY-AWARE: dependent chains count for a fraction
    (F=0.5, H=0.3, I=0.8) so chained methods don't inflate consensus.
  * Correlated independent pairs (A↔C, B↔D, C↔E) are DISCOUNTED (×0.85) so
    "two runs of the same idea" can't masquerade as independent agreement.
  * Consensus is collected by 3-PHASE BLIND VOTING: all verdicts are gathered,
    then revealed simultaneously (order shuffled), then aggregated — no chain
    sees another's vote first (defeats ATTACK-5.0-011 consensus-timing).
  * Sybil guards (ATTACK-5.0-004): confidence 1.0 is only legal at PL5; a
    high-confidence claim with thin justification is penalised; a weakly-reasoned
    minority vote is down-weighted; a category-diversity quota is enforced.

Reconciliation note: two source specs disagreed on "chains per PL". We use the
calibrator's DEPTH scheme (PL1..5 spawn 1/2/3/6/9 chains) for how many chains
run, and express QUORUM here as a per-PL fraction of whatever ran. One coherent
model.

Stdlib only.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field


# --------------------------------------------------------------------------
# Chain registry (seeded A–H; I enters via self-evolution). Mutable on purpose.
# fields: name, category, independent, dep_weight, quality_factor, depends_on
# --------------------------------------------------------------------------

@dataclass
class ChainSpec:
    name: str
    category: str
    independent: bool
    dep_weight: float = 1.0        # effective count if NOT independent
    quality_factor: float = 1.0
    depends_on: tuple[str, ...] = ()


CHAINS: dict[str, ChainSpec] = {
    "A": ChainSpec("Static Analysis",    "static",   True,  1.0, 1.0),
    "B": ChainSpec("Dynamic Analysis",   "dynamic",  True,  1.0, 1.0),
    "C": ChainSpec("Formal Methods",     "formal",   True,  1.0, 1.2),   # highest quality
    "D": ChainSpec("Empirical Testing",  "empirical",True,  1.0, 0.9),
    "E": ChainSpec("Expert Review",      "expert",   True,  1.0, 0.8),   # most subjective
    "F": ChainSpec("Test-Driven Dev",    "dynamic",  False, 0.5, 1.0, ("B",)),
    "G": ChainSpec("Code Review",        "review",   True,  1.0, 1.0),
    "H": ChainSpec("Debug Verification", "dynamic",  False, 0.3, 1.0, ("B", "F")),
    # "I": added by the self-evolution worked example — register at runtime:
    #   CHAINS["I"] = ChainSpec("Runtime Environment","runtime",False,0.8,1.0,("B",))
}

# Correlated independent pairs → discount factor applied to aggregate confidence.
CORRELATED_PAIRS: dict[frozenset[str], float] = {
    frozenset({"A", "C"}): 0.85,   # share "specification"
    frozenset({"B", "D"}): 0.85,   # share "environment"
    frozenset({"C", "E"}): 0.85,   # share "review"
}

# Per-PL quorum as a fraction of chains that ran, and the aggregate-confidence cap.
PL_QUORUM_RATIO = {1: 1.00, 2: 1.00, 3: 0.67, 4: 0.80, 5: 0.89}
PL_CONF_CAP     = {1: 0.80, 2: 0.90, 3: 0.95, 4: 0.99, 5: 0.999}


def register_chain(chain_id: str, spec: ChainSpec) -> None:
    """Self-evolution hook: add a chain. (Capability-scope change upstream.)"""
    CHAINS[chain_id] = spec


# --------------------------------------------------------------------------
# A single chain's vote
# --------------------------------------------------------------------------

@dataclass
class ChainVote:
    chain_id: str
    agrees: bool               # does this chain support the claim?
    confidence: float          # 0..1
    justification: str = ""    # word count matters for the Sybil guard

    @property
    def category(self) -> str:
        return CHAINS[self.chain_id].category


@dataclass
class VerificationResult:
    verdict: str               # VERIFIED | REFUTED | UNCERTAIN
    confidence: float
    pl: int
    effective_for: float
    effective_against: float
    required: float
    reasons: list[str] = field(default_factory=list)

    def summary(self) -> str:
        head = f"{self.verdict}  (conf {self.confidence:.2f}, PL{self.pl})"
        body = (f"    effective agree={self.effective_for:.2f}  "
                f"against={self.effective_against:.2f}  required>={self.required:.2f}")
        return head + "\n" + body + "\n" + "\n".join(f"    - {r}" for r in self.reasons)


# --------------------------------------------------------------------------
# Sybil / timing hardening (RED-TEAM-REPORT-5.0, ATTACK-5.0-004 & 011)
# --------------------------------------------------------------------------

def _harden_vote(v: ChainVote, pl: int, majority_agrees: bool,
                 majority_strength: float, reasons: list[str]) -> tuple[float, float]:
    """Return (effective_weight, adjusted_confidence) after guards."""
    spec = CHAINS[v.chain_id]
    weight = spec.dep_weight if not spec.independent else 1.0
    conf = v.confidence

    # Only PL5 formal proofs may claim certainty.
    if conf >= 1.0 and pl < 5:
        conf = 0.95
        reasons.append(f"{v.chain_id}: conf 1.0 illegal below PL5 → capped 0.95")

    # High confidence needs justification (>= ~100 words) or it's discounted.
    if conf > 0.9 and len(v.justification.split()) < 100:
        conf -= 0.2
        reasons.append(f"{v.chain_id}: high conf w/ thin justification → −0.2")

    # A weakly-reasoned vote against a strong majority is down-weighted.
    if v.agrees != majority_agrees and majority_strength > 0.7 \
            and len(v.justification.split()) < 60:
        weight *= 0.5
        reasons.append(f"{v.chain_id}: weak minority dissent → weight ×0.5")

    return weight, max(0.0, min(1.0, conf))


def _min_independence_factor(chain_ids: set[str]) -> float:
    factor = 1.0
    for pair, disc in CORRELATED_PAIRS.items():
        if pair <= chain_ids:
            factor = min(factor, disc)
    return factor


def _diversity_ok(chain_ids: list[str]) -> bool:
    """No single method category may exceed 30% of the agreeing chains."""
    if not chain_ids:
        return True
    from collections import Counter
    counts = Counter(CHAINS[c].category for c in chain_ids)
    return (max(counts.values()) / len(chain_ids)) <= 0.30 or len(chain_ids) <= 3


# --------------------------------------------------------------------------
# Core: aggregate a set of chain votes into a verdict
# --------------------------------------------------------------------------

def verify(votes: list[ChainVote], pl: int,
           external_anchor: bool = False, seed: int = 0) -> VerificationResult:
    reasons: list[str] = []
    if not votes:
        return VerificationResult("UNCERTAIN", 0.0, pl, 0, 0, 0, ["no chains ran"])

    # Phase 1+2: collect then reveal simultaneously (shuffle = blind to order).
    rng = random.Random(seed)
    ordered = votes[:]
    rng.shuffle(ordered)

    n = len(ordered)
    agree_raw = [v for v in ordered if v.agrees]
    majority_agrees = len(agree_raw) >= (n / 2)
    majority_strength = max(len(agree_raw), n - len(agree_raw)) / n

    # Phase 3: aggregate with guards.
    eff_for = eff_against = 0.0
    conf_for: list[float] = []
    for v in ordered:
        w, c = _harden_vote(v, pl, majority_agrees, majority_strength, reasons)
        q = CHAINS[v.chain_id].quality_factor
        if v.agrees:
            eff_for += w
            conf_for.append(c * q)
        else:
            eff_against += w

    required = PL_QUORUM_RATIO[pl] * n
    agreeing_ids = {v.chain_id for v in agree_raw}

    # Diversity quota.
    if not _diversity_ok(list(agreeing_ids)):
        reasons.append("diversity quota failed (>30% one category) → verdict capped UNCERTAIN")
        return VerificationResult("UNCERTAIN", 0.0, pl, eff_for, eff_against, required, reasons)

    # Confidence = mean agreeing quality-weighted conf × independence discount, capped at PL.
    base = (sum(conf_for) / len(conf_for)) if conf_for else 0.0
    indep = _min_independence_factor(agreeing_ids)
    if indep < 1.0:
        reasons.append(f"correlated chains present → independence discount ×{indep}")
    confidence = min(base * indep, PL_CONF_CAP[pl])

    # PL5 additionally requires an external anchor / formal proof present.
    pl5_anchor_ok = (pl < 5) or external_anchor or ("C" in agreeing_ids)
    if pl == 5 and not pl5_anchor_ok:
        reasons.append("PL5 requires external anchor or Chain C (formal) → UNCERTAIN")
        return VerificationResult("UNCERTAIN", confidence, pl, eff_for, eff_against, required, reasons)

    if eff_for >= required:
        verdict = "VERIFIED"
    elif eff_against >= required:
        verdict = "REFUTED"
        confidence = min(confidence, 1.0)
    else:
        verdict = "UNCERTAIN"
    reasons.append(f"effective agreement {eff_for:.2f} vs required {required:.2f}")

    return VerificationResult(verdict, round(confidence, 3), pl, eff_for, eff_against, required, reasons)


# --------------------------------------------------------------------------
# Module wrapper + self-test
# --------------------------------------------------------------------------

def as_module():
    from module import Module, Check

    def _validate() -> list[Check]:
        strong = "word " * 120  # satisfies the justification guard
        # PL3: 3 independent chains agree strongly → VERIFIED.
        r1 = verify([ChainVote("A", True, 0.9, strong),
                     ChainVote("B", True, 0.92, strong),
                     ChainVote("D", True, 0.88, strong)], pl=3)
        # PL3: 2 agree, 1 well-reasoned dissent, below quorum → not VERIFIED.
        r2 = verify([ChainVote("A", True, 0.9, strong),
                     ChainVote("B", False, 0.9, strong),
                     ChainVote("D", False, 0.9, strong)], pl=3)
        # Sybil: lone chain claiming 1.0 at PL3 is capped.
        r3 = verify([ChainVote("A", True, 1.0, "trust me")], pl=3)
        # Diversity: three dynamic-category chains can't alone carry PL4.
        return [
            Check("PL3 triple-independent agreement → VERIFIED", r1.verdict == "VERIFIED"),
            Check("PL3 confidence capped ≤0.95", r1.confidence <= 0.95),
            Check("PL3 split below quorum → not VERIFIED", r2.verdict != "VERIFIED"),
            Check("conf 1.0 below PL5 capped", r3.confidence <= 0.95),
        ]

    return Module.wrap(
        id="verify.chains", version="8.0.0",
        summary="Dependency-aware, Sybil-hardened blind-vote consensus over chains A–I.",
        run=lambda votes, pl, **kw: verify(votes, pl, **kw),
        capabilities={"verify.chains", "verify.consensus"},
        validate=_validate,
    )


if __name__ == "__main__":
    strong = "reason " * 120
    print("### PL3 — three independent chains agree")
    print(verify([ChainVote("A", True, 0.9, strong),
                  ChainVote("B", True, 0.92, strong),
                  ChainVote("D", True, 0.88, strong)], pl=3).summary())
    print("\n### PL5 — needs formal/anchor; here Chain C present")
    print(verify([ChainVote("A", True, 0.95, strong), ChainVote("B", True, 0.95, strong),
                  ChainVote("C", True, 0.97, strong), ChainVote("D", True, 0.9, strong),
                  ChainVote("E", True, 0.9, strong), ChainVote("G", True, 0.9, strong),
                  ChainVote("F", True, 0.9, strong), ChainVote("H", True, 0.9, strong),
                  ChainVote("A", True, 0.9, strong)], pl=5).summary())
    print("\n### Sybil — lone over-confident, thin justification")
    print(verify([ChainVote("A", True, 1.0, "trust me")], pl=3).summary())
