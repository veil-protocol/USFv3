"""
Version Lineage — content-hashed, immutable, rollback-safe.

Every integrated improvement is a semver node in an append-only tree. History is
never mutated; a rollback CREATES A NEW version pointing back at the target.
Auto-rollback triggers (quality −5%, failure +2%, convergence failure, resource
>2×) arm during a monitoring window. Backed by SQLite (stdlib).
"""

import _bootpath  # noqa: F401

import hashlib
import json
import sqlite3
from dataclasses import dataclass


@dataclass
class Metrics:
    quality_delta: float = 0.0     # vs parent, fraction (e.g. -0.05 = -5%)
    failure_delta: float = 0.0     # vs parent
    converged: bool = True
    resource_ratio: float = 1.0    # vs baseline


AUTO_ROLLBACK = {
    "quality_degradation":   lambda m: m.quality_delta < -0.05,
    "failure_increase":      lambda m: m.failure_delta > 0.02,
    "convergence_failure":   lambda m: not m.converged,
    "resource_exhaustion":   lambda m: m.resource_ratio > 2.0,
}


def _bump(number: str, level: str = "patch") -> str:
    a, b, c = (number.split(".") + ["0", "0", "0"])[:3]
    a, b, c = int(a), int(b), int(c)
    if level == "major":
        a, b, c = a + 1, 0, 0
    elif level == "minor":
        b, c = b + 1, 0
    else:
        c += 1
    return f"{a}.{b}.{c}"


class VersionLineage:
    def __init__(self, path: str = ":memory:"):
        self.db = sqlite3.connect(path)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS versions(
                version_id TEXT PRIMARY KEY, number TEXT, parent TEXT,
                content_hash TEXT, scope_hash TEXT, status TEXT,
                created_by TEXT, stamp TEXT, note TEXT, payload TEXT)""")
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS audit(
                version_id TEXT, event TEXT, detail TEXT)""")
        self.db.commit()

    def _vid(self, number: str, content_hash: str, stamp: str) -> str:
        return f"USF-{number}-{stamp}-{content_hash[:8]}"

    def genesis(self, number: str, scope_hash: str, stamp: str) -> str:
        ch = hashlib.sha256(f"genesis:{number}".encode()).hexdigest()
        vid = self._vid(number, ch, stamp)
        self.db.execute("INSERT INTO versions VALUES(?,?,?,?,?,?,?,?,?,?)",
                        (vid, number, None, ch, scope_hash, "ACTIVE",
                         "genesis", stamp, "genesis", "{}"))
        self._audit(vid, "CREATE", "genesis")
        self.db.commit()
        return vid

    def create(self, parent_id: str, scope_hash: str, stamp: str,
               created_by: str, note: str, payload: dict,
               level: str = "patch") -> str:
        parent = self.get(parent_id)
        number = _bump(parent["number"], level)
        ch = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()
                            + parent["content_hash"].encode()).hexdigest()
        vid = self._vid(number, ch, stamp)
        with self.db:
            self.db.execute("UPDATE versions SET status='SUPERSEDED' WHERE version_id=?",
                            (parent_id,))
            self.db.execute("INSERT INTO versions VALUES(?,?,?,?,?,?,?,?,?,?)",
                            (vid, number, parent_id, ch, scope_hash, "ACTIVE",
                             created_by, stamp, note, json.dumps(payload)))
            self._audit(vid, "CREATE", note)
        return vid

    def check_auto_rollback(self, metrics: Metrics) -> list[str]:
        return [name for name, trig in AUTO_ROLLBACK.items() if trig(metrics)]

    def rollback(self, current_id: str, stamp: str, reason: str,
                 to_id: str | None = None) -> str:
        current = self.get(current_id)
        target = self.get(to_id) if to_id else self.get(current["parent"])
        # Rollback creates a NEW active version from the target's content.
        number = _bump(current["number"]) + "-rb"
        ch = hashlib.sha256(f"rollback:{target['content_hash']}:{stamp}".encode()).hexdigest()
        vid = self._vid(number, ch, stamp)
        with self.db:
            self.db.execute("UPDATE versions SET status='ROLLED_BACK' WHERE version_id=?",
                            (current_id,))
            self.db.execute("INSERT INTO versions VALUES(?,?,?,?,?,?,?,?,?,?)",
                            (vid, number, target["version_id"], ch, target["scope_hash"],
                             "ACTIVE", "rollback", stamp, f"rollback: {reason}",
                             target["payload"]))
            self._audit(vid, "ROLLBACK", reason)
        return vid

    def get(self, version_id: str) -> dict:
        row = self.db.execute("SELECT * FROM versions WHERE version_id=?",
                              (version_id,)).fetchone()
        cols = [c[1] for c in self.db.execute("PRAGMA table_info(versions)")]
        return dict(zip(cols, row))

    def current(self) -> dict | None:
        row = self.db.execute(
            "SELECT version_id FROM versions WHERE status='ACTIVE' "
            "ORDER BY rowid DESC LIMIT 1").fetchone()
        return self.get(row[0]) if row else None

    def history(self) -> list[tuple[str, str, str]]:
        return [(r[0], r[1], r[2]) for r in self.db.execute(
            "SELECT number, status, note FROM versions ORDER BY rowid")]

    def _audit(self, vid: str, event: str, detail: str) -> None:
        self.db.execute("INSERT INTO audit VALUES(?,?,?)", (vid, event, detail))


if __name__ == "__main__":
    lin = VersionLineage()
    g = lin.genesis("3.0.0", "scope-abc", "20261029000000")
    v1 = lin.create(g, "scope-abc", "20261029000100", "MAL-QUALITY",
                    "retune calibrator", {"param": "cs_weight", "from": 1, "to": 2})
    # a bad version that degrades quality by 7% → auto-rollback fires.
    v2 = lin.create(v1, "scope-abc", "20261029000200", "MAL-EFFICIENCY",
                    "aggressive dedup", {"param": "dedup_threshold", "to": 0.5})
    trig = lin.check_auto_rollback(Metrics(quality_delta=-0.07))
    print("auto-rollback triggers:", trig)
    if trig:
        v3 = lin.rollback(v2, "20261029000300", ",".join(trig))
    print("\nlineage:")
    for num, status, note in lin.history():
        print(f"  {num:<12} {status:<11} {note}")
    print("\ncurrent:", lin.current()["number"])
