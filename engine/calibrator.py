"""
USF v3 REBORN — Precision Calibrator
=====================================

The auto-config brain of the forge. Turns a task (any domain) into a
Precision Level (PL1-PL5) plus the verification depth it implies.

This module is the first real implementation of a model that was fully
specified in `usf-public/precision/PRECISION-CALIBRATOR.md` across every
prior USF iteration but was NEVER coded — the shipped CLIs used crude
keyword regex instead. This brings the CS/DC/AE/VA/TC factor model to life.

Factor model (each factor scored 1-5):
    CS  Consequence Severity   (1 minimal -> 5 catastrophic / irreversible)
    DC  Domain Complexity      (1 well-understood -> 5 novel territory)
    AE  Adversarial Exposure   (1 none -> 5 nation-state)
    VA  Verification Available  (1 none -> 5 full formal verification)
    TC  Time Criticality       (1 no pressure -> 5 immediate)   [INVERSE]

    raw        = CS + DC + AE + VA - TC            # range -1 .. 19
    normalized = (raw + 1) / 5                     # range  0 .. 4
    PL         = clamp(floor(normalized) + 1, 1, 5)

Override rules then raise (or, for documented emergencies, lower) the PL.

Zero third-party dependencies. Run `python3 calibrator.py` for a self-test.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from typing import Optional


# --------------------------------------------------------------------------
# PL -> verification depth tables
# --------------------------------------------------------------------------

# Verification chains spawned per level. PL4 = 6 chains (the canonical choice;
# the v6 executor erroneously emitted 4 — fixed here).
PL_CHAINS: dict[int, tuple[str, ...]] = {
    1: ("A",),
    2: ("A", "B"),
    3: ("A", "B", "D"),
    4: ("A", "B", "C", "D", "E", "F"),
    5: ("A", "B", "C", "D", "E", "F", "G", "H", "I"),
}

PL_CONFIDENCE_TARGET: dict[int, float] = {
    1: 0.80,
    2: 0.90,
    3: 0.95,
    4: 0.99,
    5: 0.999,
}

PL_LABEL: dict[int, str] = {
    1: "RAPID (pattern-match)",
    2: "STANDARD",
    3: "RIGOROUS (default)",
    4: "EXHAUSTIVE",
    5: "INFORMATION-THEORETIC",
}


# --------------------------------------------------------------------------
# Domain defaults — (default_pl, floor_pl). Domains use the USF taxonomy
# prefixes; `detect_domain()` maps free text onto these keys.
# --------------------------------------------------------------------------

DOMAIN_DEFAULTS: dict[str, tuple[int, int]] = {
    "T.SEC.CRY": (4, 3),   # cryptography
    "T.SEC": (4, 3),       # security (general)
    "E.ENG.AER": (4, 4),   # aerospace engineering
    "E.ENG.NUC": (4, 4),   # nuclear
    "M.MED.SURG": (4, 4),  # surgical / safety-critical medicine
    "M.MED": (3, 3),       # medicine (general)
    "L.LAW.REG": (3, 3),   # regulatory / compliance
    "L.LAW": (3, 2),       # legal (general)
    "F.FIN": (3, 2),       # finance
    "E.ENG": (3, 2),       # engineering (general)
    "T.DEV.SEC": (4, 3),   # secure development
    "T.DEV": (2, 1),       # software development
    "T.AI": (3, 2),        # AI / ML
    "S.SCI": (3, 2),       # science / research
    "B.BIZ": (2, 1),       # business
    "default": (3, 1),
}

# Free-text -> taxonomy key. First match wins; order = MOST SPECIFIC FIRST, then
# domain-general. Widened across EVERY domain (not just security) so the forge
# classifies and calibrates work in any field — security is one domain of many.
_DOMAIN_SIGNALS: list[tuple[str, str]] = [
    # --- specific sub-domains (must precede their general parent) ---
    (r"\b(crypto\w*|cipher|encrypt\w*|decrypt\w*|key\s*exchange|zero[-\s]?knowledge|"
     r"post[-\s]?quantum|\btls\b|\bssl\b|\bpki\b|certificate|signature\s*scheme|\bhmac\b|"
     r"\bkdf\b|diffie|\brsa\b|\baes\b|ecdsa|ml[-\s]?kem|ml[-\s]?dsa|handshake)\b", "T.SEC.CRY"),
    (r"\b(aerospace|avionics|flight\s*control|spacecraft|satellite)\b", "E.ENG.AER"),
    (r"\b(nuclear|reactor)\b", "E.ENG.NUC"),
    (r"\b(surgery|surgical|anesthesi|life[-\s]?support|clinical\s*trial|operating\s*room)\b", "M.MED.SURG"),
    (r"\b(gdpr|hipaa|ccpa|sec\s*filing|compliance|regulat\w*|\bsox\b|pci[-\s]?dss|"
     r"fedramp|iso\s*27001|\bnist\b|data\s*protection|privacy\s*policy)\b", "L.LAW.REG"),
    (r"\b(secure\s*coding|appsec|owasp|\bxss\b|sqli|sql\s*inject\w*|\bcsrf\b|\bssrf\b|"
     r"authz|authn|auth(entication|orization)|\boauth\b|\bjwt\b|session\s*management|"
     r"input\s*validation|sandbox|sanitiz\w*|secret\w*\s*management|\brbac\b)\b", "T.DEV.SEC"),
    # --- general domains ---
    (r"\b(security|vulnerab\w*|weakness(es)?|\bcve\b|exploit\w*|pentest|penetration\s*test|"
     r"bug\s*bounty|attack\s*surface|malware|ransomware|phishing|red\s*team|blue\s*team|"
     r"threat\s*\w+|harden\w*|backdoor|intrusion|breach|siem|security\s*operations|"
     r"detection\s*(engineering|rule|logic|content)|\bmitre\b|\bttp\b|\bapt\b|\bc2\b|"
     r"lateral\s*movement|privilege\s*escalation|"
     r"(security|network|auth|cryptographic)\s*protocol|"
     r"protocol\s*(analysis|audit|review|hardening|weakness))\b", "T.SEC"),
    (r"\b(diagnos\w*|patient|disease|dosage|medical|treatment|therap\w*|symptom|"
     r"prognosis|clinical|\bdrug\b|health(care)?)\b", "M.MED"),
    (r"\b(contract|liabilit\w*|statute|litigation|legal|\bnda\b|agreement|terms\s*of\s*service|"
     r"intellectual\s*property|\bpatent\b|trademark|clause|counsel|jurisdiction|dispute)\b", "L.LAW"),
    (r"\b(trading|portfolio|valuation|\baudit\b|accounting|ledger|invoice|revenue|forecast|"
     r"budget|investment|hedge|derivative|equit\w*|\bbond\b|cash\s*flow|\bdcf\b|\broi\b|"
     r"financial|pricing\s*model)\b", "F.FIN"),
    (r"\b(machine\s*learning|\bml\b|deep\s*learning|neural|\bllm\b|transformer|"
     r"fine[-\s]?tun\w*|inference|embedding|\brag\b|training\s*data|classifier|"
     r"reinforcement\s*learning|prompt\s*engineering)\b", "T.AI"),
    (r"\b(hypothesis|experiment\w*|literature\s*review|\bproof\b|theorem|empirical|"
     r"research|study|survey|synthesis|meta[-\s]?analysis|statistic\w*|reproduc\w*|"
     r"peer\s*review|methodology)\b", "S.SCI"),
    (r"\b(engineering|system\s*design|distributed\s*system\w*|mechanical|electrical|"
     r"circuit|\bcad\b|tolerance|stress\s*analysis|material\w*|manufacturing|reliability|"
     r"control\s*system|embedded\s*system|hardware\s*design|thermal|structural)\b", "E.ENG"),
    (r"\b(roadmap|go[-\s]?to[-\s]?market|\bgtm\b|pricing|strategy|revenue|customer|market\w*|"
     r"competitor|product\s*(spec|launch|feature)|\bokr\b|\bkpi\b|stakeholder|operations|"
     r"growth|churn|positioning|business\s*case|m&a|merger|acquisition|due\s*diligence)\b", "B.BIZ"),
    (r"\b(refactor|implement|\bapi\b|function|module|deploy\w*|code|script|library|build|"
     r"debug|\btest(ing|s)?\b|database|migration|microservice\w*|container|kubernetes|docker|"
     r"ci[-/\s]?cd|backend|frontend|algorithm|data\s*structure|compiler|concurrency|"
     r"latency|performance)\b", "T.DEV"),
]


# --------------------------------------------------------------------------
# Magic-keyword precision overrides (the usf-7 ergonomics; highest wins).
# These are detected here so the planner and the calibrator agree.
# --------------------------------------------------------------------------

_MAGIC_KEYWORDS: dict[str, int] = {
    "ultrathink": 5,
    "megathink": 5,
    "think harder": 3,
    "think hard": 3,
    "think": 2,
    "eco": 1,
    "fast": 1,
}


@dataclass
class Factors:
    """The five calibration factors, each 1-5."""
    cs: int = 3  # consequence severity
    dc: int = 3  # domain complexity
    ae: int = 1  # adversarial exposure
    va: int = 3  # verification availability
    tc: int = 3  # time criticality (inverse)

    def clamp(self) -> "Factors":
        c = lambda v: max(1, min(5, int(v)))
        return Factors(c(self.cs), c(self.dc), c(self.ae), c(self.va), c(self.tc))

    def raw(self) -> int:
        return self.cs + self.dc + self.ae + self.va - self.tc


@dataclass
class Calibration:
    """Result of a calibration, with full provenance."""
    task: str
    domain: str
    factors: Factors
    base_pl: int
    final_pl: int
    chains: tuple[str, ...]
    confidence_target: float
    label: str
    reasons: list[str] = field(default_factory=list)

    def summary(self) -> str:
        f = self.factors
        lines = [
            f"task           : {self.task[:72]}",
            f"domain         : {self.domain}",
            f"factors        : CS={f.cs} DC={f.dc} AE={f.ae} VA={f.va} TC={f.tc}"
            f"  (raw={f.raw()})",
            f"base PL        : {self.base_pl}",
            f"final PL       : {self.final_pl}  [{self.label}]",
            f"chains         : {len(self.chains)}  ({', '.join(self.chains)})",
            f"confidence tgt : {self.confidence_target:.1%}",
            "reasons        :",
        ]
        lines += [f"    - {r}" for r in self.reasons]
        return "\n".join(lines)


# --------------------------------------------------------------------------
# Core math
# --------------------------------------------------------------------------

def compute_base_pl(factors: Factors) -> int:
    normalized = (factors.raw() + 1) / 5.0
    return max(1, min(5, math.floor(normalized) + 1))


def detect_domain(task: str) -> str:
    t = task.lower()
    for pattern, key in _DOMAIN_SIGNALS:
        if re.search(pattern, t):
            return key
    return "default"


def detect_magic_keyword(task: str) -> Optional[int]:
    """Return the highest PL implied by any magic keyword, else None."""
    t = task.lower()
    hits = [pl for kw, pl in _MAGIC_KEYWORDS.items() if kw in t]
    return max(hits) if hits else None


# --------------------------------------------------------------------------
# Heuristic auto-scorer — estimate factors from free text when the caller
# has not scored them by hand. Deliberately conservative.
# --------------------------------------------------------------------------

_SIGNALS = {
    "cs": [  # consequence severity raisers
        (r"\b(production|irreversible|destruc|delete|wipe|financial|safety|life|patient|nuclear|launch)\b", 2),
        (r"\b(critical|severe|catastroph|breach|leak)\b", 1),
        (r"\b(draft|sketch|prototype|throwaway|scratch|toy|example)\b", -2),
    ],
    "dc": [
        (r"\b(novel|research|unknown|open\s*problem|first[-\s]?principles|unprecedented)\b", 2),
        (r"\b(complex|intricate|multi[-\s]?step|distributed|concurren)\b", 1),
        (r"\b(simple|trivial|routine|standard|basic|well[-\s]?understood)\b", -2),
    ],
    "ae": [
        (r"\b(nation[-\s]?state|apt\b|state[-\s]?sponsored)\b", 4),
        (r"\b(adversar|attacker|threat\s*model|hostile)\b", 3),
        (r"\b(security|exploit|vulnerab|untrusted\s*input|malicious)\b", 2),
    ],
    "va": [
        (r"\b(formal(ly)?\s*verif|theorem|proof|test\s*suite|ground\s*truth|benchmark)\b", 2),
        (r"\b(verifiable|measurable|reproducible)\b", 1),
        (r"\b(subjective|opinion|aesthetic|unmeasurable)\b", -2),
    ],
    "tc": [
        (r"\b(urgent|immediately|asap|now|emergency|incident|outage|hotfix)\b", 3),
        (r"\b(quick|fast|rapid|soon)\b", 1),
        (r"\b(thorough|exhaustive|comprehensive|take\s*your\s*time|no\s*rush)\b", -2),
    ],
}


def auto_score(task: str, domain: str) -> Factors:
    t = task.lower()
    base = {"cs": 2, "dc": 2, "ae": 1, "va": 3, "tc": 3}
    for factor, rules in _SIGNALS.items():
        for pattern, delta in rules:
            if re.search(pattern, t):
                base[factor] += delta
    # Domain nudges: security/crypto domains carry inherent adversarial exposure.
    if domain.startswith("T.SEC"):
        base["ae"] = max(base["ae"], 4)
        base["cs"] = max(base["cs"], 3)
    return Factors(base["cs"], base["dc"], base["ae"], base["va"], base["tc"]).clamp()


# --------------------------------------------------------------------------
# Override rules (spec §3): raise PL for high-stakes domains; permit a
# documented emergency downgrade.
# --------------------------------------------------------------------------

def apply_overrides(base_pl: int, factors: Factors, domain: str,
                    reasons: list[str]) -> int:
    pl = base_pl

    # Domain floor.
    default_pl, floor_pl = DOMAIN_DEFAULTS.get(domain, DOMAIN_DEFAULTS["default"])
    if pl < floor_pl:
        reasons.append(f"domain '{domain}' floor raises PL {pl} -> {floor_pl}")
        pl = floor_pl

    # Nation-state exposure.
    if factors.ae >= 5 and pl < 4:
        reasons.append("adversarial exposure = nation-state (AE=5): floor PL4")
        pl = max(pl, 4)

    # Crypto / regulatory explicit floors (redundant with table but explicit).
    if domain.startswith("T.SEC.CRY") and pl < 3:
        reasons.append("cryptography: floor PL3")
        pl = max(pl, 3)

    # Documented emergency downgrade: only when truly low-consequence.
    if factors.tc >= 5 and factors.cs <= 2 and pl > 1:
        reasons.append(
            f"EMERGENCY downgrade (TC=5, CS={factors.cs}<=2): PL {pl} -> 1 "
            "[risk accepted — low consequence]"
        )
        pl = 1

    return max(1, min(5, pl))


# --------------------------------------------------------------------------
# Public entry point
# --------------------------------------------------------------------------

def calibrate(task: str,
              domain: Optional[str] = None,
              factors: Optional[Factors] = None,
              honor_keywords: bool = True) -> Calibration:
    """Calibrate a task to a Precision Level.

    task     : the free-text goal/vision.
    domain   : optional taxonomy key; auto-detected if omitted.
    factors  : optional hand-scored Factors; auto-estimated if omitted.
    honor_keywords : if True, a magic keyword (ultrathink/think/eco) sets a
                     precision FLOOR before factor scoring.
    """
    reasons: list[str] = []
    dom = domain or detect_domain(task)
    if domain is None:
        reasons.append(f"domain auto-detected as '{dom}'")

    f = (factors or auto_score(task, dom)).clamp()
    if factors is None:
        reasons.append("factors auto-estimated from task text")

    base_pl = compute_base_pl(f)
    reasons.append(
        f"factor model: raw={f.raw()} -> base PL{base_pl}"
    )

    final_pl = apply_overrides(base_pl, f, dom, reasons)

    if honor_keywords:
        kw_pl = detect_magic_keyword(task)
        if kw_pl is not None and kw_pl > final_pl:
            reasons.append(f"magic keyword raises PL {final_pl} -> {kw_pl}")
            final_pl = kw_pl
        elif kw_pl is not None:
            reasons.append(f"magic keyword (PL{kw_pl}) <= calibrated PL; no change")

    return Calibration(
        task=task,
        domain=dom,
        factors=f,
        base_pl=base_pl,
        final_pl=final_pl,
        chains=PL_CHAINS[final_pl],
        confidence_target=PL_CONFIDENCE_TARGET[final_pl],
        label=PL_LABEL[final_pl],
        reasons=reasons,
    )


# --------------------------------------------------------------------------
# Self-test — the three worked examples from the spec must reproduce.
# --------------------------------------------------------------------------

if __name__ == "__main__":
    # Canonical factor-model checks (spec §3 worked examples).
    assert compute_base_pl(Factors(1, 2, 1, 3, 4)) == 1, "low-stakes -> PL1"
    assert compute_base_pl(Factors(4, 4, 4, 4, 2)) == 4, "security -> PL4"
    assert compute_base_pl(Factors(4, 3, 2, 2, 5)) == 2, "emergency triage -> PL2"
    print("factor-model checks: OK\n")

    demos = [
        "quickly explain what a hash map is",
        "audit the cryptographic key-exchange in our auth service for nation-state adversaries",
        "write a comprehensive research report synthesizing recent work on fixed points in self-improving systems",
        "hotfix the typo in the README now, urgent",
        "ultrathink: design the migration plan for our billing database",
    ]
    for d in demos:
        print(calibrate(d).summary())
        print("-" * 72)
