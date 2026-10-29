"""
Claims-Based Task Ownership for USF Multi-Agent Execution.

USF 7.0 Implementation - Prevents duplicate work and enables task stealing.

Based on patterns from:
- claude-flow: Task coordination
- Distributed systems: Work stealing queues

States:
- UNCLAIMED: Available for any agent to claim
- CLAIMED: Owned by an agent, in progress
- STEALABLE: Timed out, can be stolen by another agent
- COMPLETED: Successfully finished
- FAILED: Failed after max retries

Key features:
- Atomic claim/release operations
- Timeout-based automatic release
- Work stealing for load balancing
- Duplicate prevention
"""

import asyncio
import time
import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class TaskState(Enum):
    """Task ownership states."""
    UNCLAIMED = "unclaimed"
    CLAIMED = "claimed"
    STEALABLE = "stealable"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class TaskClaim:
    """A claimed task with ownership metadata."""
    task_id: str
    task_hash: str  # Content hash for deduplication
    description: str
    state: TaskState
    owner_id: Optional[str] = None
    claimed_at: Optional[datetime] = None
    timeout_seconds: float = 300.0  # 5 minute default
    attempts: int = 0
    max_attempts: int = 3
    result: Optional[Any] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_timed_out(self) -> bool:
        """Check if claim has timed out."""
        if self.state != TaskState.CLAIMED or not self.claimed_at:
            return False
        elapsed = (datetime.now() - self.claimed_at).total_seconds()
        return elapsed > self.timeout_seconds

    @property
    def can_be_stolen(self) -> bool:
        """Check if task can be stolen by another agent."""
        return self.state == TaskState.STEALABLE or (
            self.state == TaskState.CLAIMED and self.is_timed_out
        )

    @property
    def is_available(self) -> bool:
        """Check if task is available for claiming."""
        return self.state == TaskState.UNCLAIMED or self.can_be_stolen

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "task_id": self.task_id,
            "task_hash": self.task_hash,
            "description": self.description,
            "state": self.state.value,
            "owner_id": self.owner_id,
            "claimed_at": self.claimed_at.isoformat() if self.claimed_at else None,
            "timeout_seconds": self.timeout_seconds,
            "attempts": self.attempts,
            "max_attempts": self.max_attempts,
            "error": self.error,
            "metadata": self.metadata,
        }


class TaskClaimManager:
    """
    Manages task ownership claims across agents.

    Provides atomic operations for:
    - Claiming tasks
    - Releasing claims
    - Stealing timed-out tasks
    - Completing/failing tasks
    - Preventing duplicate work
    """

    def __init__(
        self,
        default_timeout: float = 300.0,
        max_attempts: int = 3,
        persistence_path: Optional[Path] = None
    ):
        self.default_timeout = default_timeout
        self.max_attempts = max_attempts
        self.persistence_path = persistence_path

        self._claims: Dict[str, TaskClaim] = {}
        self._hash_to_id: Dict[str, str] = {}  # For deduplication
        self._lock = asyncio.Lock()

        if persistence_path:
            self._load_claims()

    def _compute_hash(self, description: str) -> str:
        """Compute content hash for deduplication."""
        return hashlib.sha256(description.encode()).hexdigest()[:16]

    def _load_claims(self):
        """Load persisted claims."""
        if not self.persistence_path or not self.persistence_path.exists():
            return

        try:
            with open(self.persistence_path, "r") as f:
                data = json.load(f)
                for claim_data in data.get("claims", []):
                    claim = TaskClaim(
                        task_id=claim_data["task_id"],
                        task_hash=claim_data["task_hash"],
                        description=claim_data["description"],
                        state=TaskState(claim_data["state"]),
                        owner_id=claim_data.get("owner_id"),
                        claimed_at=datetime.fromisoformat(claim_data["claimed_at"]) if claim_data.get("claimed_at") else None,
                        timeout_seconds=claim_data.get("timeout_seconds", self.default_timeout),
                        attempts=claim_data.get("attempts", 0),
                        max_attempts=claim_data.get("max_attempts", self.max_attempts),
                        error=claim_data.get("error"),
                        metadata=claim_data.get("metadata", {}),
                    )
                    self._claims[claim.task_id] = claim
                    self._hash_to_id[claim.task_hash] = claim.task_id
        except Exception as e:
            logger.warning(f"Failed to load claims: {e}")

    def _save_claims(self):
        """Persist claims to disk."""
        if not self.persistence_path:
            return

        self.persistence_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "version": "1.0",
            "updated_at": datetime.now().isoformat(),
            "claims": [c.to_dict() for c in self._claims.values()]
        }
        with open(self.persistence_path, "w") as f:
            json.dump(data, f, indent=2)

    async def register_task(
        self,
        task_id: str,
        description: str,
        timeout_seconds: Optional[float] = None,
        metadata: Optional[Dict] = None
    ) -> TaskClaim:
        """
        Register a new task for claiming.

        Returns existing claim if task already registered (deduplication).
        """
        async with self._lock:
            task_hash = self._compute_hash(description)

            # Check for duplicate
            if task_hash in self._hash_to_id:
                existing_id = self._hash_to_id[task_hash]
                return self._claims[existing_id]

            claim = TaskClaim(
                task_id=task_id,
                task_hash=task_hash,
                description=description,
                state=TaskState.UNCLAIMED,
                timeout_seconds=timeout_seconds or self.default_timeout,
                max_attempts=self.max_attempts,
                metadata=metadata or {},
            )

            self._claims[task_id] = claim
            self._hash_to_id[task_hash] = task_id
            self._save_claims()

            return claim

    async def claim(
        self,
        task_id: str,
        owner_id: str,
        allow_steal: bool = True
    ) -> Optional[TaskClaim]:
        """
        Attempt to claim a task.

        Returns the claim if successful, None if task unavailable.
        """
        async with self._lock:
            if task_id not in self._claims:
                return None

            claim = self._claims[task_id]

            # Check if available
            if not claim.is_available:
                if not (allow_steal and claim.can_be_stolen):
                    return None

            # Check max attempts
            if claim.attempts >= claim.max_attempts:
                claim.state = TaskState.FAILED
                claim.error = f"Max attempts ({claim.max_attempts}) exceeded"
                self._save_claims()
                return None

            # Claim it
            claim.state = TaskState.CLAIMED
            claim.owner_id = owner_id
            claim.claimed_at = datetime.now()
            claim.attempts += 1

            self._save_claims()
            logger.debug(f"Task {task_id} claimed by {owner_id} (attempt {claim.attempts})")

            return claim

    async def release(self, task_id: str, owner_id: str) -> bool:
        """
        Release a claim without completing.

        Returns True if released, False if not owned by this agent.
        """
        async with self._lock:
            if task_id not in self._claims:
                return False

            claim = self._claims[task_id]

            if claim.owner_id != owner_id:
                return False

            claim.state = TaskState.UNCLAIMED
            claim.owner_id = None
            claim.claimed_at = None

            self._save_claims()
            return True

    async def complete(
        self,
        task_id: str,
        owner_id: str,
        result: Any = None
    ) -> bool:
        """
        Mark a task as completed.

        Returns True if completed, False if not owned by this agent.
        """
        async with self._lock:
            if task_id not in self._claims:
                return False

            claim = self._claims[task_id]

            if claim.owner_id != owner_id:
                return False

            claim.state = TaskState.COMPLETED
            claim.result = result

            self._save_claims()
            logger.debug(f"Task {task_id} completed by {owner_id}")

            return True

    async def fail(
        self,
        task_id: str,
        owner_id: str,
        error: str
    ) -> bool:
        """
        Mark a task as failed.

        If attempts remain, task becomes UNCLAIMED for retry.
        Otherwise, task becomes FAILED permanently.
        """
        async with self._lock:
            if task_id not in self._claims:
                return False

            claim = self._claims[task_id]

            if claim.owner_id != owner_id:
                return False

            claim.error = error

            if claim.attempts < claim.max_attempts:
                claim.state = TaskState.UNCLAIMED
                claim.owner_id = None
                claim.claimed_at = None
                logger.debug(f"Task {task_id} failed, will retry ({claim.attempts}/{claim.max_attempts})")
            else:
                claim.state = TaskState.FAILED
                logger.debug(f"Task {task_id} failed permanently after {claim.attempts} attempts")

            self._save_claims()
            return True

    async def get_available(self) -> List[TaskClaim]:
        """Get all available tasks."""
        async with self._lock:
            self._update_stealable()
            return [c for c in self._claims.values() if c.is_available]

    async def get_stealable(self) -> List[TaskClaim]:
        """Get all stealable (timed out) tasks."""
        async with self._lock:
            self._update_stealable()
            return [c for c in self._claims.values() if c.can_be_stolen]

    async def get_by_owner(self, owner_id: str) -> List[TaskClaim]:
        """Get all tasks owned by an agent."""
        async with self._lock:
            return [c for c in self._claims.values() if c.owner_id == owner_id]

    def _update_stealable(self):
        """Update timed-out claims to stealable state."""
        for claim in self._claims.values():
            if claim.state == TaskState.CLAIMED and claim.is_timed_out:
                claim.state = TaskState.STEALABLE
                logger.debug(f"Task {claim.task_id} marked stealable (timed out)")

    async def steal_work(self, owner_id: str) -> Optional[TaskClaim]:
        """
        Attempt to steal an available or timed-out task.

        Used for load balancing when an agent finishes early.
        """
        async with self._lock:
            self._update_stealable()

            # Prefer stealable (timed out) tasks first
            for claim in self._claims.values():
                if claim.can_be_stolen:
                    return await self.claim(claim.task_id, owner_id, allow_steal=True)

            # Then try unclaimed tasks
            for claim in self._claims.values():
                if claim.state == TaskState.UNCLAIMED:
                    return await self.claim(claim.task_id, owner_id)

            return None

    def get_stats(self) -> Dict[str, Any]:
        """Get claim statistics."""
        states = {}
        for claim in self._claims.values():
            state = claim.state.value
            states[state] = states.get(state, 0) + 1

        return {
            "total_tasks": len(self._claims),
            "by_state": states,
            "unique_owners": len(set(c.owner_id for c in self._claims.values() if c.owner_id)),
        }

    async def cleanup_completed(self, older_than_seconds: float = 3600):
        """Remove completed tasks older than threshold."""
        async with self._lock:
            cutoff = datetime.now() - timedelta(seconds=older_than_seconds)
            to_remove = []

            for task_id, claim in self._claims.items():
                if claim.state in [TaskState.COMPLETED, TaskState.FAILED]:
                    if claim.claimed_at and claim.claimed_at < cutoff:
                        to_remove.append(task_id)

            for task_id in to_remove:
                claim = self._claims.pop(task_id)
                self._hash_to_id.pop(claim.task_hash, None)

            if to_remove:
                self._save_claims()
                logger.debug(f"Cleaned up {len(to_remove)} old claims")


# Global manager instance
_manager: Optional[TaskClaimManager] = None


def get_claim_manager(
    persistence_path: Optional[Path] = None
) -> TaskClaimManager:
    """Get or create the global claim manager."""
    global _manager
    if _manager is None:
        _manager = TaskClaimManager(persistence_path=persistence_path)
    return _manager


# CLI for testing
if __name__ == "__main__":
    async def test():
        print("Task Claims Test")
        print("=" * 60)

        manager = TaskClaimManager()

        # Register tasks
        task1 = await manager.register_task(
            "task_001",
            "Analyze security vulnerabilities",
            timeout_seconds=2.0  # Short timeout for testing
        )
        task2 = await manager.register_task(
            "task_002",
            "Review authentication code"
        )
        task3 = await manager.register_task(
            "task_003",
            "Analyze security vulnerabilities"  # Duplicate
        )

        print(f"\n1. Registered 3 tasks (1 duplicate)")
        print(f"   task_001: {task1.task_id}")
        print(f"   task_002: {task2.task_id}")
        print(f"   task_003 (dup): {task3.task_id}")  # Should be same as task1

        # Claim tasks
        print("\n2. Agent A claims task_001")
        claim1 = await manager.claim("task_001", "agent_a")
        print(f"   Success: {claim1 is not None}")

        print("\n3. Agent B tries to claim task_001 (should fail)")
        claim1b = await manager.claim("task_001", "agent_b", allow_steal=False)
        print(f"   Success: {claim1b is not None}")

        # Wait for timeout
        print("\n4. Wait for timeout...")
        await asyncio.sleep(2.5)

        print("\n5. Agent B steals timed-out task_001")
        claim1c = await manager.claim("task_001", "agent_b", allow_steal=True)
        print(f"   Success: {claim1c is not None}")
        print(f"   New owner: {claim1c.owner_id if claim1c else 'N/A'}")
        print(f"   Attempts: {claim1c.attempts if claim1c else 'N/A'}")

        # Complete task
        print("\n6. Agent B completes task_001")
        success = await manager.complete("task_001", "agent_b", result="No vulnerabilities found")
        print(f"   Success: {success}")

        # Stats
        print("\n7. Final stats:")
        stats = manager.get_stats()
        for key, value in stats.items():
            print(f"   {key}: {value}")

    asyncio.run(test())
