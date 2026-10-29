#!/usr/bin/env python3
"""
USF 8.0 REBORN — UserPromptSubmit router hook.

The glue that was designed in every prior version and never wired. When a prompt
opts into USF — "use usf", "usf:", or a magic keyword (ultrathink/think/eco) —
this hook runs the planner and injects the resulting plan as context, and on
PL3+ recommends entering plan mode (read-only explore → approval gate → execute).

Contract: Claude Code calls this with the hook event JSON on stdin. For
UserPromptSubmit, anything printed to stdout (exit 0) is added to the model's
context. On no trigger — or any error — it stays silent and never blocks the
prompt. Stdlib only.
"""

import json
import pathlib
import re
import sys

TRIGGERS = ("use usf", "usf:", "/usf", "ultrathink", "megathink",
            "think hard", "think harder", "use usf deep", "use usf plan")


def _strip_trigger(prompt: str) -> str:
    out = prompt
    for t in ("use usf deep", "use usf plan", "use usf", "usf:", "/usf"):
        out = re.sub(re.escape(t), "", out, flags=re.IGNORECASE)
    return out.strip(" :-\t\n") or prompt


def main() -> int:
    try:
        raw = sys.stdin.read()
        event = json.loads(raw) if raw.strip() else {}
        prompt = event.get("prompt", "")
        low = prompt.lower()
        if not any(t in low for t in TRIGGERS):
            return 0  # not a USF prompt — stay silent

        engine = pathlib.Path(__file__).resolve().parent.parent.parent / "engine"
        sys.path.insert(0, str(engine))
        import usf as planner  # noqa

        task = _strip_trigger(prompt)
        p = planner.plan(task)

        lines = [
            "[USF 8.0 ROUTER] This prompt opted into USF. Suggested configuration:",
            f"  vision     : {task[:70]}",
            f"  domain     : {p.domain}",
            f"  precision  : PL{p.precision_level} ({p.precision_label}) → {p.confidence_target:.0%} target",
            f"  compute    : {p.compute_type} ({p.aggregation})",
            f"  panel      : {', '.join(e['persona'] for e in p.expert_panel)}",
            f"  chains     : {', '.join(p.verification_chains)}  |  agents: {p.total_agents}",
            "  pipeline   : " + " → ".join(s["name"] for s in p.pipeline),
        ]
        if p.precision_level >= 3:
            lines.append(
                "  ACTION: PL3+ — enter PLAN MODE (read-only explore → plan doc → "
                "approval gate via ExitPlanMode) before executing. Apply the panel "
                "and verification chains above; render output in the codified grammar.")
        else:
            lines.append("  ACTION: PL1–2 — proceed directly with the configuration above.")
        print("\n".join(lines))
        return 0
    except Exception:
        # Never block prompt submission on a hook error.
        return 0


if __name__ == "__main__":
    sys.exit(main())
