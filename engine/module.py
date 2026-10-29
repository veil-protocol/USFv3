"""
USF 8.0 REBORN — Module Architecture
====================================

The backbone. Every aspect of USF is a Module with a uniform contract, so that
each one can be independently:

    run        — do its job
    validate   — prove it still works (used by self-evolution + CI)
    improve    — accept a self-evolution proposal (bounded, gated)
    vampirize  — absorb external repo/research/content into itself

Each module also declares the CAPABILITIES it contributes. The union of all
module capabilities IS the system's capability scope — the thing the
bounded-self-improvement safety bound watches (see evolution/capability_scope).

This is what makes USF a platform rather than a script: new modules plug in,
existing ones are built upon, and outside content is assimilated — all through
one contract.

Stdlib only.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Callable, Optional


# --------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------

@dataclass
class Check:
    name: str
    ok: bool
    detail: str = ""


@dataclass
class ValidationResult:
    module_id: str
    checks: list[Check] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return all(c.ok for c in self.checks) if self.checks else True

    @property
    def score(self) -> float:
        if not self.checks:
            return 1.0
        return sum(1 for c in self.checks if c.ok) / len(self.checks)

    def summary(self) -> str:
        head = f"{'PASS' if self.ok else 'FAIL'} {self.module_id} ({self.score:.0%})"
        body = "\n".join(f"    {'ok' if c.ok else 'XX'}  {c.name}"
                         + (f" — {c.detail}" if c.detail else "")
                         for c in self.checks)
        return head + ("\n" + body if body else "")


# --------------------------------------------------------------------------
# Provenance — where a module's patterns came from. Written by vampirize().
# --------------------------------------------------------------------------

@dataclass
class Provenance:
    source: str              # repo URL / paper / file — pinned permalink, not HEAD
    ingested: str            # ISO date (passed in; no wall-clock here)
    confidence: float        # validation confidence at ingest
    note: str = ""


# --------------------------------------------------------------------------
# Module
# --------------------------------------------------------------------------

@dataclass
class Module:
    """A unit of USF capability. Subclass OR wrap callables via `wrap()`.

    The four contract methods have safe defaults so a minimal module just needs
    an id, version, and a run function.
    """
    id: str
    version: str
    summary: str
    capabilities: frozenset[str] = frozenset()
    # Core behaviour.
    _run: Optional[Callable[..., Any]] = None
    _validate: Optional[Callable[[], list[Check]]] = None
    # Extensibility flags/hooks.
    improvable: bool = True
    vampirizable: bool = True
    _vampirize: Optional[Callable[[Any], list[dict]]] = None
    provenance: list[Provenance] = field(default_factory=list)

    # -- run -------------------------------------------------------------
    def run(self, *args, **kwargs) -> Any:
        if self._run is None:
            raise NotImplementedError(f"module {self.id} has no run()")
        return self._run(*args, **kwargs)

    # -- validate --------------------------------------------------------
    def validate(self) -> ValidationResult:
        checks = self._validate() if self._validate else []
        return ValidationResult(self.id, checks)

    # -- improve ---------------------------------------------------------
    def improve(self, proposal: "ImprovementProposal") -> str:
        """Apply a validated self-evolution proposal. Returns the new version.

        The evolution engine is responsible for validation + gating BEFORE
        calling this; here we only bump the version and record the change.
        A real module overrides this to mutate its own parameters/spec.
        """
        if not self.improvable:
            raise PermissionError(f"module {self.id} is not improvable")
        self.version = _bump_patch(self.version)
        return self.version

    # -- vampirize -------------------------------------------------------
    def vampirize(self, source: Any) -> list[dict]:
        """Extract candidate patterns from external content.

        Returns a list of candidate-pattern dicts for the vampirize pipeline to
        validate + (on approval) fold in. Does NOT self-integrate — integration
        is capability-scope-gated upstream.
        """
        if not self.vampirizable:
            raise PermissionError(f"module {self.id} is not vampirizable")
        if self._vampirize:
            return self._vampirize(source)
        return []

    def record_provenance(self, p: Provenance) -> None:
        self.provenance.append(p)

    # -- identity --------------------------------------------------------
    def content_hash(self) -> str:
        blob = json.dumps(
            {"id": self.id, "version": self.version,
             "capabilities": sorted(self.capabilities)},
            sort_keys=True,
        )
        return hashlib.sha256(blob.encode()).hexdigest()[:16]

    @classmethod
    def wrap(cls, id: str, version: str, summary: str, run: Callable,
             capabilities: set[str] | frozenset[str] = frozenset(),
             validate: Optional[Callable[[], list[Check]]] = None,
             **kw) -> "Module":
        return cls(id=id, version=version, summary=summary,
                   capabilities=frozenset(capabilities), _run=run,
                   _validate=validate, **kw)


@dataclass
class ImprovementProposal:
    """A self-evolution proposal targeting a module (see evolution/)."""
    source_agent: str          # which MAL agent proposed it
    target_module: str
    category: str              # TAXONOMY|TEMPLATE|ARCHETYPE|PRECISION|VERIFICATION|PROCESS|META
    risk: str                  # LOW|MEDIUM|HIGH|CRITICAL
    description: str
    adds_capabilities: frozenset[str] = frozenset()   # non-empty => scope expansion


# --------------------------------------------------------------------------
# Registry
# --------------------------------------------------------------------------

class ModuleRegistry:
    def __init__(self) -> None:
        self._modules: dict[str, Module] = {}

    def register(self, module: Module) -> Module:
        if module.id in self._modules:
            raise ValueError(f"duplicate module id: {module.id}")
        self._modules[module.id] = module
        return module

    def get(self, module_id: str) -> Module:
        return self._modules[module_id]

    def all(self) -> list[Module]:
        return list(self._modules.values())

    def capability_scope(self) -> frozenset[str]:
        """The union of every module's capabilities — the system scope."""
        out: set[str] = set()
        for m in self._modules.values():
            out |= set(m.capabilities)
        return frozenset(out)

    def scope_hash(self) -> str:
        blob = json.dumps(sorted(self.capability_scope()), sort_keys=True)
        return hashlib.sha256(blob.encode()).hexdigest()[:16]

    def validate_all(self) -> list[ValidationResult]:
        return [m.validate() for m in self._modules.values()]


def _bump_patch(version: str) -> str:
    parts = version.split(".")
    try:
        parts[-1] = str(int(parts[-1]) + 1)
        return ".".join(parts)
    except (ValueError, IndexError):
        return version + ".1"


# --------------------------------------------------------------------------
# Default registry — the modules that exist today, wrapped under the contract.
# --------------------------------------------------------------------------

def build_default_registry() -> ModuleRegistry:
    import calibrator as cal
    import usf as planner

    reg = ModuleRegistry()

    # --- calibrator module ---
    def _cal_validate() -> list[Check]:
        c = cal.Factors
        return [
            Check("factor-model low-stakes->PL1",
                  cal.compute_base_pl(c(1, 2, 1, 3, 4)) == 1),
            Check("factor-model security->PL4",
                  cal.compute_base_pl(c(4, 4, 4, 4, 2)) == 4),
            Check("nation-state crypto audit floors PL4",
                  cal.calibrate("audit the cryptographic key-exchange for "
                                "nation-state adversaries").final_pl == 4),
        ]

    reg.register(Module.wrap(
        id="precision.calibrator", version="8.0.0",
        summary="CS/DC/AE/VA/TC factor model -> Precision Level.",
        run=lambda task, **kw: cal.calibrate(task, **kw),
        capabilities={"precision.calibrate", "domain.detect"},
        validate=_cal_validate,
    ))

    # --- planner module ---
    def _plan_validate() -> list[Check]:
        p = planner.plan("audit the crypto key-exchange for nation-state adversaries")
        r = planner.plan("write a quick explainer on hash maps")
        return [
            Check("security vision -> PL4 hivemind", p.precision_level == 4 and p.compute_type == "hivemind"),
            Check("panel synthesized for domain", any(e["persona"] == "Red Team Operator" for e in p.expert_panel)),
            Check("agents = chains + panel", p.total_agents == len(p.verification_chains) + len(p.expert_panel)),
            Check("rapid vision stays low PL", r.precision_level <= 2),
        ]

    reg.register(Module.wrap(
        id="plan.planner", version="8.0.0",
        summary="Vision -> configured, staged execution plan.",
        run=lambda task, **kw: planner.plan(task, **kw),
        capabilities={"plan.generate", "compute.select", "panel.synthesize"},
        validate=_plan_validate,
    ))

    return reg


if __name__ == "__main__":
    reg = build_default_registry()
    print(f"registered modules : {[m.id for m in reg.all()]}")
    print(f"capability scope   : {sorted(reg.capability_scope())}")
    print(f"scope hash         : {reg.scope_hash()}")
    print("-" * 60)
    ok = True
    for res in reg.validate_all():
        print(res.summary())
        ok = ok and res.ok
    print("-" * 60)
    print("ALL MODULES VALID" if ok else "VALIDATION FAILURES PRESENT")
