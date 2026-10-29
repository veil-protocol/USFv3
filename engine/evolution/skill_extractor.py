"""
Skill Extractor - Auto-extract reusable patterns from successful sessions.

USF 7.0 Implementation - Captures successful task-solution pairs as skills.

Based on patterns from:
- Claudeception: Multi-agent skill extraction
- claude-flow: Solution caching and replay

Quality gates prevent trivial or unreliable solutions from being extracted.
"""

import asyncio
import hashlib
import json
import re
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set


@dataclass
class Session:
    """Represents a completed task session."""
    id: str
    task: str
    solution: str
    verification_passed: bool
    confidence: float
    latency_seconds: float
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_documentation_lookup(self) -> bool:
        """Check if this was just a documentation lookup (not novel)."""
        doc_patterns = [
            r'according to (the )?documentation',
            r'the manual (says|states)',
            r'per (the )?docs',
            r'from (the )?readme',
            r'as documented',
        ]
        solution_lower = self.solution.lower()
        return any(re.search(p, solution_lower) for p in doc_patterns)

    @property
    def reusability_score(self) -> float:
        """Estimate how reusable this solution is (0.0-1.0)."""
        score = 0.0

        # Length factor: Not too short, not too long
        length = len(self.solution)
        if 100 < length < 5000:
            score += 0.3
        elif 50 < length <= 100:
            score += 0.1

        # Contains code blocks (likely actionable)
        if '```' in self.solution:
            score += 0.2

        # Contains structured output markers
        if any(m in self.solution for m in ['[FINDING]', '[DATA]', '[STAT:']):
            score += 0.1

        # Contains step-by-step instructions
        if re.search(r'(step \d|1\.\s|first,|then,|finally,)', self.solution.lower()):
            score += 0.2

        # Has verification evidence
        if self.verification_passed:
            score += 0.2

        return min(score, 1.0)


@dataclass
class Skill:
    """Extracted skill that can be reused."""
    id: str
    name: str
    problem_pattern: str  # Regex pattern matching applicable problems
    solution_template: str
    verification_steps: List[str]
    extracted_from: str  # Session ID
    confidence: float
    reusability_score: float
    created_at: datetime = field(default_factory=datetime.now)
    use_count: int = 0
    success_rate: float = 1.0
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def matches(self, task: str) -> bool:
        """Check if this skill applies to the given task."""
        try:
            return bool(re.search(self.problem_pattern, task, re.IGNORECASE))
        except re.error:
            return False

    def to_dict(self) -> Dict[str, Any]:
        """Serialize skill to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "problem_pattern": self.problem_pattern,
            "solution_template": self.solution_template,
            "verification_steps": self.verification_steps,
            "extracted_from": self.extracted_from,
            "confidence": self.confidence,
            "reusability_score": self.reusability_score,
            "created_at": self.created_at.isoformat(),
            "use_count": self.use_count,
            "success_rate": self.success_rate,
            "tags": self.tags,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Skill":
        """Deserialize skill from dictionary."""
        data = data.copy()
        data["created_at"] = datetime.fromisoformat(data["created_at"])
        return cls(**data)


class SkillExtractor:
    """
    Extracts reusable skills from successful sessions.

    Quality Gates (all must pass):
    1. Solution length > 100 characters (not trivial)
    2. Verification passed (actually works)
    3. Not a documentation lookup (novel solution)
    4. Reusability score > 0.6 (generalizable)
    """

    QUALITY_GATES: List[Callable[[Session], bool]] = [
        lambda s: len(s.solution) > 100,           # Not trivial
        lambda s: s.verification_passed,            # Actually works
        lambda s: not s.is_documentation_lookup,    # Novel solution
        lambda s: s.reusability_score > 0.6,        # Generalizable
    ]

    def __init__(self, storage_path: Optional[Path] = None):
        self.storage_path = storage_path or Path.home() / ".usf" / "skills"
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.skills: Dict[str, Skill] = {}
        self._load_skills()

    def _load_skills(self):
        """Load persisted skills from storage."""
        skills_file = self.storage_path / "skills.json"
        if skills_file.exists():
            try:
                with open(skills_file, "r") as f:
                    data = json.load(f)
                    for skill_data in data.get("skills", []):
                        skill = Skill.from_dict(skill_data)
                        self.skills[skill.id] = skill
            except Exception:
                pass  # Start fresh if loading fails

    def _save_skills(self):
        """Persist skills to storage."""
        skills_file = self.storage_path / "skills.json"
        data = {
            "version": "1.0",
            "updated_at": datetime.now().isoformat(),
            "skills": [s.to_dict() for s in self.skills.values()]
        }
        with open(skills_file, "w") as f:
            json.dump(data, f, indent=2)

    def passes_quality_gates(self, session: Session) -> tuple[bool, List[str]]:
        """
        Check if session passes all quality gates.

        Returns: (passes: bool, failed_gates: List[str])
        """
        failed_gates = []

        gate_names = [
            "solution_length",
            "verification_passed",
            "not_documentation_lookup",
            "reusability_score"
        ]

        for gate, name in zip(self.QUALITY_GATES, gate_names):
            if not gate(session):
                failed_gates.append(name)

        return len(failed_gates) == 0, failed_gates

    def generate_name(self, task: str) -> str:
        """Generate a concise name for the skill from the task."""
        # Extract key action words
        task_lower = task.lower()

        # Common action patterns
        actions = ["fix", "implement", "create", "build", "analyze", "scan",
                  "exploit", "enumerate", "configure", "deploy", "test"]

        for action in actions:
            if action in task_lower:
                # Extract subject after action word
                pattern = rf'{action}\s+(?:the\s+)?(\w+(?:\s+\w+)?)'
                match = re.search(pattern, task_lower)
                if match:
                    return f"{action.title()} {match.group(1).title()}"

        # Fallback: use first few significant words
        words = re.findall(r'\b\w+\b', task)
        significant = [w for w in words if len(w) > 3 and w.lower() not in
                      {'the', 'this', 'that', 'with', 'from', 'into', 'about'}]
        return " ".join(significant[:3]).title()

    def generate_problem_pattern(self, task: str) -> str:
        """Generate a regex pattern matching similar problems."""
        # Extract key terms and create flexible pattern
        words = re.findall(r'\b\w{4,}\b', task.lower())

        # Remove very common words
        stopwords = {'this', 'that', 'with', 'from', 'into', 'about', 'should',
                    'would', 'could', 'please', 'want', 'need', 'help'}
        keywords = [w for w in words if w not in stopwords][:5]

        if not keywords:
            return re.escape(task[:50])  # Fallback to literal match

        # Create pattern requiring at least 2 keywords to match
        keyword_patterns = [rf'\b{re.escape(kw)}\b' for kw in keywords]
        return f"(?=.*{'|'.join(keyword_patterns[:3])})"

    def extract_verification_steps(self, solution: str) -> List[str]:
        """Extract verification steps from the solution."""
        steps = []

        # Look for explicit verification sections
        verify_section = re.search(
            r'(?:verification|test|validate|check).*?:(.*?)(?=\n\n|\Z)',
            solution,
            re.IGNORECASE | re.DOTALL
        )
        if verify_section:
            step_text = verify_section.group(1)
            # Extract numbered or bulleted items
            items = re.findall(r'(?:[-*•]|\d+\.)\s*(.+?)(?=\n|$)', step_text)
            steps.extend(items)

        # Look for test commands in code blocks
        code_blocks = re.findall(r'```(?:bash|sh)?\n(.+?)```', solution, re.DOTALL)
        for block in code_blocks:
            if any(t in block.lower() for t in ['test', 'verify', 'check', 'assert']):
                steps.append(f"Run: {block.strip()[:100]}")

        # Fallback: basic verification
        if not steps:
            steps = ["Verify the solution addresses the original problem"]

        return steps[:5]  # Limit to 5 steps

    def extract_tags(self, task: str, solution: str) -> List[str]:
        """Extract relevant tags from task and solution."""
        tags = set()

        # Domain detection
        domain_patterns = {
            "security": ["security", "vulnerability", "exploit", "attack", "pentest"],
            "web": ["http", "api", "endpoint", "web", "html", "javascript"],
            "network": ["port", "scan", "tcp", "udp", "socket", "network"],
            "linux": ["linux", "bash", "shell", "sudo", "chmod", "grep"],
            "windows": ["windows", "powershell", "registry", "active directory"],
            "python": ["python", "pip", "venv", "flask", "django"],
            "database": ["sql", "database", "query", "postgresql", "mysql"],
        }

        combined = (task + " " + solution).lower()
        for tag, patterns in domain_patterns.items():
            if any(p in combined for p in patterns):
                tags.add(tag)

        return list(tags)

    async def extract(self, session: Session) -> Optional[Skill]:
        """
        Attempt to extract a skill from a completed session.

        Returns: Skill if extraction successful, None if quality gates fail
        """
        # Check quality gates
        passes, failed_gates = self.passes_quality_gates(session)
        if not passes:
            return None

        # Generate skill ID
        skill_id = hashlib.sha256(
            f"{session.task}:{session.id}".encode()
        ).hexdigest()[:16]

        # Check for duplicate
        if skill_id in self.skills:
            return self.skills[skill_id]

        skill = Skill(
            id=skill_id,
            name=self.generate_name(session.task),
            problem_pattern=self.generate_problem_pattern(session.task),
            solution_template=session.solution,
            verification_steps=self.extract_verification_steps(session.solution),
            extracted_from=session.id,
            confidence=session.confidence,
            reusability_score=session.reusability_score,
            tags=self.extract_tags(session.task, session.solution),
            metadata={
                "original_task": session.task,
                "latency_seconds": session.latency_seconds,
            }
        )

        await self.store(skill)
        return skill

    async def store(self, skill: Skill):
        """Store a skill to the registry."""
        self.skills[skill.id] = skill
        self._save_skills()

    def find_applicable(self, task: str, top_k: int = 3) -> List[Skill]:
        """
        Find skills applicable to the given task.

        Returns skills sorted by relevance and confidence.
        """
        matches = []
        for skill in self.skills.values():
            if skill.matches(task):
                # Score by confidence and success rate
                score = skill.confidence * skill.success_rate * skill.reusability_score
                matches.append((score, skill))

        # Sort by score descending
        matches.sort(key=lambda x: x[0], reverse=True)
        return [skill for _, skill in matches[:top_k]]

    def record_usage(self, skill_id: str, success: bool):
        """Record skill usage for learning."""
        if skill_id in self.skills:
            skill = self.skills[skill_id]
            skill.use_count += 1
            # Exponential moving average for success rate
            alpha = 0.1
            skill.success_rate = (
                skill.success_rate * (1 - alpha) +
                (1.0 if success else 0.0) * alpha
            )
            self._save_skills()

    def get_stats(self) -> Dict[str, Any]:
        """Get skill extractor statistics."""
        if not self.skills:
            return {
                "total_skills": 0,
                "avg_confidence": 0.0,
                "avg_reusability": 0.0,
                "avg_success_rate": 0.0,
                "total_uses": 0,
                "tags": {},
            }

        skills = list(self.skills.values())
        tag_counts: Dict[str, int] = {}
        for skill in skills:
            for tag in skill.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

        return {
            "total_skills": len(skills),
            "avg_confidence": sum(s.confidence for s in skills) / len(skills),
            "avg_reusability": sum(s.reusability_score for s in skills) / len(skills),
            "avg_success_rate": sum(s.success_rate for s in skills) / len(skills),
            "total_uses": sum(s.use_count for s in skills),
            "tags": tag_counts,
        }


# Global extractor instance (lazy initialization)
_extractor: Optional[SkillExtractor] = None


def get_extractor(storage_path: Optional[Path] = None) -> SkillExtractor:
    """Get or create the global skill extractor instance."""
    global _extractor
    if _extractor is None:
        _extractor = SkillExtractor(storage_path=storage_path)
    return _extractor


# CLI for testing
if __name__ == "__main__":
    import asyncio

    async def test():
        extractor = SkillExtractor()

        # Create a test session
        session = Session(
            id="test_session_001",
            task="Fix SQL injection vulnerability in the login endpoint",
            solution="""
## Solution

The SQL injection vulnerability was in the login handler. Here's the fix:

```python
# Before (vulnerable)
query = f"SELECT * FROM users WHERE username = '{username}'"

# After (parameterized)
query = "SELECT * FROM users WHERE username = ?"
cursor.execute(query, (username,))
```

[FINDING] SQL injection in login endpoint
[STAT:CONFIDENCE] 0.95
[STAT:SEVERITY] Critical

## Verification Steps:
1. Run the SQL injection test payload: `admin' OR '1'='1' --`
2. Verify it no longer bypasses authentication
3. Run the full security test suite
""",
            verification_passed=True,
            confidence=0.95,
            latency_seconds=12.5,
        )

        print("Testing Skill Extraction")
        print("=" * 60)
        print(f"Session ID: {session.id}")
        print(f"Task: {session.task}")
        print(f"Reusability Score: {session.reusability_score:.2f}")
        print()

        # Check quality gates
        passes, failed = extractor.passes_quality_gates(session)
        print(f"Quality Gates: {'PASS' if passes else 'FAIL'}")
        if failed:
            print(f"  Failed: {failed}")
        print()

        # Extract skill
        skill = await extractor.extract(session)
        if skill:
            print("Extracted Skill:")
            print(f"  ID: {skill.id}")
            print(f"  Name: {skill.name}")
            print(f"  Pattern: {skill.problem_pattern}")
            print(f"  Tags: {skill.tags}")
            print(f"  Verification Steps: {len(skill.verification_steps)}")
            for step in skill.verification_steps:
                print(f"    - {step[:60]}...")
        else:
            print("Skill extraction failed (quality gates not met)")

        print()
        print("Extractor Stats:", extractor.get_stats())

    asyncio.run(test())
