"""
USF v3 REBORN — engine package.

The wired, zero-dependency product. Core modules are importable flat (the way
the CLI and the plan-mode hook use them):

    calibrator   — CS/DC/AE/VA/TC precision calibration
    usf          — the planner (vision → staged plan)
    verification — chains A–I, blind-vote consensus
    codex        — codified-output grammar + wired efficiency
    module       — the Module contract + registry
    vampirize    — governed external-content ingest
    evolution/   — bounded self-improvement (oracle_meta, capability_scope, …)

Reference implementations harvested from prior versions (not on the wired path)
live under `_harvested/`.
"""

__version__ = "3.0.0"
