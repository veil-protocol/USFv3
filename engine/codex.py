"""
Codex — the codified-output grammar + the wired efficiency layer.

Two things that were scattered and never unified across prior USF versions, now
one module:

  1. CODIFIED OUTPUT — the compact grammar agents emit and consume:
       * structured markers:  [FINDING] [CLAIM] [STAT k=v] [DATA] [LIMITATION] [VERDICT]
       * role-tag personas:   "Role: X | Focus: Y / Key approach: a; b"  (~85% smaller)
       * archetype refs:      ARC-AD@security   (expands from cache in verbose mode)

  2. EFFICIENCY — context assembly that actually RUNS. Prior versions shipped
     tiered_loader/dedup modules but the executor still hard-truncated at 8000
     chars (measured 1.0x). This assembler tiers by relevance (L1 full / L2 lead
     sentences / L3 headers-only) and de-duplicates, achieving a real reduction.

Stdlib only.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass


# --------------------------------------------------------------------------
# 1a. Structured markers
# --------------------------------------------------------------------------

MARKERS = ("FINDING", "CLAIM", "STAT", "DATA", "LIMITATION", "VERDICT")
_MARKER_RE = re.compile(r"\[(" + "|".join(MARKERS) + r")(?::([^\]]*))?\]\s?(.*)")


@dataclass
class Marked:
    kind: str
    attrs: dict
    text: str


def emit(kind: str, text: str = "", **attrs) -> str:
    kind = kind.upper()
    if kind not in MARKERS:
        raise ValueError(f"unknown marker {kind}")
    if attrs:
        a = ",".join(f"{k}={v}" for k, v in attrs.items())
        return f"[{kind}:{a}] {text}".rstrip()
    return f"[{kind}] {text}".rstrip()


def parse(line: str) -> Marked | None:
    m = _MARKER_RE.match(line.strip())
    if not m:
        return None
    kind, raw_attrs, text = m.group(1), m.group(2), m.group(3)
    attrs = {}
    if raw_attrs:
        for part in raw_attrs.split(","):
            if "=" in part:
                k, v = part.split("=", 1)
                attrs[k.strip()] = v.strip()
    return Marked(kind, attrs, text.strip())


# --------------------------------------------------------------------------
# 1b. Role-tag persona codification (the ~85% reduction from CONTEXT-OPTIMIZATION)
# --------------------------------------------------------------------------

def codify_persona(name: str, focus: str, approaches: list[str]) -> str:
    return f"Role: {name} | Focus: {focus}\nKey approach: " + "; ".join(approaches)


def archetype_ref(arc_id: str, domain: str) -> str:
    return f"{arc_id}@{domain}"


# --------------------------------------------------------------------------
# 2. Efficiency — tiered, deduped context assembly (actually wired)
# --------------------------------------------------------------------------

def est_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def tier(text: str, level: int) -> str:
    """L1 full · L2 lead sentence(s) per paragraph · L3 headers/first-line only."""
    if level <= 1:
        return text
    paras = [p for p in text.split("\n\n") if p.strip()]
    out = []
    for p in paras:
        if level == 2:
            sentences = re.split(r"(?<=[.!?])\s+", p.strip())
            out.append(" ".join(sentences[:2]))
        else:  # level 3
            out.append(p.strip().splitlines()[0][:100])
    return "\n".join(out)


@dataclass
class AssemblyStats:
    raw_tokens: int
    final_tokens: int
    kept: int
    deduped: int

    @property
    def ratio(self) -> float:
        return self.raw_tokens / max(1, self.final_tokens)


def assemble_context(chunks: list[tuple[str, float]], budget_tokens: int):
    """chunks = [(text, relevance 0..1)]. Returns (assembled_text, AssemblyStats).

    Relevance routes the tier (>=0.7 full / >=0.4 lead-sentences / else headers),
    exact duplicates are dropped, and chunks are added by relevance until the
    token budget is hit.
    """
    raw = sum(est_tokens(t) for t, _ in chunks)
    seen: set[str] = set()
    picked: list[str] = []
    used = 0
    deduped = 0

    for text, rel in sorted(chunks, key=lambda c: -c[1]):
        h = hashlib.sha256(_norm(text).encode()).hexdigest()[:16]
        if h in seen:
            deduped += 1
            continue
        seen.add(h)
        level = 1 if rel >= 0.7 else (2 if rel >= 0.4 else 3)
        piece = tier(text, level)
        cost = est_tokens(piece)
        if used + cost > budget_tokens:
            piece = tier(text, 3)          # last resort: headers only
            cost = est_tokens(piece)
            if used + cost > budget_tokens:
                continue
        picked.append(piece)
        used += cost

    assembled = "\n\n".join(picked)
    return assembled, AssemblyStats(raw, est_tokens(assembled), len(picked), deduped)


# --------------------------------------------------------------------------
# Module wrapper + self-test
# --------------------------------------------------------------------------

def as_module():
    from module import Module, Check

    def _validate() -> list[Check]:
        m = parse(emit("STAT", "key-exchange UAF", severity="HIGH", cwe="CWE-416"))
        persona = codify_persona("Red Team Operator", "destructive_analysis",
                                 ["assume malicious input", "try to break the fix"])
        chunks = [("# Alpha\n\nFirst sentence here. Second. Third extra detail.", 0.9),
                  ("# Alpha\n\nFirst sentence here. Second. Third extra detail.", 0.9),  # dup
                  ("# Beta\n\nLess relevant body text that should be tiered down hard.", 0.2)]
        _, stats = assemble_context(chunks, budget_tokens=50)
        return [
            Check("marker round-trips w/ attrs", m is not None and m.kind == "STAT"
                  and m.attrs.get("cwe") == "CWE-416"),
            Check("persona codified compactly (<160 chars)", len(persona) < 160),
            Check("archetype ref format", archetype_ref("ARC-AD", "security") == "ARC-AD@security"),
            Check("context dedup removed the duplicate", stats.deduped == 1),
            Check("efficiency actually reduces (ratio>1)", stats.ratio > 1.0),
        ]

    return Module.wrap(
        id="efficiency.codex", version="8.0.0",
        summary="Codified-output grammar + tiered/deduped context assembly.",
        run=lambda chunks, budget: assemble_context(chunks, budget),
        capabilities={"output.codify", "context.tier", "context.dedup"},
        validate=_validate,
    )


if __name__ == "__main__":
    print("### markers")
    print(" ", emit("FINDING", "buffer detachment UAF in WebAudio"))
    print(" ", emit("STAT", "validated=1 false_positive=5", pl=5))
    print(" ", emit("VERDICT", "VERIFIED", conf=0.95))
    print("\n### codified persona (vs a ~1KB verbose block)")
    print(codify_persona("Security Researcher", "constructive_analysis",
                         ["reason from first principles", "map the attack surface"]))
    print("\n### efficiency wiring")
    chunks = [("# Core\n\nKey fact one. Key fact two. Minor aside three.", 0.95),
              ("# Core\n\nKey fact one. Key fact two. Minor aside three.", 0.95),
              ("# Background\n\n" + "filler sentence. " * 40, 0.3)]
    text, stats = assemble_context(chunks, budget_tokens=60)
    print(f"  raw={stats.raw_tokens}tok final={stats.final_tokens}tok "
          f"ratio={stats.ratio:.2f}x deduped={stats.deduped}")
