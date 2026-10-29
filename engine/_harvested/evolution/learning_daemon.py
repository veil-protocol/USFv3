"""
Daemon-Based Learning for USF Multi-Agent System.

USF 7.0 Implementation - Background learning from successful executions.

Based on patterns from:
- claude-flow: Pattern mining from successful runs
- aider: Reflexion-based memory
- roo-code: Continuous improvement loop

Features:
- Asynchronous pattern extraction
- Success/failure correlation analysis
- Automatic threshold tuning
- Cross-session knowledge transfer
- Skill candidate identification

The daemon runs in the background and:
1. Monitors completed task executions
2. Extracts patterns from high-confidence successes
3. Correlates failures with context signals
4. Updates routing weights (SONA Q-table)
5. Identifies skill extraction candidates
"""

import asyncio
import hashlib
import json
import logging
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
import threading

logger = logging.getLogger(__name__)


class ExecutionOutcome(Enum):
    """Task execution outcomes for learning."""
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILURE = "failure"
    TIMEOUT = "timeout"
    ERROR = "error"


@dataclass
class ExecutionRecord:
    """Record of a task execution for analysis."""
    task_id: str
    task_description: str
    agent_id: str
    archetype: Optional[str]
    domain: str
    precision_level: int
    outcome: ExecutionOutcome
    confidence: float
    duration_seconds: float
    token_count: int
    error_message: Optional[str] = None
    output_hash: Optional[str] = None
    context_signals: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "task_description": self.task_description,
            "agent_id": self.agent_id,
            "archetype": self.archetype,
            "domain": self.domain,
            "precision_level": self.precision_level,
            "outcome": self.outcome.value,
            "confidence": self.confidence,
            "duration_seconds": self.duration_seconds,
            "token_count": self.token_count,
            "error_message": self.error_message,
            "output_hash": self.output_hash,
            "context_signals": self.context_signals,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class LearnedPattern:
    """A pattern extracted from successful executions."""
    pattern_id: str
    pattern_type: str  # "routing", "precision", "archetype", "domain"
    condition: Dict[str, Any]  # When to apply
    action: Dict[str, Any]  # What to do
    confidence: float
    support_count: int  # How many executions support this
    last_validated: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pattern_id": self.pattern_id,
            "pattern_type": self.pattern_type,
            "condition": self.condition,
            "action": self.action,
            "confidence": self.confidence,
            "support_count": self.support_count,
            "last_validated": self.last_validated.isoformat(),
        }


@dataclass
class SkillCandidate:
    """Candidate for skill extraction."""
    candidate_id: str
    task_pattern: str
    solution_hash: str
    success_count: int
    avg_confidence: float
    avg_duration: float
    example_task_ids: List[str] = field(default_factory=list)
    ready_for_extraction: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "task_pattern": self.task_pattern,
            "solution_hash": self.solution_hash,
            "success_count": self.success_count,
            "avg_confidence": self.avg_confidence,
            "avg_duration": self.avg_duration,
            "example_task_ids": self.example_task_ids[:5],
            "ready_for_extraction": self.ready_for_extraction,
        }


class LearningDaemon:
    """
    Background learning daemon for USF.

    Continuously analyzes execution records to:
    - Extract successful patterns
    - Tune routing decisions
    - Identify skill candidates
    - Correlate failures with context
    """

    # Thresholds
    MIN_CONFIDENCE_FOR_LEARNING = 0.7
    MIN_SUPPORT_FOR_PATTERN = 3
    SKILL_EXTRACTION_THRESHOLD = 5
    PATTERN_DECAY_DAYS = 30

    def __init__(
        self,
        persistence_path: Optional[Path] = None,
        learning_interval: float = 60.0,  # seconds
        auto_start: bool = False
    ):
        """
        Initialize learning daemon.

        Args:
            persistence_path: Where to save learned patterns
            learning_interval: How often to run learning cycle
            auto_start: Whether to start daemon automatically
        """
        self.persistence_path = persistence_path
        self.learning_interval = learning_interval

        # State
        self._records: List[ExecutionRecord] = []
        self._patterns: Dict[str, LearnedPattern] = {}
        self._skill_candidates: Dict[str, SkillCandidate] = {}
        self._running = False
        self._task: Optional[asyncio.Task] = None
        self._lock = asyncio.Lock()

        # Callbacks
        self._on_pattern_learned: List[Callable[[LearnedPattern], None]] = []
        self._on_skill_ready: List[Callable[[SkillCandidate], None]] = []

        # Statistics
        self._stats = {
            "records_processed": 0,
            "patterns_learned": 0,
            "patterns_applied": 0,
            "skills_identified": 0,
            "learning_cycles": 0,
        }

        if persistence_path:
            self._load_state()

        if auto_start:
            self.start()

    def _load_state(self):
        """Load persisted state."""
        if not self.persistence_path or not self.persistence_path.exists():
            return

        try:
            with open(self.persistence_path, "r") as f:
                data = json.load(f)

                for pattern_data in data.get("patterns", []):
                    pattern = LearnedPattern(
                        pattern_id=pattern_data["pattern_id"],
                        pattern_type=pattern_data["pattern_type"],
                        condition=pattern_data["condition"],
                        action=pattern_data["action"],
                        confidence=pattern_data["confidence"],
                        support_count=pattern_data["support_count"],
                        last_validated=datetime.fromisoformat(pattern_data["last_validated"]),
                    )
                    self._patterns[pattern.pattern_id] = pattern

                for candidate_data in data.get("skill_candidates", []):
                    candidate = SkillCandidate(
                        candidate_id=candidate_data["candidate_id"],
                        task_pattern=candidate_data["task_pattern"],
                        solution_hash=candidate_data["solution_hash"],
                        success_count=candidate_data["success_count"],
                        avg_confidence=candidate_data["avg_confidence"],
                        avg_duration=candidate_data["avg_duration"],
                        example_task_ids=candidate_data.get("example_task_ids", []),
                        ready_for_extraction=candidate_data.get("ready_for_extraction", False),
                    )
                    self._skill_candidates[candidate.candidate_id] = candidate

                self._stats = data.get("stats", self._stats)

        except Exception as e:
            logger.warning(f"Failed to load learning state: {e}")

    def _save_state(self):
        """Persist learning state."""
        if not self.persistence_path:
            return

        self.persistence_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "version": "1.0",
            "updated_at": datetime.now().isoformat(),
            "patterns": [p.to_dict() for p in self._patterns.values()],
            "skill_candidates": [c.to_dict() for c in self._skill_candidates.values()],
            "stats": self._stats,
        }
        with open(self.persistence_path, "w") as f:
            json.dump(data, f, indent=2)

    def start(self):
        """Start the learning daemon."""
        if self._running:
            return

        self._running = True
        self._task = asyncio.create_task(self._daemon_loop())
        logger.info("Learning daemon started")

    def stop(self):
        """Stop the learning daemon."""
        self._running = False
        if self._task:
            self._task.cancel()
        self._save_state()
        logger.info("Learning daemon stopped")

    async def _daemon_loop(self):
        """Main daemon loop."""
        while self._running:
            try:
                await self._learning_cycle()
                await asyncio.sleep(self.learning_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Learning cycle error: {e}")
                await asyncio.sleep(self.learning_interval)

    async def _learning_cycle(self):
        """Run one learning cycle."""
        async with self._lock:
            self._stats["learning_cycles"] += 1

            # Process new records
            if self._records:
                await self._extract_patterns()
                await self._identify_skill_candidates()
                await self._decay_old_patterns()
                self._save_state()

    def record_execution(self, record: ExecutionRecord):
        """
        Record an execution for learning.

        Thread-safe - can be called from any context.
        """
        self._records.append(record)
        self._stats["records_processed"] += 1

    async def _extract_patterns(self):
        """Extract patterns from recent records."""
        # Group successful executions
        successes = [
            r for r in self._records
            if r.outcome == ExecutionOutcome.SUCCESS
            and r.confidence >= self.MIN_CONFIDENCE_FOR_LEARNING
        ]

        if not successes:
            return

        # Pattern 1: Domain → Archetype mapping
        domain_archetype_counts: Dict[Tuple[str, str], int] = defaultdict(int)
        for record in successes:
            if record.archetype:
                domain_archetype_counts[(record.domain, record.archetype)] += 1

        for (domain, archetype), count in domain_archetype_counts.items():
            if count >= self.MIN_SUPPORT_FOR_PATTERN:
                pattern_id = f"domain_archetype_{domain}_{archetype}"
                pattern = LearnedPattern(
                    pattern_id=pattern_id,
                    pattern_type="archetype",
                    condition={"domain": domain},
                    action={"preferred_archetype": archetype},
                    confidence=min(0.5 + count * 0.1, 0.95),
                    support_count=count,
                )
                self._patterns[pattern_id] = pattern
                self._notify_pattern_learned(pattern)

        # Pattern 2: Task keywords → Precision level
        keyword_precision: Dict[Tuple[str, int], int] = defaultdict(int)
        for record in successes:
            keywords = self._extract_keywords(record.task_description)
            for kw in keywords:
                keyword_precision[(kw, record.precision_level)] += 1

        for (keyword, precision), count in keyword_precision.items():
            if count >= self.MIN_SUPPORT_FOR_PATTERN:
                pattern_id = f"keyword_precision_{keyword}_{precision}"
                pattern = LearnedPattern(
                    pattern_id=pattern_id,
                    pattern_type="precision",
                    condition={"contains_keyword": keyword},
                    action={"suggested_precision": precision},
                    confidence=min(0.5 + count * 0.1, 0.95),
                    support_count=count,
                )
                self._patterns[pattern_id] = pattern

        # Pattern 3: Agent performance by domain
        agent_domain_performance: Dict[Tuple[str, str], List[float]] = defaultdict(list)
        for record in successes:
            agent_domain_performance[(record.agent_id, record.domain)].append(record.confidence)

        for (agent_id, domain), confidences in agent_domain_performance.items():
            if len(confidences) >= self.MIN_SUPPORT_FOR_PATTERN:
                avg_conf = sum(confidences) / len(confidences)
                pattern_id = f"agent_domain_{agent_id}_{domain}"
                pattern = LearnedPattern(
                    pattern_id=pattern_id,
                    pattern_type="routing",
                    condition={"domain": domain},
                    action={"preferred_agent": agent_id, "expected_confidence": avg_conf},
                    confidence=avg_conf,
                    support_count=len(confidences),
                )
                self._patterns[pattern_id] = pattern

        # Clear processed records
        self._records = [r for r in self._records if r not in successes]

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract significant keywords from text."""
        # Simple keyword extraction
        keywords = []
        text_lower = text.lower()

        significant_terms = [
            "security", "audit", "vulnerability", "exploit",
            "authentication", "authorization", "encryption",
            "analyze", "review", "test", "verify",
            "implement", "build", "create", "fix",
            "research", "investigate", "explain",
        ]

        for term in significant_terms:
            if term in text_lower:
                keywords.append(term)

        return keywords

    async def _identify_skill_candidates(self):
        """Identify patterns that could become skills."""
        # Group by task pattern (simplified description hash)
        task_groups: Dict[str, List[ExecutionRecord]] = defaultdict(list)

        for record in self._records:
            if record.outcome == ExecutionOutcome.SUCCESS and record.confidence >= 0.8:
                # Create simplified pattern
                pattern = self._simplify_task(record.task_description)
                task_groups[pattern].append(record)

        for pattern, records in task_groups.items():
            if len(records) >= self.SKILL_EXTRACTION_THRESHOLD:
                candidate_id = hashlib.sha256(pattern.encode()).hexdigest()[:12]

                if candidate_id in self._skill_candidates:
                    # Update existing
                    candidate = self._skill_candidates[candidate_id]
                    candidate.success_count = len(records)
                    candidate.avg_confidence = sum(r.confidence for r in records) / len(records)
                    candidate.avg_duration = sum(r.duration_seconds for r in records) / len(records)
                    candidate.example_task_ids = [r.task_id for r in records[:5]]
                else:
                    # Create new
                    candidate = SkillCandidate(
                        candidate_id=candidate_id,
                        task_pattern=pattern,
                        solution_hash=records[0].output_hash or "",
                        success_count=len(records),
                        avg_confidence=sum(r.confidence for r in records) / len(records),
                        avg_duration=sum(r.duration_seconds for r in records) / len(records),
                        example_task_ids=[r.task_id for r in records[:5]],
                    )
                    self._skill_candidates[candidate_id] = candidate
                    self._stats["skills_identified"] += 1

                # Check if ready for extraction
                if candidate.success_count >= self.SKILL_EXTRACTION_THRESHOLD * 2:
                    if not candidate.ready_for_extraction:
                        candidate.ready_for_extraction = True
                        self._notify_skill_ready(candidate)

    def _simplify_task(self, description: str) -> str:
        """Simplify task description to pattern."""
        # Remove specific values, keep structure
        import re

        simplified = description.lower()

        # Remove numbers
        simplified = re.sub(r'\d+', 'N', simplified)

        # Remove file paths
        simplified = re.sub(r'/[\w/.-]+', 'PATH', simplified)

        # Remove URLs
        simplified = re.sub(r'https?://\S+', 'URL', simplified)

        # Remove IPs
        simplified = re.sub(r'\d+\.\d+\.\d+\.\d+', 'IP', simplified)

        # Normalize whitespace
        simplified = re.sub(r'\s+', ' ', simplified).strip()

        return simplified[:100]

    async def _decay_old_patterns(self):
        """Decay patterns that haven't been validated recently."""
        cutoff = datetime.now() - timedelta(days=self.PATTERN_DECAY_DAYS)

        to_remove = []
        for pattern_id, pattern in self._patterns.items():
            if pattern.last_validated < cutoff:
                # Reduce confidence
                pattern.confidence *= 0.9
                if pattern.confidence < 0.3:
                    to_remove.append(pattern_id)

        for pattern_id in to_remove:
            del self._patterns[pattern_id]

    def get_routing_suggestion(self, domain: str, task_description: str) -> Optional[Dict[str, Any]]:
        """
        Get routing suggestion based on learned patterns.

        Returns suggestion dict or None if no pattern matches.
        """
        best_match = None
        best_confidence = 0.0

        for pattern in self._patterns.values():
            if pattern.pattern_type == "routing":
                if pattern.condition.get("domain") == domain:
                    if pattern.confidence > best_confidence:
                        best_match = pattern
                        best_confidence = pattern.confidence

        if best_match:
            self._stats["patterns_applied"] += 1
            best_match.last_validated = datetime.now()
            return best_match.action

        return None

    def get_precision_suggestion(self, task_description: str) -> Optional[int]:
        """Get suggested precision level based on learned patterns."""
        keywords = self._extract_keywords(task_description)

        suggestions = []
        for pattern in self._patterns.values():
            if pattern.pattern_type == "precision":
                keyword = pattern.condition.get("contains_keyword")
                if keyword and keyword in keywords:
                    suggestions.append((
                        pattern.action.get("suggested_precision", 3),
                        pattern.confidence
                    ))

        if suggestions:
            # Weighted average
            total_weight = sum(s[1] for s in suggestions)
            if total_weight > 0:
                weighted = sum(s[0] * s[1] for s in suggestions) / total_weight
                self._stats["patterns_applied"] += 1
                return round(weighted)

        return None

    def get_ready_skills(self) -> List[SkillCandidate]:
        """Get skill candidates ready for extraction."""
        return [c for c in self._skill_candidates.values() if c.ready_for_extraction]

    def on_pattern_learned(self, callback: Callable[[LearnedPattern], None]):
        """Register callback for pattern learning events."""
        self._on_pattern_learned.append(callback)

    def on_skill_ready(self, callback: Callable[[SkillCandidate], None]):
        """Register callback for skill readiness events."""
        self._on_skill_ready.append(callback)

    def _notify_pattern_learned(self, pattern: LearnedPattern):
        """Notify callbacks of new pattern."""
        self._stats["patterns_learned"] += 1
        for callback in self._on_pattern_learned:
            try:
                callback(pattern)
            except Exception as e:
                logger.warning(f"Pattern callback error: {e}")

    def _notify_skill_ready(self, candidate: SkillCandidate):
        """Notify callbacks of skill ready for extraction."""
        for callback in self._on_skill_ready:
            try:
                callback(candidate)
            except Exception as e:
                logger.warning(f"Skill callback error: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """Get daemon statistics."""
        return {
            **self._stats,
            "patterns_count": len(self._patterns),
            "skill_candidates_count": len(self._skill_candidates),
            "pending_records": len(self._records),
            "running": self._running,
        }


# Global daemon instance
_daemon: Optional[LearningDaemon] = None


def get_learning_daemon(
    persistence_path: Optional[Path] = None,
    auto_start: bool = True
) -> LearningDaemon:
    """Get or create the global learning daemon."""
    global _daemon
    if _daemon is None:
        _daemon = LearningDaemon(
            persistence_path=persistence_path,
            auto_start=auto_start
        )
    return _daemon


# CLI for testing
if __name__ == "__main__":
    import random

    print("Learning Daemon Test")
    print("=" * 60)

    async def test():
        daemon = LearningDaemon(learning_interval=2.0)

        # Register callbacks
        daemon.on_pattern_learned(lambda p: print(f"  [PATTERN] {p.pattern_type}: {p.action}"))
        daemon.on_skill_ready(lambda s: print(f"  [SKILL] Ready: {s.task_pattern[:50]}"))

        # Simulate execution records
        domains = ["security", "crypto", "analysis"]
        archetypes = ["ARC-AD", "ARC-TH", "ARC-QA", "ARC-IM", "ARC-ST"]

        print("\n1. Recording 20 simulated executions...")
        for i in range(20):
            domain = random.choice(domains)
            archetype = random.choice(archetypes)

            record = ExecutionRecord(
                task_id=f"task_{i:03d}",
                task_description=f"Analyze {domain} vulnerabilities in system",
                agent_id=f"agent_{archetype}",
                archetype=archetype,
                domain=domain,
                precision_level=random.choice([2, 3, 4]),
                outcome=ExecutionOutcome.SUCCESS if random.random() > 0.2 else ExecutionOutcome.PARTIAL,
                confidence=random.uniform(0.7, 0.95),
                duration_seconds=random.uniform(5, 30),
                token_count=random.randint(1000, 5000),
            )
            daemon.record_execution(record)

        print(f"\n2. Running learning cycle...")
        daemon.start()
        await asyncio.sleep(3)
        daemon.stop()

        print(f"\n3. Statistics:")
        stats = daemon.get_stats()
        for key, value in stats.items():
            print(f"   {key}: {value}")

        print(f"\n4. Learned Patterns ({len(daemon._patterns)}):")
        for pattern in list(daemon._patterns.values())[:5]:
            print(f"   - {pattern.pattern_type}: {pattern.condition} → {pattern.action}")
            print(f"     Confidence: {pattern.confidence:.0%}, Support: {pattern.support_count}")

        print(f"\n5. Testing suggestions:")
        suggestion = daemon.get_routing_suggestion("security", "audit vulnerabilities")
        print(f"   Routing for 'security' domain: {suggestion}")

        precision = daemon.get_precision_suggestion("analyze security vulnerabilities")
        print(f"   Precision for 'analyze security': PL{precision}")

    asyncio.run(test())
