"""
Continuity Ledgers for USF Cross-Session State Persistence.

USF 7.0 Implementation - Maintains state across session boundaries.

Based on patterns from:
- claude-flow: Session persistence
- aider: Cross-session memory
- cursor-tools: Project state

Features:
- Append-only ledger for audit trail
- Cross-session state restoration
- Automatic checkpoint creation
- Conflict resolution
- State pruning for efficiency

Ledger Types:
- task_ledger: Task execution history
- learning_ledger: Learned patterns and Q-tables
- skill_ledger: Extracted skills
- context_ledger: Context summaries
- error_ledger: Error patterns for prevention
"""

import hashlib
import json
import logging
import os
import shutil
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, Generator, List, Optional, Set, Tuple, Union
import threading
import fcntl

logger = logging.getLogger(__name__)


class LedgerType(Enum):
    """Types of continuity ledgers."""
    TASK = "task"
    LEARNING = "learning"
    SKILL = "skill"
    CONTEXT = "context"
    ERROR = "error"


class EntryType(Enum):
    """Types of ledger entries."""
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    CHECKPOINT = "checkpoint"
    RESTORE = "restore"


@dataclass
class LedgerEntry:
    """A single entry in the ledger."""
    entry_id: str
    entry_type: EntryType
    key: str
    value: Any
    previous_hash: str
    timestamp: datetime = field(default_factory=datetime.now)
    session_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def hash(self) -> str:
        """Compute hash of this entry."""
        content = json.dumps({
            "entry_id": self.entry_id,
            "entry_type": self.entry_type.value,
            "key": self.key,
            "value": str(self.value),
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp.isoformat(),
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "entry_type": self.entry_type.value,
            "key": self.key,
            "value": self.value,
            "previous_hash": self.previous_hash,
            "hash": self.hash,
            "timestamp": self.timestamp.isoformat(),
            "session_id": self.session_id,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LedgerEntry":
        return cls(
            entry_id=data["entry_id"],
            entry_type=EntryType(data["entry_type"]),
            key=data["key"],
            value=data["value"],
            previous_hash=data["previous_hash"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            session_id=data.get("session_id"),
            metadata=data.get("metadata", {}),
        )


@dataclass
class LedgerCheckpoint:
    """A checkpoint capturing ledger state at a point in time."""
    checkpoint_id: str
    ledger_type: LedgerType
    state: Dict[str, Any]
    entry_count: int
    last_entry_hash: str
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "checkpoint_id": self.checkpoint_id,
            "ledger_type": self.ledger_type.value,
            "state": self.state,
            "entry_count": self.entry_count,
            "last_entry_hash": self.last_entry_hash,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LedgerCheckpoint":
        return cls(
            checkpoint_id=data["checkpoint_id"],
            ledger_type=LedgerType(data["ledger_type"]),
            state=data["state"],
            entry_count=data["entry_count"],
            last_entry_hash=data["last_entry_hash"],
            created_at=datetime.fromisoformat(data["created_at"]),
        )


class ContinuityLedger:
    """
    Append-only ledger for cross-session state persistence.

    Each ledger maintains:
    - Append-only log of all changes
    - Periodic checkpoints for fast restoration
    - Current state view
    - Chain integrity verification
    """

    CHECKPOINT_INTERVAL = 100  # entries between checkpoints
    MAX_ENTRIES_BEFORE_PRUNE = 10000
    PRUNE_KEEP_ENTRIES = 1000

    def __init__(
        self,
        ledger_type: LedgerType,
        base_path: Path,
        session_id: Optional[str] = None
    ):
        """
        Initialize a continuity ledger.

        Args:
            ledger_type: Type of ledger
            base_path: Base directory for ledger files
            session_id: Current session identifier
        """
        self.ledger_type = ledger_type
        self.base_path = base_path / ledger_type.value
        self.session_id = session_id or self._generate_session_id()

        # File paths
        self.entries_path = self.base_path / "entries.jsonl"
        self.checkpoints_path = self.base_path / "checkpoints"
        self.state_path = self.base_path / "current_state.json"

        # In-memory state
        self._state: Dict[str, Any] = {}
        self._entries: List[LedgerEntry] = []
        self._last_hash = "genesis"
        self._lock = threading.Lock()
        self._entry_counter = 0

        # Ensure directories exist
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.checkpoints_path.mkdir(parents=True, exist_ok=True)

        # Load existing state
        self._restore()

    def _generate_session_id(self) -> str:
        """Generate unique session ID."""
        return f"session_{int(time.time() * 1000)}"

    def _restore(self):
        """Restore ledger state from disk."""
        # Try to restore from latest checkpoint first
        checkpoint = self._load_latest_checkpoint()

        if checkpoint:
            self._state = checkpoint.state.copy()
            self._entry_counter = checkpoint.entry_count
            self._last_hash = checkpoint.last_entry_hash
            logger.debug(f"Restored from checkpoint {checkpoint.checkpoint_id}")

            # Replay entries after checkpoint
            self._replay_entries_after(checkpoint.entry_count)
        else:
            # Replay all entries
            self._replay_all_entries()

    def _load_latest_checkpoint(self) -> Optional[LedgerCheckpoint]:
        """Load the most recent checkpoint."""
        if not self.checkpoints_path.exists():
            return None

        checkpoints = sorted(self.checkpoints_path.glob("*.json"), reverse=True)
        if not checkpoints:
            return None

        try:
            with open(checkpoints[0], "r") as f:
                data = json.load(f)
                return LedgerCheckpoint.from_dict(data)
        except Exception as e:
            logger.warning(f"Failed to load checkpoint: {e}")
            return None

    def _replay_entries_after(self, start_index: int):
        """Replay entries after a specific index."""
        if not self.entries_path.exists():
            return

        try:
            with open(self.entries_path, "r") as f:
                for i, line in enumerate(f):
                    if i < start_index:
                        continue
                    entry = LedgerEntry.from_dict(json.loads(line))
                    self._apply_entry(entry, persist=False)
        except Exception as e:
            logger.warning(f"Failed to replay entries: {e}")

    def _replay_all_entries(self):
        """Replay all entries from the beginning."""
        if not self.entries_path.exists():
            return

        try:
            with open(self.entries_path, "r") as f:
                for line in f:
                    entry = LedgerEntry.from_dict(json.loads(line))
                    self._apply_entry(entry, persist=False)
        except Exception as e:
            logger.warning(f"Failed to replay entries: {e}")

    def _apply_entry(self, entry: LedgerEntry, persist: bool = True):
        """Apply an entry to the state."""
        if entry.entry_type == EntryType.CREATE:
            self._state[entry.key] = entry.value
        elif entry.entry_type == EntryType.UPDATE:
            self._state[entry.key] = entry.value
        elif entry.entry_type == EntryType.DELETE:
            self._state.pop(entry.key, None)
        elif entry.entry_type == EntryType.CHECKPOINT:
            pass  # Checkpoints don't modify state
        elif entry.entry_type == EntryType.RESTORE:
            if isinstance(entry.value, dict):
                self._state = entry.value.copy()

        self._last_hash = entry.hash
        self._entry_counter += 1
        self._entries.append(entry)

        if persist:
            self._persist_entry(entry)

            # Create checkpoint if needed
            if self._entry_counter % self.CHECKPOINT_INTERVAL == 0:
                self._create_checkpoint()

            # Prune if needed
            if len(self._entries) > self.MAX_ENTRIES_BEFORE_PRUNE:
                self._prune_entries()

    def _persist_entry(self, entry: LedgerEntry):
        """Persist entry to disk with file locking."""
        with open(self.entries_path, "a") as f:
            # File lock for concurrent access
            try:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                f.write(json.dumps(entry.to_dict()) + "\n")
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)

        # Also update current state file
        self._save_current_state()

    def _save_current_state(self):
        """Save current state to quick-access file."""
        with open(self.state_path, "w") as f:
            json.dump({
                "state": self._state,
                "entry_count": self._entry_counter,
                "last_hash": self._last_hash,
                "updated_at": datetime.now().isoformat(),
            }, f, indent=2)

    def _create_checkpoint(self):
        """Create a checkpoint of current state."""
        checkpoint = LedgerCheckpoint(
            checkpoint_id=f"cp_{self._entry_counter}_{int(time.time())}",
            ledger_type=self.ledger_type,
            state=self._state.copy(),
            entry_count=self._entry_counter,
            last_entry_hash=self._last_hash,
        )

        checkpoint_file = self.checkpoints_path / f"{checkpoint.checkpoint_id}.json"
        with open(checkpoint_file, "w") as f:
            json.dump(checkpoint.to_dict(), f, indent=2)

        logger.debug(f"Created checkpoint {checkpoint.checkpoint_id}")

        # Clean old checkpoints (keep last 5)
        checkpoints = sorted(self.checkpoints_path.glob("*.json"), reverse=True)
        for old_checkpoint in checkpoints[5:]:
            old_checkpoint.unlink()

    def _prune_entries(self):
        """Prune old entries, keeping only recent ones."""
        # Create checkpoint first
        self._create_checkpoint()

        # Keep only recent entries
        self._entries = self._entries[-self.PRUNE_KEEP_ENTRIES:]

        # Rewrite entries file
        temp_path = self.entries_path.with_suffix(".tmp")
        with open(temp_path, "w") as f:
            for entry in self._entries:
                f.write(json.dumps(entry.to_dict()) + "\n")

        # Atomic replace
        shutil.move(str(temp_path), str(self.entries_path))

        logger.debug(f"Pruned entries, kept {len(self._entries)}")

    def _create_entry(
        self,
        entry_type: EntryType,
        key: str,
        value: Any,
        metadata: Optional[Dict] = None
    ) -> LedgerEntry:
        """Create a new ledger entry."""
        return LedgerEntry(
            entry_id=f"{self.session_id}_{self._entry_counter}_{int(time.time() * 1000)}",
            entry_type=entry_type,
            key=key,
            value=value,
            previous_hash=self._last_hash,
            session_id=self.session_id,
            metadata=metadata or {},
        )

    def set(self, key: str, value: Any, metadata: Optional[Dict] = None):
        """
        Set a value in the ledger.

        Creates UPDATE entry if key exists, CREATE otherwise.
        """
        with self._lock:
            entry_type = EntryType.UPDATE if key in self._state else EntryType.CREATE
            entry = self._create_entry(entry_type, key, value, metadata)
            self._apply_entry(entry)

    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the ledger."""
        return self._state.get(key, default)

    def delete(self, key: str) -> bool:
        """Delete a key from the ledger."""
        with self._lock:
            if key not in self._state:
                return False

            entry = self._create_entry(EntryType.DELETE, key, None)
            self._apply_entry(entry)
            return True

    def keys(self) -> List[str]:
        """Get all keys in the ledger."""
        return list(self._state.keys())

    def items(self) -> List[Tuple[str, Any]]:
        """Get all key-value pairs."""
        return list(self._state.items())

    def get_history(self, key: str) -> List[LedgerEntry]:
        """Get history of changes for a specific key."""
        return [e for e in self._entries if e.key == key]

    def verify_integrity(self) -> Tuple[bool, Optional[str]]:
        """Verify the integrity of the ledger chain."""
        if not self._entries:
            return True, None

        expected_hash = "genesis"
        for entry in self._entries:
            if entry.previous_hash != expected_hash:
                return False, f"Chain broken at entry {entry.entry_id}"
            expected_hash = entry.hash

        return True, None

    def export_state(self) -> Dict[str, Any]:
        """Export current state for backup."""
        return {
            "ledger_type": self.ledger_type.value,
            "state": self._state.copy(),
            "entry_count": self._entry_counter,
            "last_hash": self._last_hash,
            "exported_at": datetime.now().isoformat(),
        }

    def import_state(self, data: Dict[str, Any]):
        """Import state from backup."""
        with self._lock:
            entry = self._create_entry(
                EntryType.RESTORE,
                "_restore_",
                data.get("state", {}),
                {"imported_from": data.get("exported_at")}
            )
            self._apply_entry(entry)

    def get_stats(self) -> Dict[str, Any]:
        """Get ledger statistics."""
        return {
            "ledger_type": self.ledger_type.value,
            "entry_count": self._entry_counter,
            "state_keys": len(self._state),
            "memory_entries": len(self._entries),
            "last_hash": self._last_hash,
            "session_id": self.session_id,
        }


class LedgerManager:
    """
    Manages multiple continuity ledgers.

    Provides unified interface for all ledger types.
    """

    def __init__(self, base_path: Path, session_id: Optional[str] = None):
        """
        Initialize ledger manager.

        Args:
            base_path: Base directory for all ledgers
            session_id: Session identifier to use
        """
        self.base_path = base_path
        self.session_id = session_id or f"session_{int(time.time() * 1000)}"

        self._ledgers: Dict[LedgerType, ContinuityLedger] = {}

        # Initialize all ledger types
        for ledger_type in LedgerType:
            self._ledgers[ledger_type] = ContinuityLedger(
                ledger_type=ledger_type,
                base_path=base_path,
                session_id=self.session_id,
            )

    def get_ledger(self, ledger_type: LedgerType) -> ContinuityLedger:
        """Get a specific ledger."""
        return self._ledgers[ledger_type]

    @property
    def task(self) -> ContinuityLedger:
        """Task execution ledger."""
        return self._ledgers[LedgerType.TASK]

    @property
    def learning(self) -> ContinuityLedger:
        """Learning patterns ledger."""
        return self._ledgers[LedgerType.LEARNING]

    @property
    def skill(self) -> ContinuityLedger:
        """Skills ledger."""
        return self._ledgers[LedgerType.SKILL]

    @property
    def context(self) -> ContinuityLedger:
        """Context summaries ledger."""
        return self._ledgers[LedgerType.CONTEXT]

    @property
    def error(self) -> ContinuityLedger:
        """Error patterns ledger."""
        return self._ledgers[LedgerType.ERROR]

    def export_all(self) -> Dict[str, Any]:
        """Export all ledger states."""
        return {
            ledger_type.value: ledger.export_state()
            for ledger_type, ledger in self._ledgers.items()
        }

    def verify_all(self) -> Dict[str, Tuple[bool, Optional[str]]]:
        """Verify integrity of all ledgers."""
        return {
            ledger_type.value: ledger.verify_integrity()
            for ledger_type, ledger in self._ledgers.items()
        }

    def get_all_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics for all ledgers."""
        return {
            ledger_type.value: ledger.get_stats()
            for ledger_type, ledger in self._ledgers.items()
        }


# Global manager instance
_manager: Optional[LedgerManager] = None


def get_ledger_manager(base_path: Optional[Path] = None) -> LedgerManager:
    """Get or create the global ledger manager."""
    global _manager
    if _manager is None:
        if base_path is None:
            base_path = Path.home() / ".usf" / "ledgers"
        _manager = LedgerManager(base_path=base_path)
    return _manager


# CLI for testing
if __name__ == "__main__":
    import tempfile

    print("Continuity Ledger Test")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        base_path = Path(tmpdir)

        # Test single ledger
        print("\n1. Single Ledger Test")
        ledger = ContinuityLedger(
            ledger_type=LedgerType.TASK,
            base_path=base_path,
            session_id="test_session"
        )

        # Add some entries
        ledger.set("task_001", {"status": "completed", "confidence": 0.95})
        ledger.set("task_002", {"status": "in_progress", "confidence": 0.0})
        ledger.set("task_001", {"status": "completed", "confidence": 0.97})  # Update

        print(f"   Keys: {ledger.keys()}")
        print(f"   task_001: {ledger.get('task_001')}")

        # Check history
        history = ledger.get_history("task_001")
        print(f"   task_001 history: {len(history)} entries")

        # Verify integrity
        valid, error = ledger.verify_integrity()
        print(f"   Integrity: {'OK' if valid else error}")

        # Test ledger manager
        print("\n2. Ledger Manager Test")
        manager = LedgerManager(base_path=base_path, session_id="manager_test")

        # Use different ledgers
        manager.task.set("execution_001", {"result": "success"})
        manager.learning.set("pattern_001", {"domain": "security", "archetype": "ARC-AD"})
        manager.skill.set("skill_001", {"name": "sql_injection_detection"})
        manager.error.set("error_001", {"type": "timeout", "count": 3})

        # Get all stats
        print("   All ledger stats:")
        stats = manager.get_all_stats()
        for ledger_type, stat in stats.items():
            print(f"     {ledger_type}: {stat['state_keys']} keys, {stat['entry_count']} entries")

        # Verify all
        integrity = manager.verify_all()
        all_valid = all(v[0] for v in integrity.values())
        print(f"   All ledgers valid: {all_valid}")

        # Test persistence
        print("\n3. Persistence Test")
        # Create new manager with same path (simulates new session)
        manager2 = LedgerManager(base_path=base_path, session_id="new_session")

        # Should restore previous state
        print(f"   Restored task keys: {manager2.task.keys()}")
        print(f"   Restored learning keys: {manager2.learning.keys()}")
        print(f"   execution_001: {manager2.task.get('execution_001')}")

        print("\n4. Export/Import Test")
        export = manager2.export_all()
        print(f"   Exported {len(export)} ledgers")

        print("\nTest complete!")
