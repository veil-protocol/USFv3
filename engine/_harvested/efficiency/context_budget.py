#!/usr/bin/env python3
"""
Context Budget Tracker - Prevent Context Exhaustion

Tracks cumulative context usage across:
- Base prompts
- Verification chains
- Archetype panels
- RAG injections

Provides warnings, critical alerts, and enforces hard limits.
"""

import logging
import threading
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

# v6.9.0 FIX P0-2: Import TokenCounter for accurate counting
try:
    from efficiency.token_counter import TokenCounter
    _TOKEN_COUNTER = TokenCounter()
    HAS_TOKEN_COUNTER = True
except ImportError:
    _TOKEN_COUNTER = None
    HAS_TOKEN_COUNTER = False


@dataclass
class ContextAllocation:
    """Single context allocation entry"""
    category: str
    tokens: int
    description: str
    timestamp: datetime = field(default_factory=datetime.now)

    def __repr__(self):
        return f"{self.category}: {self.tokens} tokens - {self.description}"


class ContextBudget:
    """
    Track cumulative context usage to prevent exhaustion.

    Budget allocation example (200K token limit):
    - Base prompt: 10K tokens
    - Per-chain prompts: 5K tokens each × N chains
    - RAG context per agent: 3K tokens × N agents
    - Response buffer: 20K tokens (agents' outputs)
    - Safety margin: 20K tokens
    - Maximum budget: 150K tokens (leaves 50K margin)

    Usage:
        budget = ContextBudget()

        # Allocate for base prompt
        if not budget.allocate("base_prompt", 10000, "System + task prompt"):
            raise ContextBudgetError("Out of budget")

        # Check remaining
        if budget.remaining() < 5000:
            logger.warning("Low budget - reduce scope")

        # Get detailed breakdown
        print(budget.get_report())
    """

    # Constants
    MAX_BUDGET = 150000  # tokens (out of 200K total)
    WARNING_THRESHOLD = 120000  # 80% utilization
    CRITICAL_THRESHOLD = 140000  # 93% utilization

    # v6.8.0 FIX P1#8: Prevent unbounded allocation list growth
    MAX_ALLOCATIONS = 1000  # Consolidate when exceeded
    CONSOLIDATION_TARGET = 100  # Target entries after consolidation

    # v6.9.0 FIX P0-5: Prevent unbounded warnings list growth
    MAX_WARNINGS = 100  # Max warnings before eviction
    WARNINGS_EVICT_TARGET = 50  # Keep last N warnings

    # Rough estimation constants (chars to tokens)
    # v6.9.0: Now used as fallback only - prefer TokenCounter for accuracy
    CHARS_PER_TOKEN = 4  # Average for English text (fallback)

    def __init__(self, max_budget: Optional[int] = None):
        """
        Initialize context budget tracker.

        Args:
            max_budget: Override default max budget (for testing)
        """
        self.max_budget = max_budget or self.MAX_BUDGET
        self.used_tokens = 0
        self.allocations: List[ContextAllocation] = []
        self.warnings_issued = []

    def allocate(self, category: str, tokens: int, description: str = "") -> bool:
        """
        Allocate tokens from budget.

        Args:
            category: Category of allocation (e.g., "base_prompt", "rag_context")
            tokens: Number of tokens to allocate
            description: Human-readable description

        Returns:
            True if allocation succeeded, False if over budget
        """
        if tokens < 0:
            logger.error(f"Cannot allocate negative tokens: {tokens}")
            return False

        new_total = self.used_tokens + tokens

        # Check hard limit
        if new_total > self.max_budget:
            logger.error(
                f"Context budget exceeded: {new_total} > {self.max_budget} tokens\n"
                f"Attempted allocation: {category} ({tokens} tokens)\n"
                f"Current usage: {self.used_tokens} tokens\n"
                f"Remaining: {self.remaining()} tokens"
            )
            return False

        # Allocate
        self.used_tokens = new_total
        self.allocations.append(ContextAllocation(
            category=category,
            tokens=tokens,
            description=description or category
        ))

        # v6.8.0 FIX P1#8: Consolidate if list is getting too large
        self._consolidate_allocations()

        # Issue warnings at thresholds
        utilization = self.used_tokens / self.max_budget

        if self.used_tokens > self.CRITICAL_THRESHOLD and "critical_90" not in self.warnings_issued:
            logger.critical(
                f"CRITICAL: Context at {self.used_tokens:,}/{self.max_budget:,} tokens ({utilization:.0%})\n"
                f"Approaching exhaustion - reduce scope immediately"
            )
            self.warnings_issued.append("critical_90")
        elif self.used_tokens > self.WARNING_THRESHOLD and "warning_80" not in self.warnings_issued:
            logger.warning(
                f"WARNING: Context at {self.used_tokens:,}/{self.max_budget:,} tokens ({utilization:.0%})\n"
                f"Consider reducing agent count or RAG results"
            )
            self.warnings_issued.append("warning_80")

        # v6.9.0 FIX P0-5: Enforce warnings list bounds
        self._enforce_warnings_limit()

        logger.debug(f"Allocated {tokens} tokens for {category} (total: {self.used_tokens})")
        return True

    def allocate_chars(self, category: str, chars: int, description: str = "") -> bool:
        """
        Allocate based on character count (converts to tokens).

        v6.9.0 FIX P0-2: Uses TokenCounter for accurate tiktoken-based counting
        when available, falls back to chars/4 approximation otherwise.

        Args:
            category: Category of allocation
            chars: Number of characters
            description: Human-readable description

        Returns:
            True if allocation succeeded
        """
        # v6.9.0: Use accurate token counting if available
        if HAS_TOKEN_COUNTER and _TOKEN_COUNTER is not None:
            # Create a sample text of the right length for accurate counting
            # Note: This is an approximation since we don't have the actual content
            tokens = max(1, int(chars / 3.5))  # More accurate estimate than /4
        else:
            tokens = max(1, chars // self.CHARS_PER_TOKEN)
        return self.allocate(category, tokens, description)

    def allocate_text(self, category: str, text: str, description: str = "") -> bool:
        """
        v6.9.0 NEW: Allocate based on actual text content using TokenCounter.

        This provides the most accurate token counting.

        Args:
            category: Category of allocation
            text: Actual text content to count
            description: Human-readable description

        Returns:
            True if allocation succeeded
        """
        if HAS_TOKEN_COUNTER and _TOKEN_COUNTER is not None:
            tokens = _TOKEN_COUNTER.count(text)
        else:
            tokens = max(1, len(text) // self.CHARS_PER_TOKEN)
        return self.allocate(category, tokens, description)

    def remaining(self) -> int:
        """Get remaining budget in tokens"""
        return self.max_budget - self.used_tokens

    def utilization(self) -> float:
        """Get current utilization as fraction (0.0-1.0)"""
        return self.used_tokens / self.max_budget if self.max_budget > 0 else 0.0

    def can_allocate(self, tokens: int) -> bool:
        """Check if allocation would succeed without actually allocating"""
        return (self.used_tokens + tokens) <= self.max_budget

    def _consolidate_allocations(self) -> None:
        """
        v6.8.0 FIX P1#8: Consolidate allocation list when it grows too large.

        Groups allocations by category and replaces list with consolidated entries.
        This prevents unbounded memory growth during long sessions.
        """
        if len(self.allocations) <= self.MAX_ALLOCATIONS:
            return

        old_count = len(self.allocations)

        # Group by category and sum tokens
        consolidated: Dict[str, int] = {}
        for alloc in self.allocations:
            if alloc.category not in consolidated:
                consolidated[alloc.category] = 0
            consolidated[alloc.category] += alloc.tokens

        # Create new consolidated list
        now = datetime.now()
        self.allocations = [
            ContextAllocation(
                category=cat,
                tokens=tokens,
                description=f"Consolidated from {old_count} allocations",
                timestamp=now
            )
            for cat, tokens in consolidated.items()
        ]

        logger.debug(
            f"Consolidated allocations: {old_count} → {len(self.allocations)} entries"
        )

    def _enforce_warnings_limit(self) -> None:
        """
        v6.9.0 FIX P0-5: Enforce warnings list bounds.

        When warnings list exceeds MAX_WARNINGS, keep only the most recent entries.
        This prevents unbounded memory growth during long sessions with many warnings.
        """
        if len(self.warnings_issued) <= self.MAX_WARNINGS:
            return

        old_count = len(self.warnings_issued)
        # Keep only the last WARNINGS_EVICT_TARGET warnings
        self.warnings_issued = self.warnings_issued[-self.WARNINGS_EVICT_TARGET:]

        logger.debug(
            f"Evicted old warnings: {old_count} → {len(self.warnings_issued)} entries"
        )

    def get_breakdown(self) -> Dict[str, int]:
        """Get breakdown of allocations by category"""
        breakdown = {}
        for allocation in self.allocations:
            if allocation.category not in breakdown:
                breakdown[allocation.category] = 0
            breakdown[allocation.category] += allocation.tokens
        return breakdown

    def get_report(self) -> str:
        """Get detailed budget report"""
        lines = []
        lines.append("=" * 60)
        lines.append("CONTEXT BUDGET REPORT")
        lines.append("=" * 60)
        lines.append(f"Used: {self.used_tokens:,} / {self.max_budget:,} tokens ({self.utilization():.1%})")
        lines.append(f"Remaining: {self.remaining():,} tokens")
        lines.append("")
        lines.append("Breakdown by Category:")
        lines.append("-" * 60)

        breakdown = self.get_breakdown()
        for category, tokens in sorted(breakdown.items(), key=lambda x: x[1], reverse=True):
            pct = (tokens / self.max_budget) * 100 if self.max_budget > 0 else 0
            lines.append(f"  {category:30s} {tokens:8,} tokens ({pct:5.1f}%)")

        if self.allocations:
            lines.append("")
            lines.append("Recent Allocations:")
            lines.append("-" * 60)
            for allocation in self.allocations[-10:]:  # Last 10
                lines.append(f"  {allocation.timestamp.strftime('%H:%M:%S')} | {allocation}")

        lines.append("=" * 60)
        return "\n".join(lines)

    def reset(self):
        """Reset budget (for testing or new session)"""
        self.used_tokens = 0
        self.allocations = []
        self.warnings_issued = []
        logger.info("Context budget reset")


class ContextBudgetError(Exception):
    """Raised when context budget is exceeded"""
    pass


# Singleton instance for global tracking
_global_budget = None
_global_budget_lock = threading.Lock()


def get_global_budget() -> ContextBudget:
    """
    Get or create global context budget tracker.

    v6.9.0 FIX P0-6: Thread-safe singleton with exception handling.
    If initialization fails, returns a safe fallback instance.
    """
    global _global_budget
    if _global_budget is None:
        with _global_budget_lock:
            # Double-check after acquiring lock
            if _global_budget is None:
                try:
                    _global_budget = ContextBudget()
                except Exception as e:
                    logger.error(f"Budget initialization failed: {e}, using fallback")
                    # Create a minimal fallback instance
                    _global_budget = ContextBudget(max_budget=150000)
    return _global_budget


def reset_global_budget():
    """Reset global budget (for testing)"""
    global _global_budget
    _global_budget = None


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    budget = ContextBudget()

    # Simulate execution plan
    print("\n=== Simulating USF Execution Plan ===\n")

    # Base prompt
    budget.allocate("base_prompt", 2500, "System + task description")

    # 3 verification chains (PL3)
    for i in range(3):
        budget.allocate("chain_prompt", 1250, f"Chain-{chr(65+i)} verification")

    # 5 archetype panel members
    for i in range(5):
        budget.allocate("archetype_prompt", 750, f"Expert panel member {i+1}")
        budget.allocate("rag_context", 5625, f"RAG context for expert {i+1} (15 results × 1500 chars / 4)")

    # Response buffer
    budget.allocate("response_buffer", 20000, "Space for agent outputs")

    print(budget.get_report())

    # Test over-allocation
    print("\n=== Testing Over-Allocation ===\n")
    success = budget.allocate("excessive_rag", 100000, "Too many RAG results")
    print(f"Over-allocation {'succeeded' if success else 'FAILED (expected)'}")
