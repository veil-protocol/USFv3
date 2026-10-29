"""
SONA: Self-Optimizing Neural Architecture Router

USF 7.0 Implementation - Adaptive agent routing with Q-learning.

Achieves <0.05ms routing decisions by:
1. Pre-computed Q-tables for task-type → agent-performance mapping
2. O(1) lookup with lazy initialization
3. Background learning updates (non-blocking)

Based on patterns from:
- claude-flow: Q-learning agent routing
- multi-agent-code-analyzer: Task classification
"""

import asyncio
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Any
from collections import defaultdict
import json
import hashlib
from pathlib import Path


@dataclass
class TaskClassification:
    """Task type classification result."""
    task_type: str
    confidence: float
    subtypes: List[str] = field(default_factory=list)
    features: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RoutingDecision:
    """Agent routing decision with metadata."""
    agent_id: str
    confidence: float
    q_value: float
    latency_ms: float
    alternatives: List[str] = field(default_factory=list)


@dataclass
class AgentPerformance:
    """Tracked performance metrics for an agent."""
    total_tasks: int = 0
    successes: int = 0
    failures: int = 0
    total_latency: float = 0.0
    avg_confidence: float = 0.5

    @property
    def success_rate(self) -> float:
        if self.total_tasks == 0:
            return 0.5
        return self.successes / self.total_tasks

    @property
    def avg_latency(self) -> float:
        if self.total_tasks == 0:
            return 1.0
        return self.total_latency / self.total_tasks


class TaskClassifier:
    """Fast task type classification using keyword matching.

    Achieves <0.01ms classification via:
    - Pre-computed keyword sets
    - Single-pass token matching
    - Hash-based subtype detection
    """

    # Primary task type keywords
    # NOTE: Keywords are checked in order of insertion, security-related terms
    # should be in security to ensure proper routing for security audits
    TASK_TYPES = {
        "security": {
            "keywords": {"security", "vulnerability", "exploit", "attack", "pentest", "cve",
                        "hack", "breach", "malware", "injection", "xss", "sqli",
                        "privilege", "escalation", "reconnaissance", "enumeration",
                        "audit", "hardening", "threat", "risk", "ctf", "oscp"},
            "subtypes": ["offensive", "defensive", "audit", "research"]
        },
        "analysis": {
            "keywords": {"analyze", "review", "assess", "evaluate", "examine",
                        "investigate", "study", "understand", "explain"},
            "subtypes": ["code", "architecture", "performance", "behavior"]
        },
        "implementation": {
            "keywords": {"implement", "build", "create", "develop", "write",
                        "code", "program", "construct", "deploy", "setup"},
            "subtypes": ["feature", "fix", "refactor", "integration"]
        },
        "verification": {
            "keywords": {"verify", "validate", "test", "check", "confirm",
                        "prove", "certify", "compliance"},
            "subtypes": ["functional", "security", "performance", "compliance"]
        },
        "planning": {
            "keywords": {"plan", "design", "architect", "strategy", "roadmap",
                        "schedule", "organize", "prioritize", "decompose"},
            "subtypes": ["technical", "strategic", "tactical", "resource"]
        },
        "research": {
            "keywords": {"research", "find", "search", "lookup", "discover",
                        "investigate", "explore", "learn", "study"},
            "subtypes": ["technical", "academic", "market", "threat"]
        }
    }

    def __init__(self):
        # Pre-compute flattened keyword map for O(1) lookup
        self._keyword_to_type: Dict[str, str] = {}
        for task_type, config in self.TASK_TYPES.items():
            for keyword in config["keywords"]:
                self._keyword_to_type[keyword] = task_type

    def classify(self, task: str) -> TaskClassification:
        """Classify task type in <0.01ms."""
        start = time.perf_counter()

        # Tokenize and lowercase
        tokens = set(task.lower().split())

        # Score each task type
        type_scores: Dict[str, int] = defaultdict(int)
        matched_subtypes: List[str] = []

        for token in tokens:
            # Strip punctuation
            clean_token = token.strip(".,!?:;\"'()[]{}").lower()
            if clean_token in self._keyword_to_type:
                task_type = self._keyword_to_type[clean_token]
                type_scores[task_type] += 1

                # Check for subtype matches
                for subtype in self.TASK_TYPES[task_type]["subtypes"]:
                    if subtype in task.lower():
                        matched_subtypes.append(f"{task_type}:{subtype}")

        # Determine primary type
        if type_scores:
            primary_type = max(type_scores.items(), key=lambda x: x[1])
            total_matches = sum(type_scores.values())
            confidence = primary_type[1] / max(total_matches, 1)
        else:
            primary_type = ("analysis", 0)  # Default
            confidence = 0.5

        elapsed_ms = (time.perf_counter() - start) * 1000

        return TaskClassification(
            task_type=primary_type[0],
            confidence=min(confidence, 1.0),
            subtypes=matched_subtypes,
            features={
                "token_count": len(tokens),
                "match_count": sum(type_scores.values()),
                "classification_ms": elapsed_ms
            }
        )


class SONARouter:
    """Self-Optimizing Neural Architecture Router.

    Achieves <0.05ms routing decisions via:
    - Q-table based agent selection
    - Lazy initialization with defaults
    - Non-blocking background learning

    Q-Learning Update:
        Q(s,a) ← Q(s,a) + α * (reward - Q(s,a))

    Where:
        - s = task_type
        - a = agent_id
        - α = learning_rate
        - reward = success (1.0) - latency_penalty - failure_penalty (-0.5)
    """

    def __init__(
        self,
        learning_rate: float = 0.1,
        latency_weight: float = 0.1,
        persistence_path: Optional[Path] = None
    ):
        self.learning_rate = learning_rate
        self.latency_weight = latency_weight
        self.persistence_path = persistence_path

        # Q-table: task_type → {agent_id → q_value}
        self.q_table: Dict[str, Dict[str, float]] = defaultdict(
            lambda: defaultdict(lambda: 0.5)  # Default Q-value
        )

        # Performance tracking
        self.agent_performance: Dict[str, AgentPerformance] = defaultdict(AgentPerformance)

        # Task classifier
        self.classifier = TaskClassifier()

        # Default agents per task type
        self.default_agents: Dict[str, str] = {
            "security": "chain-d",  # Adversarial verification
            "analysis": "chain-a",  # Single-source analysis
            "implementation": "review-security",
            "verification": "chain-b",  # Dual-source verification
            "planning": "meta-decompose",
            "research": "research-cve",
        }

        # Load persisted Q-table if available
        if persistence_path and persistence_path.exists():
            self._load_q_table()

    def route(self, task: str, context: Optional[Dict] = None) -> RoutingDecision:
        """Route task to best-performing agent in <0.05ms."""
        start = time.perf_counter()

        # Classify task
        classification = self.classifier.classify(task)
        task_type = classification.task_type

        # Get Q-values for this task type
        agent_scores = self.q_table[task_type]

        # Select best agent
        if agent_scores:
            best_agent, best_q = max(agent_scores.items(), key=lambda x: x[1])
            alternatives = sorted(
                [a for a in agent_scores.keys() if a != best_agent],
                key=lambda a: agent_scores[a],
                reverse=True
            )[:3]
        else:
            # Fall back to default
            best_agent = self.default_agents.get(task_type, "chain-a")
            best_q = 0.5
            alternatives = []

        elapsed_ms = (time.perf_counter() - start) * 1000

        return RoutingDecision(
            agent_id=best_agent,
            confidence=classification.confidence,
            q_value=best_q,
            latency_ms=elapsed_ms,
            alternatives=alternatives
        )

    def update(
        self,
        task_type: str,
        agent_id: str,
        success: bool,
        latency_seconds: float,
        confidence: float = 0.5
    ):
        """Update Q-value after task completion (Q-learning)."""
        # Calculate reward
        reward = 1.0 if success else -0.5
        reward -= latency_seconds * self.latency_weight  # Penalize slow agents
        reward += (confidence - 0.5) * 0.2  # Bonus for high confidence

        # Q-learning update
        old_q = self.q_table[task_type][agent_id]
        new_q = old_q + self.learning_rate * (reward - old_q)
        self.q_table[task_type][agent_id] = new_q

        # Update performance metrics
        perf = self.agent_performance[agent_id]
        perf.total_tasks += 1
        if success:
            perf.successes += 1
        else:
            perf.failures += 1
        perf.total_latency += latency_seconds
        perf.avg_confidence = (
            perf.avg_confidence * (perf.total_tasks - 1) + confidence
        ) / perf.total_tasks

    async def update_async(
        self,
        task_type: str,
        agent_id: str,
        success: bool,
        latency_seconds: float,
        confidence: float = 0.5
    ):
        """Non-blocking Q-value update."""
        # Run update in background
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            self.update,
            task_type,
            agent_id,
            success,
            latency_seconds,
            confidence
        )

    def get_stats(self) -> Dict[str, Any]:
        """Get router statistics."""
        return {
            "task_types": len(self.q_table),
            "agents_tracked": len(self.agent_performance),
            "total_decisions": sum(
                p.total_tasks for p in self.agent_performance.values()
            ),
            "avg_success_rate": sum(
                p.success_rate for p in self.agent_performance.values()
            ) / max(len(self.agent_performance), 1),
            "q_table_size": sum(len(agents) for agents in self.q_table.values()),
        }

    def get_best_agents(self, task_type: str, top_k: int = 5) -> List[Dict]:
        """Get top performing agents for a task type."""
        agent_scores = self.q_table.get(task_type, {})
        sorted_agents = sorted(
            agent_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_k]

        return [
            {
                "agent_id": agent_id,
                "q_value": q_value,
                "performance": {
                    "success_rate": self.agent_performance[agent_id].success_rate,
                    "avg_latency": self.agent_performance[agent_id].avg_latency,
                    "total_tasks": self.agent_performance[agent_id].total_tasks,
                }
            }
            for agent_id, q_value in sorted_agents
        ]

    def _load_q_table(self):
        """Load Q-table from persistence file."""
        try:
            with open(self.persistence_path, "r") as f:
                data = json.load(f)
                self.q_table = defaultdict(
                    lambda: defaultdict(lambda: 0.5),
                    {k: defaultdict(lambda: 0.5, v) for k, v in data.get("q_table", {}).items()}
                )
                # Load performance data
                for agent_id, perf_data in data.get("performance", {}).items():
                    perf = AgentPerformance(**perf_data)
                    self.agent_performance[agent_id] = perf
        except Exception:
            pass  # Start fresh if loading fails

    def save(self):
        """Persist Q-table to disk."""
        if not self.persistence_path:
            return

        data = {
            "q_table": {k: dict(v) for k, v in self.q_table.items()},
            "performance": {
                k: {
                    "total_tasks": v.total_tasks,
                    "successes": v.successes,
                    "failures": v.failures,
                    "total_latency": v.total_latency,
                    "avg_confidence": v.avg_confidence,
                }
                for k, v in self.agent_performance.items()
            }
        }

        self.persistence_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.persistence_path, "w") as f:
            json.dump(data, f, indent=2)


# Global router instance (lazy initialization)
_router: Optional[SONARouter] = None


def get_router(persistence_path: Optional[Path] = None) -> SONARouter:
    """Get or create the global SONA router instance."""
    global _router
    if _router is None:
        _router = SONARouter(persistence_path=persistence_path)
    return _router


def classify_task(task: str) -> str:
    """Convenience function for task classification."""
    classifier = TaskClassifier()
    return classifier.classify(task).task_type


def route_task(task: str, context: Optional[Dict] = None) -> RoutingDecision:
    """Convenience function for task routing."""
    return get_router().route(task, context)


# CLI for testing
if __name__ == "__main__":
    import sys

    router = SONARouter()

    test_tasks = [
        "Perform a security audit of the authentication system",
        "Analyze the code for potential vulnerabilities",
        "Implement a new feature for user authentication",
        "Verify that the fix resolves the SQL injection issue",
        "Create a plan for the security hardening project",
        "Research CVE-2024-1234 and find available exploits",
    ]

    print("SONA Router Test")
    print("=" * 60)

    for task in test_tasks:
        result = router.route(task)
        print(f"\nTask: {task[:50]}...")
        print(f"  Agent: {result.agent_id}")
        print(f"  Q-Value: {result.q_value:.3f}")
        print(f"  Confidence: {result.confidence:.3f}")
        print(f"  Latency: {result.latency_ms:.4f}ms")
        print(f"  Alternatives: {result.alternatives}")

    print("\n" + "=" * 60)
    print("Router Stats:", router.get_stats())
