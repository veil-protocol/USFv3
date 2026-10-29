#!/usr/bin/env python3
"""
ENGINE-11 Integration - Token Efficiency Enforcement

v6.9.0 UPDATE: Now includes TieredLoader integration for 5x token savings.

This module provides a simple API for integrating ENGINE-11 (Token Efficiency)
into the USF execution flow. It wires together:
- ContextBudget: Prevent context exhaustion
- Deduplicator: Avoid sending duplicate content
- TieredLoader: Load context at appropriate granularity (v6.9.0)

Usage:
    from efficiency.integration import (
        check_budget_before_spawn,
        allocate_for_agents,
        reset_session_budget,
        get_deduplicator,
        deduplicate_context,
        # v6.9.0: Tiered loading
        get_tiered_loader,
        load_tiered_context,
        MAX_FALLBACK_RAG_RESULTS
    )

    # Before spawning agents
    can_proceed, recommended = check_budget_before_spawn(num_agents=5)
    if not can_proceed:
        print(f"Budget constraint: reduce to {recommended} agents")

    # Allocate budget
    if allocate_for_agents(num_agents=5):
        # Spawn agents...
        pass

    # Deduplicate RAG results before sending
    unique_results = deduplicate_context(rag_results)

    # v6.9.0: Load context with tiered granularity
    items = [("path/to/file.md", 0.85), ("path/to/other.md", 0.45)]
    tiered = load_tiered_context(items, total_budget=50000)

    # New session
    reset_session_budget()
"""

import logging
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any

from .context_budget import get_global_budget, ContextBudget
from .deduplication import Deduplicator

# v6.9.0 FIX P0-1: Import TieredLoader for context tiering
try:
    from .tiered_loader import TieredLoader, ContextTier, LoadedContext
    HAS_TIERED_LOADER = True
except ImportError:
    HAS_TIERED_LOADER = False
    TieredLoader = None
    ContextTier = None
    LoadedContext = None

logger = logging.getLogger(__name__)

# Global deduplicator instance (lazy initialization)
_deduplicator: Optional[Deduplicator] = None

# v6.9.0 FIX P0-1: Global TieredLoader instance (lazy initialization)
_tiered_loader: Optional[TieredLoader] = None

# Default vault path for deduplicator
DEFAULT_VAULT_PATH = "/Users/sidious_transit/Desktop/Sharedv2/obsidian-vault4"

# v6.9.0 FIX P0-4: Cap RAG fallback results to prevent context exhaustion
MAX_FALLBACK_RAG_RESULTS = 15


def get_deduplicator(vault_path: Optional[str] = None) -> Deduplicator:
    """
    Get or create global deduplicator instance.

    Args:
        vault_path: Path to Obsidian vault (optional, uses default if not provided)

    Returns:
        Deduplicator instance for the session
    """
    global _deduplicator
    if _deduplicator is None:
        path = vault_path or DEFAULT_VAULT_PATH
        if Path(path).exists():
            _deduplicator = Deduplicator(vault_path=path)
            logger.debug(f"Initialized deduplicator with vault: {path}")
        else:
            # Fallback: create with temp directory if vault doesn't exist
            import tempfile
            temp_path = tempfile.mkdtemp(prefix="usf_dedup_")
            _deduplicator = Deduplicator(vault_path=temp_path)
            logger.warning(f"Vault not found at {path}, using temp: {temp_path}")
    return _deduplicator


def get_tiered_loader(vault_path: Optional[str] = None) -> Optional[TieredLoader]:
    """
    v6.9.0 FIX P0-1: Get or create global TieredLoader instance.

    TieredLoader provides relevance-based context loading that achieves 5x token savings
    by loading high-relevance content fully (L1), medium as summaries (L2),
    and low as headers only (L3).

    Args:
        vault_path: Path to Obsidian vault (optional, uses default if not provided)

    Returns:
        TieredLoader instance for the session, or None if unavailable
    """
    global _tiered_loader
    if not HAS_TIERED_LOADER:
        logger.warning("TieredLoader not available - no tiered loading")
        return None

    if _tiered_loader is None:
        path = vault_path or DEFAULT_VAULT_PATH
        if Path(path).exists():
            _tiered_loader = TieredLoader(vault_path=path)
            logger.debug(f"Initialized TieredLoader with vault: {path}")
        else:
            logger.warning(f"Vault not found at {path}, TieredLoader disabled")
            return None
    return _tiered_loader


def load_tiered_context(
    items: List[Tuple[str, float]],  # (path, relevance_score)
    total_budget: Optional[int] = None,
    vault_path: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    v6.9.0 FIX P0-1: Load context at appropriate granularity based on relevance.

    This is the main entry point for tiered context loading in the execution flow.
    Achieves 5x token savings by loading:
    - L1 (relevance >= 0.7): Full content
    - L2 (relevance 0.4-0.7): Paragraph summaries
    - L3 (relevance < 0.4): Section headers only

    Args:
        items: List of (path, relevance_score) tuples
        total_budget: Maximum tokens to use (default: 50K)
        vault_path: Path to vault (optional)

    Returns:
        List of dicts with: path, content, tier, token_count, relevance_score, truncated
    """
    loader = get_tiered_loader(vault_path)
    if loader is None:
        # Fallback: return empty list (caller should handle gracefully)
        logger.warning("TieredLoader unavailable, returning empty context")
        return []

    if total_budget is None:
        total_budget = 50000  # Default 50K tokens

    try:
        contexts = loader.load_batch(items, total_budget=total_budget)
        stats = loader.get_stats(contexts)

        logger.info(
            f"ENGINE-11: Tiered loading complete - {stats['total_items']} items, "
            f"{stats['total_tokens']:,} tokens (saved {stats['savings_ratio']:.1f}x vs full load)"
        )

        # Convert LoadedContext to dicts for easier consumption
        return [
            {
                "path": ctx.path,
                "content": ctx.content,
                "tier": ctx.tier.value if ctx.tier else "L1",
                "token_count": ctx.token_count,
                "relevance_score": ctx.relevance_score,
                "truncated": ctx.truncated,
                "original_tokens": ctx.original_tokens
            }
            for ctx in contexts
        ]
    except Exception as e:
        logger.error(f"Tiered loading failed: {e}")
        return []


def check_budget_before_spawn(
    num_agents: int,
    estimated_tokens_per_agent: int = 5000
) -> Tuple[bool, int]:
    """
    Check if we have budget for spawning agents.

    This should be called BEFORE spawning verification chains or archetype panels
    to ensure we don't exceed context limits.

    Args:
        num_agents: Number of agents to spawn
        estimated_tokens_per_agent: Estimated token consumption per agent
            - Default 5000 covers: prompt (~1500) + RAG context (~2500) + response buffer (~1000)

    Returns:
        Tuple of (can_proceed: bool, recommended_agent_count: int)
        - can_proceed: True if full allocation is possible
        - recommended_agent_count: Number of agents we can actually afford
    """
    budget = get_global_budget()
    total_needed = num_agents * estimated_tokens_per_agent

    if budget.can_allocate(total_needed):
        logger.debug(f"Budget check passed: {num_agents} agents × {estimated_tokens_per_agent} = {total_needed} tokens")
        return True, num_agents

    # Calculate how many agents we CAN afford
    remaining = budget.remaining()
    affordable = max(1, remaining // estimated_tokens_per_agent)

    logger.warning(
        f"Budget constraint: requested {num_agents} agents ({total_needed} tokens), "
        f"but only {remaining} tokens remaining. Recommending {affordable} agents."
    )
    return False, affordable


def allocate_for_agents(
    num_agents: int,
    tokens_per_agent: int = 5000,
    category: str = "agent_spawn"
) -> bool:
    """
    Allocate budget for agent spawning.

    This should be called AFTER check_budget_before_spawn confirms availability,
    or when you want to force allocation and handle failure.

    Args:
        num_agents: Number of agents being spawned
        tokens_per_agent: Token allocation per agent
        category: Budget category for tracking (default: "agent_spawn")

    Returns:
        True if allocation succeeded, False if budget exceeded
    """
    budget = get_global_budget()
    total = num_agents * tokens_per_agent
    description = f"{num_agents} agents @ {tokens_per_agent} tokens each"

    success = budget.allocate(category, total, description)
    if success:
        logger.info(f"Allocated {total} tokens for {description}")
    else:
        logger.error(f"Failed to allocate {total} tokens - budget exceeded")

    return success


def allocate_for_rag(
    num_results: int,
    chars_per_result: int = 1500,
    category: str = "rag_context"
) -> bool:
    """
    Allocate budget for RAG context injection.

    Args:
        num_results: Number of RAG results to inject
        chars_per_result: Average characters per result
        category: Budget category for tracking

    Returns:
        True if allocation succeeded
    """
    budget = get_global_budget()
    # Convert chars to tokens (rough estimate: 4 chars = 1 token)
    tokens_per_result = max(1, chars_per_result // 4)
    total = num_results * tokens_per_result
    description = f"{num_results} RAG results @ ~{tokens_per_result} tokens each"

    return budget.allocate(category, total, description)


def allocate_for_prompt(
    prompt_chars: int,
    category: str = "prompt"
) -> bool:
    """
    Allocate budget for a prompt.

    Args:
        prompt_chars: Character count of the prompt
        category: Budget category for tracking

    Returns:
        True if allocation succeeded
    """
    budget = get_global_budget()
    return budget.allocate_chars(category, prompt_chars, f"Prompt ({prompt_chars} chars)")


def deduplicate_context(
    items: List[Tuple[str, str]],
    vault_path: Optional[str] = None
) -> List[Tuple[str, str, bool]]:
    """
    Deduplicate context items before sending to agents.

    Args:
        items: List of (path, content) tuples
        vault_path: Optional vault path for deduplicator

    Returns:
        List of (path, content, is_new) tuples - only includes unique items
    """
    dedup = get_deduplicator(vault_path)
    return dedup.deduplicate_batch(items)


def mark_content_sent(content: str, path: str = "") -> None:
    """
    Mark content as sent in the current session.

    Call this after sending content to prevent re-sending in same session.

    Args:
        content: The content that was sent
        path: Optional path identifier
    """
    dedup = get_deduplicator()
    dedup.mark_sent(content, path)


def is_duplicate(content: str, session_only: bool = True) -> bool:
    """
    Check if content is a duplicate.

    Args:
        content: Content to check
        session_only: If True, only check current session

    Returns:
        True if content was already sent
    """
    dedup = get_deduplicator()
    return dedup.is_duplicate(content, session_only)


def get_content_overlap(content: str) -> float:
    """
    Get overlap ratio with already-sent content.

    Args:
        content: Content to check

    Returns:
        Overlap ratio (0.0-1.0)
    """
    dedup = get_deduplicator()
    return dedup.find_overlap(content)


def reset_session_budget() -> None:
    """
    Reset budget and deduplication tracking for a new session.

    Call this at the start of a new USF task to reset:
    - Context budget allocations
    - Deduplication session hashes
    """
    budget = get_global_budget()
    budget.reset()
    logger.info("Context budget reset")

    dedup = get_deduplicator()
    dedup.clear_session()
    logger.info("Deduplication session cleared")


def get_budget_report() -> str:
    """
    Get a detailed budget usage report.

    Returns:
        Formatted string with budget breakdown
    """
    budget = get_global_budget()
    return budget.get_report()


def get_budget_stats() -> Dict[str, Any]:
    """
    Get budget statistics as a dictionary.

    Returns:
        Dict with: used_tokens, max_budget, remaining, utilization, breakdown
    """
    budget = get_global_budget()
    return {
        "used_tokens": budget.used_tokens,
        "max_budget": budget.max_budget,
        "remaining": budget.remaining(),
        "utilization": budget.utilization(),
        "breakdown": budget.get_breakdown()
    }


def get_dedup_stats() -> Dict[str, Any]:
    """
    Get deduplication statistics.

    Returns:
        Dict with session and global dedup stats
    """
    dedup = get_deduplicator()
    return {
        "session": dedup.get_session_stats(),
        "global": dedup.get_global_stats()
    }


# Convenience function for the execution flow
def enforce_budget_limit(
    num_chains: int,
    num_archetypes: int,
    rag_results_per_agent: int = 10,
    # v6.8.0 FIX P1#7: Increased by 50% to match actual measurements
    tokens_per_chain: int = 4500,  # was 3000, actual: 3500-6000
    tokens_per_archetype: int = 3750,  # was 2500, actual: 3000-5000
    tokens_per_rag: int = 563  # was 375 (~1500 chars / 4)
) -> Tuple[bool, Dict[str, int]]:
    """
    Comprehensive budget check and allocation for a USF execution plan.

    This is the main entry point for budget enforcement in usf_executor.py.

    Args:
        num_chains: Number of verification chains
        num_archetypes: Number of archetype panel members
        rag_results_per_agent: RAG results per agent
        tokens_per_chain: Token estimate per verification chain
        tokens_per_archetype: Token estimate per archetype
        tokens_per_rag: Token estimate per RAG result

    Returns:
        Tuple of (success: bool, allocation_details: dict)
    """
    budget = get_global_budget()

    # Calculate total needed
    chain_tokens = num_chains * tokens_per_chain
    archetype_tokens = num_archetypes * tokens_per_archetype
    total_agents = num_chains + num_archetypes
    rag_tokens = total_agents * rag_results_per_agent * tokens_per_rag

    total_needed = chain_tokens + archetype_tokens + rag_tokens

    details = {
        "chains": {"count": num_chains, "tokens": chain_tokens},
        "archetypes": {"count": num_archetypes, "tokens": archetype_tokens},
        "rag": {"count": total_agents * rag_results_per_agent, "tokens": rag_tokens},
        "total_requested": total_needed,
        "budget_remaining": budget.remaining(),
        "budget_max": budget.max_budget
    }

    if not budget.can_allocate(total_needed):
        # Calculate what we can afford
        remaining = budget.remaining()

        # Proportionally reduce
        if total_needed > 0:
            scale = remaining / total_needed
            details["recommended_chains"] = max(1, int(num_chains * scale))
            details["recommended_archetypes"] = max(1, int(num_archetypes * scale))
            details["scale_factor"] = scale

        logger.warning(
            f"Budget enforcement: requested {total_needed} tokens, "
            f"but only {remaining} available. Scale factor: {scale:.2f}"
        )
        return False, details

    # Allocate
    budget.allocate("verification_chains", chain_tokens, f"{num_chains} chains")
    budget.allocate("archetype_panel", archetype_tokens, f"{num_archetypes} archetypes")
    budget.allocate("rag_context", rag_tokens, f"{total_agents * rag_results_per_agent} RAG results")

    details["allocated"] = True
    details["new_remaining"] = budget.remaining()

    logger.info(
        f"Budget allocated: {total_needed} tokens "
        f"({num_chains} chains + {num_archetypes} archetypes + RAG). "
        f"Remaining: {budget.remaining()}"
    )

    return True, details


# Module-level initialization log
logger.debug("ENGINE-11 integration module loaded")
