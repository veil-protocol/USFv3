"""
Circuit Breaker Pattern for USF Agent Execution.

USF 7.0 Implementation - Prevents cascading failures and provides graceful degradation.

Based on patterns from:
- claude-flow: Error recovery patterns
- Standard circuit breaker pattern (Netflix Hystrix)

States:
- CLOSED: Normal operation, requests pass through
- OPEN: Circuit tripped, requests fail fast
- HALF_OPEN: Testing if service recovered

Thresholds:
- 5 consecutive failures → OPEN state
- 5 minute backoff in OPEN state
- 3 successful requests in HALF_OPEN → CLOSED
"""

import asyncio
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, TypeVar, Generic
import logging

logger = logging.getLogger(__name__)

T = TypeVar("T")


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing fast
    HALF_OPEN = "half_open"  # Testing recovery


@dataclass
class CircuitStats:
    """Statistics for a circuit breaker."""
    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    rejected_calls: int = 0  # Failed fast in OPEN state
    last_failure_time: Optional[datetime] = None
    last_success_time: Optional[datetime] = None
    consecutive_failures: int = 0
    consecutive_successes: int = 0
    state_changes: List[tuple] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        if self.total_calls == 0:
            return 1.0
        return self.successful_calls / self.total_calls

    @property
    def failure_rate(self) -> float:
        if self.total_calls == 0:
            return 0.0
        return self.failed_calls / self.total_calls


class CircuitBreaker(Generic[T]):
    """
    Circuit breaker for protecting against cascading failures.

    Usage:
        breaker = CircuitBreaker("agent_spawn")

        async def spawn_agent():
            async with breaker:
                return await actual_spawn()

        # Or functional style:
        result = await breaker.execute(actual_spawn)
    """

    def __init__(
        self,
        name: str,
        failure_threshold: int = 5,
        recovery_timeout: float = 300.0,  # 5 minutes
        success_threshold: int = 3,
        half_open_max_calls: int = 3,
    ):
        """
        Initialize circuit breaker.

        Args:
            name: Identifier for this circuit
            failure_threshold: Consecutive failures to trip circuit
            recovery_timeout: Seconds before attempting recovery
            success_threshold: Successes in HALF_OPEN to close circuit
            half_open_max_calls: Max concurrent calls in HALF_OPEN state
        """
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold
        self.half_open_max_calls = half_open_max_calls

        self._state = CircuitState.CLOSED
        self._last_state_change = datetime.now()
        self._stats = CircuitStats()
        self._half_open_calls = 0
        self._lock = asyncio.Lock()

    @property
    def state(self) -> CircuitState:
        """Get current circuit state, checking for timeout recovery."""
        if self._state == CircuitState.OPEN:
            # Check if recovery timeout has elapsed
            elapsed = (datetime.now() - self._last_state_change).total_seconds()
            if elapsed >= self.recovery_timeout:
                self._transition_to(CircuitState.HALF_OPEN)
        return self._state

    @property
    def stats(self) -> CircuitStats:
        """Get circuit statistics."""
        return self._stats

    def _transition_to(self, new_state: CircuitState):
        """Transition to a new state."""
        old_state = self._state
        self._state = new_state
        self._last_state_change = datetime.now()

        if new_state == CircuitState.HALF_OPEN:
            self._half_open_calls = 0

        self._stats.state_changes.append((
            datetime.now().isoformat(),
            old_state.value,
            new_state.value
        ))

        logger.info(f"CircuitBreaker[{self.name}]: {old_state.value} → {new_state.value}")

    def _record_success(self):
        """Record a successful call."""
        self._stats.total_calls += 1
        self._stats.successful_calls += 1
        self._stats.consecutive_successes += 1
        self._stats.consecutive_failures = 0
        self._stats.last_success_time = datetime.now()

        if self._state == CircuitState.HALF_OPEN:
            if self._stats.consecutive_successes >= self.success_threshold:
                self._transition_to(CircuitState.CLOSED)

    def _record_failure(self, error: Exception):
        """Record a failed call."""
        self._stats.total_calls += 1
        self._stats.failed_calls += 1
        self._stats.consecutive_failures += 1
        self._stats.consecutive_successes = 0
        self._stats.last_failure_time = datetime.now()

        if self._state == CircuitState.CLOSED:
            if self._stats.consecutive_failures >= self.failure_threshold:
                self._transition_to(CircuitState.OPEN)
        elif self._state == CircuitState.HALF_OPEN:
            # Any failure in HALF_OPEN returns to OPEN
            self._transition_to(CircuitState.OPEN)

    def _record_rejection(self):
        """Record a rejected call (failed fast)."""
        self._stats.total_calls += 1
        self._stats.rejected_calls += 1

    async def execute(
        self,
        func: Callable[[], T],
        fallback: Optional[Callable[[], T]] = None
    ) -> T:
        """
        Execute function through circuit breaker.

        Args:
            func: Async function to execute
            fallback: Optional fallback if circuit is open

        Returns:
            Result from func or fallback

        Raises:
            CircuitOpenError: If circuit is open and no fallback provided
        """
        current_state = self.state  # Triggers timeout check

        if current_state == CircuitState.OPEN:
            self._record_rejection()
            if fallback:
                logger.debug(f"CircuitBreaker[{self.name}]: Using fallback (circuit OPEN)")
                return await fallback() if asyncio.iscoroutinefunction(fallback) else fallback()
            raise CircuitOpenError(
                f"Circuit {self.name} is OPEN. "
                f"Retry after {self.recovery_timeout - (datetime.now() - self._last_state_change).total_seconds():.0f}s"
            )

        if current_state == CircuitState.HALF_OPEN:
            async with self._lock:
                if self._half_open_calls >= self.half_open_max_calls:
                    self._record_rejection()
                    if fallback:
                        return await fallback() if asyncio.iscoroutinefunction(fallback) else fallback()
                    raise CircuitOpenError(f"Circuit {self.name} HALF_OPEN limit reached")
                self._half_open_calls += 1

        try:
            result = await func() if asyncio.iscoroutinefunction(func) else func()
            self._record_success()
            return result
        except Exception as e:
            self._record_failure(e)
            raise

    async def __aenter__(self):
        """Context manager entry - check circuit state."""
        current_state = self.state

        if current_state == CircuitState.OPEN:
            self._record_rejection()
            raise CircuitOpenError(f"Circuit {self.name} is OPEN")

        if current_state == CircuitState.HALF_OPEN:
            async with self._lock:
                if self._half_open_calls >= self.half_open_max_calls:
                    self._record_rejection()
                    raise CircuitOpenError(f"Circuit {self.name} HALF_OPEN limit reached")
                self._half_open_calls += 1

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - record result."""
        if exc_type is None:
            self._record_success()
        else:
            self._record_failure(exc_val)
        return False  # Don't suppress exceptions

    def reset(self):
        """Manually reset circuit to CLOSED state."""
        self._transition_to(CircuitState.CLOSED)
        self._stats.consecutive_failures = 0
        self._stats.consecutive_successes = 0

    def force_open(self):
        """Manually open circuit (for testing or emergency)."""
        self._transition_to(CircuitState.OPEN)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize circuit state for monitoring."""
        return {
            "name": self.name,
            "state": self._state.value,
            "stats": {
                "total_calls": self._stats.total_calls,
                "successful_calls": self._stats.successful_calls,
                "failed_calls": self._stats.failed_calls,
                "rejected_calls": self._stats.rejected_calls,
                "success_rate": f"{self._stats.success_rate:.1%}",
                "consecutive_failures": self._stats.consecutive_failures,
            },
            "config": {
                "failure_threshold": self.failure_threshold,
                "recovery_timeout": self.recovery_timeout,
                "success_threshold": self.success_threshold,
            },
            "last_state_change": self._last_state_change.isoformat(),
        }


class CircuitOpenError(Exception):
    """Raised when circuit is open and request is rejected."""
    pass


# ============================================================================
# CIRCUIT BREAKER REGISTRY
# ============================================================================

class CircuitBreakerRegistry:
    """
    Global registry of circuit breakers.

    Provides centralized management and monitoring.
    """

    def __init__(self):
        self._breakers: Dict[str, CircuitBreaker] = {}

    def get_or_create(
        self,
        name: str,
        failure_threshold: int = 5,
        recovery_timeout: float = 300.0,
        **kwargs
    ) -> CircuitBreaker:
        """Get existing or create new circuit breaker."""
        if name not in self._breakers:
            self._breakers[name] = CircuitBreaker(
                name=name,
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                **kwargs
            )
        return self._breakers[name]

    def get(self, name: str) -> Optional[CircuitBreaker]:
        """Get circuit breaker by name."""
        return self._breakers.get(name)

    def all(self) -> Dict[str, CircuitBreaker]:
        """Get all circuit breakers."""
        return self._breakers.copy()

    def status(self) -> Dict[str, Dict]:
        """Get status of all circuit breakers."""
        return {name: cb.to_dict() for name, cb in self._breakers.items()}

    def reset_all(self):
        """Reset all circuit breakers."""
        for cb in self._breakers.values():
            cb.reset()


# Global registry instance
_registry = CircuitBreakerRegistry()


def get_breaker(
    name: str,
    failure_threshold: int = 5,
    recovery_timeout: float = 300.0,
    **kwargs
) -> CircuitBreaker:
    """Get or create a circuit breaker from the global registry."""
    return _registry.get_or_create(name, failure_threshold, recovery_timeout, **kwargs)


def get_registry() -> CircuitBreakerRegistry:
    """Get the global circuit breaker registry."""
    return _registry


# ============================================================================
# PREDEFINED BREAKERS FOR USF COMPONENTS
# ============================================================================

# Agent spawning circuit
AGENT_SPAWN_BREAKER = "agent_spawn"

# RAG retrieval circuit
RAG_RETRIEVAL_BREAKER = "rag_retrieval"

# External API circuit
EXTERNAL_API_BREAKER = "external_api"

# Shell execution circuit
SHELL_EXEC_BREAKER = "shell_exec"


def get_agent_breaker() -> CircuitBreaker:
    """Get circuit breaker for agent spawning."""
    return get_breaker(AGENT_SPAWN_BREAKER, failure_threshold=5, recovery_timeout=300)


def get_rag_breaker() -> CircuitBreaker:
    """Get circuit breaker for RAG retrieval."""
    return get_breaker(RAG_RETRIEVAL_BREAKER, failure_threshold=3, recovery_timeout=60)


def get_api_breaker() -> CircuitBreaker:
    """Get circuit breaker for external APIs."""
    return get_breaker(EXTERNAL_API_BREAKER, failure_threshold=5, recovery_timeout=120)


def get_shell_breaker() -> CircuitBreaker:
    """Get circuit breaker for shell execution."""
    return get_breaker(SHELL_EXEC_BREAKER, failure_threshold=10, recovery_timeout=60)


# CLI for testing
if __name__ == "__main__":
    import random

    async def test():
        print("Circuit Breaker Test")
        print("=" * 60)

        breaker = CircuitBreaker("test", failure_threshold=3, recovery_timeout=5)

        async def flaky_operation(fail_rate: float = 0.5):
            await asyncio.sleep(0.1)
            if random.random() < fail_rate:
                raise Exception("Random failure")
            return "success"

        # Test normal operation
        print("\n1. Normal operation (low failure rate)")
        for i in range(5):
            try:
                result = await breaker.execute(lambda: flaky_operation(0.1))
                print(f"  Call {i+1}: {result}")
            except Exception as e:
                print(f"  Call {i+1}: Error - {e}")

        print(f"\n  State: {breaker.state.value}")
        print(f"  Stats: {breaker.stats.success_rate:.0%} success rate")

        # Test circuit tripping
        print("\n2. High failure rate (should trip circuit)")
        breaker.reset()
        for i in range(10):
            try:
                result = await breaker.execute(lambda: flaky_operation(0.9))
                print(f"  Call {i+1}: {result}")
            except CircuitOpenError as e:
                print(f"  Call {i+1}: REJECTED - {e}")
            except Exception as e:
                print(f"  Call {i+1}: Failed - {e}")

        print(f"\n  State: {breaker.state.value}")
        print(f"  Consecutive failures: {breaker.stats.consecutive_failures}")

        # Test fallback
        print("\n3. Testing fallback")
        try:
            result = await breaker.execute(
                lambda: flaky_operation(1.0),
                fallback=lambda: "fallback_value"
            )
            print(f"  Result: {result}")
        except Exception as e:
            print(f"  Error: {e}")

        # Test recovery
        print("\n4. Wait for recovery timeout")
        await asyncio.sleep(6)  # Wait for 5s recovery timeout + margin
        print(f"  State after timeout: {breaker.state.value}")

        # Test HALF_OPEN state
        print("\n5. HALF_OPEN recovery test")
        for i in range(5):
            try:
                result = await breaker.execute(lambda: flaky_operation(0.0))
                print(f"  Call {i+1}: {result}, State: {breaker.state.value}")
            except Exception as e:
                print(f"  Call {i+1}: Error - {e}")

        print("\n" + "=" * 60)
        print("Final status:", breaker.to_dict())

    asyncio.run(test())
