"""
USF 6.0 ENGINE 11: Token Efficiency Components

This module provides token efficiency enforcement for USF execution:
- ContextBudget: Track cumulative context usage, prevent exhaustion
- Deduplicator: Avoid sending duplicate content
- TieredLoader: Load context on-demand by tier
- TokenCounter: Count tokens in text
- Integration API: Simple wrappers for executor integration

Quick Start:
    from efficiency import check_budget_before_spawn, allocate_for_agents, reset_session_budget

    # Before spawning agents
    can_proceed, recommended = check_budget_before_spawn(num_agents=5)

    # Allocate budget
    allocate_for_agents(num_agents=5)

    # New session
    reset_session_budget()
"""
from .tiered_loader import TieredLoader, ContextTier, LoadedContext
from .deduplication import Deduplicator, ContentFingerprint
from .token_counter import TokenCounter
from .context_budget import ContextBudget, ContextBudgetError, get_global_budget, reset_global_budget

# Integration API (simple wrappers for executor)
from .integration import (
    check_budget_before_spawn,
    allocate_for_agents,
    allocate_for_rag,
    allocate_for_prompt,
    reset_session_budget,
    get_deduplicator,
    deduplicate_context,
    mark_content_sent,
    is_duplicate,
    get_content_overlap,
    get_budget_report,
    get_budget_stats,
    get_dedup_stats,
    enforce_budget_limit,
)

__all__ = [
    # Tiered loading
    'TieredLoader', 'ContextTier', 'LoadedContext',
    # Deduplication
    'Deduplicator', 'ContentFingerprint',
    # Token counting
    'TokenCounter',
    # Context budget (ENGINE-11 core)
    'ContextBudget', 'ContextBudgetError', 'get_global_budget', 'reset_global_budget',
    # Integration API (recommended for executor)
    'check_budget_before_spawn',
    'allocate_for_agents',
    'allocate_for_rag',
    'allocate_for_prompt',
    'reset_session_budget',
    'get_deduplicator',
    'deduplicate_context',
    'mark_content_sent',
    'is_duplicate',
    'get_content_overlap',
    'get_budget_report',
    'get_budget_stats',
    'get_dedup_stats',
    'enforce_budget_limit',
]
