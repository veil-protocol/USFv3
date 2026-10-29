#!/usr/bin/env python3
"""
PreCompact Hook - Auto-save session state before context compaction.

USF 7.0 Implementation - Preserves session state when Claude context is compacted.

This hook is triggered before Claude's context window is compacted/summarized,
allowing USF to save critical session state that would otherwise be lost.

Saves:
- Current task state and progress
- Accumulated findings and confidence scores
- Skill extraction candidates
- SONA router learning state
- Task claims state

Usage:
    This hook is called automatically by Claude Code when context is about to be compacted.
    Can also be invoked manually:

    python3 .claude/hooks/pre_compact.py --session-id abc123

Configuration:
    Set USF_COMPACT_SAVE_PATH to override default save location.
    Default: ~/.usf/sessions/
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

# Default save path
DEFAULT_SAVE_PATH = Path.home() / ".usf" / "sessions"


def get_session_state() -> Dict[str, Any]:
    """
    Collect current session state from various USF components.

    Returns a dictionary of all state that should be preserved.
    """
    state = {
        "timestamp": datetime.now().isoformat(),
        "usf_version": "7.0",
        "components": {}
    }

    # Try to get SONA router state
    try:
        from omega.v3.sona_router import get_router
        router = get_router()
        state["components"]["sona_router"] = {
            "q_table": dict(router.q_table),
            "stats": router.get_stats()
        }
    except Exception as e:
        state["components"]["sona_router"] = {"error": str(e)}

    # Try to get skill extractor state
    try:
        from omega.skill_extractor import get_extractor
        extractor = get_extractor()
        state["components"]["skill_extractor"] = {
            "skills_count": len(extractor.skills),
            "stats": extractor.get_stats()
        }
    except Exception as e:
        state["components"]["skill_extractor"] = {"error": str(e)}

    # Try to get task claims state
    try:
        from omega.task_claims import get_claim_manager
        manager = get_claim_manager()
        state["components"]["task_claims"] = manager.get_stats()
    except Exception as e:
        state["components"]["task_claims"] = {"error": str(e)}

    # Try to get circuit breaker state
    try:
        from omega.circuit_breaker import get_registry
        registry = get_registry()
        state["components"]["circuit_breakers"] = registry.status()
    except Exception as e:
        state["components"]["circuit_breakers"] = {"error": str(e)}

    return state


def save_session(
    session_id: str,
    save_path: Optional[Path] = None,
    extra_data: Optional[Dict] = None
) -> Path:
    """
    Save session state to disk.

    Args:
        session_id: Unique identifier for this session
        save_path: Override default save location
        extra_data: Additional data to include in save

    Returns:
        Path to saved session file
    """
    if save_path is None:
        save_path = Path(os.environ.get("USF_COMPACT_SAVE_PATH", str(DEFAULT_SAVE_PATH)))

    save_path.mkdir(parents=True, exist_ok=True)

    # Get current state
    state = get_session_state()
    state["session_id"] = session_id

    if extra_data:
        state["extra"] = extra_data

    # Save to file
    filename = f"session_{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = save_path / filename

    with open(filepath, "w") as f:
        json.dump(state, f, indent=2, default=str)

    return filepath


def load_session(
    session_id: str,
    save_path: Optional[Path] = None
) -> Optional[Dict[str, Any]]:
    """
    Load most recent session state.

    Args:
        session_id: Session identifier to load
        save_path: Override default save location

    Returns:
        Session state dictionary or None if not found
    """
    if save_path is None:
        save_path = Path(os.environ.get("USF_COMPACT_SAVE_PATH", str(DEFAULT_SAVE_PATH)))

    if not save_path.exists():
        return None

    # Find most recent session file
    pattern = f"session_{session_id}_*.json"
    files = sorted(save_path.glob(pattern), reverse=True)

    if not files:
        return None

    with open(files[0], "r") as f:
        return json.load(f)


def restore_session(session_data: Dict[str, Any]) -> Dict[str, bool]:
    """
    Restore session state to USF components.

    Args:
        session_data: Previously saved session state

    Returns:
        Dictionary of component names and whether restoration succeeded
    """
    results = {}

    components = session_data.get("components", {})

    # Restore SONA router
    if "sona_router" in components and "q_table" in components["sona_router"]:
        try:
            from omega.v3.sona_router import get_router
            router = get_router()
            # Restore Q-table
            for task_type, agents in components["sona_router"]["q_table"].items():
                for agent_id, q_value in agents.items():
                    router.q_table[task_type][agent_id] = q_value
            results["sona_router"] = True
        except Exception as e:
            results["sona_router"] = False

    # Other components auto-restore from their persistence files

    return results


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="USF 7.0 PreCompact Hook - Save session state before compaction"
    )
    parser.add_argument(
        "--session-id",
        default="default",
        help="Session identifier (default: 'default')"
    )
    parser.add_argument(
        "--save-path",
        type=Path,
        help=f"Override save location (default: {DEFAULT_SAVE_PATH})"
    )
    parser.add_argument(
        "--restore",
        action="store_true",
        help="Restore session instead of saving"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available session saves"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress output (for hook integration)"
    )

    args = parser.parse_args()

    save_path = args.save_path or Path(
        os.environ.get("USF_COMPACT_SAVE_PATH", str(DEFAULT_SAVE_PATH))
    )

    if args.list:
        if save_path.exists():
            files = sorted(save_path.glob("session_*.json"), reverse=True)
            if files:
                print(f"Available sessions in {save_path}:")
                for f in files[:10]:
                    print(f"  {f.name}")
            else:
                print("No saved sessions found.")
        else:
            print(f"Save path does not exist: {save_path}")
        return

    if args.restore:
        session_data = load_session(args.session_id, save_path)
        if session_data:
            results = restore_session(session_data)
            if not args.quiet:
                print(f"Restored session {args.session_id}:")
                for component, success in results.items():
                    status = "OK" if success else "FAILED"
                    print(f"  {component}: {status}")
        else:
            if not args.quiet:
                print(f"No session found: {args.session_id}")
            sys.exit(1)
    else:
        # Save session
        filepath = save_session(args.session_id, save_path)
        if not args.quiet:
            print(f"Session saved to: {filepath}")


if __name__ == "__main__":
    main()
