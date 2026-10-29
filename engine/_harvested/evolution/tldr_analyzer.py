"""
5-Layer TLDR Analyzer for USF Multi-Agent Output Processing.

USF 7.0 Implementation - Hierarchical summarization at 5 detail levels.

Based on patterns from:
- claude-engineer: Hierarchical context management
- aider: Progressive disclosure retrieval
- cursor-tools: Multi-level summaries

Layers:
- L1: One-liner (10-15 words) - Tweet-sized
- L2: Paragraph (50-100 words) - Executive summary
- L3: Section (200-500 words) - Key findings with evidence
- L4: Detailed (1000-2000 words) - Full analysis with context
- L5: Complete (unlimited) - Raw output with all details

Use Cases:
- L1: Status dashboards, notifications
- L2: Executive briefings, quick reviews
- L3: Technical summaries, reports
- L4: Deep analysis, audits
- L5: Archives, debugging, full context
"""

import re
import hashlib
from dataclasses import dataclass, field
from datetime import datetime
from enum import IntEnum
from typing import Any, Dict, List, Optional, Tuple
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class TLDRLevel(IntEnum):
    """TLDR detail levels (1=brief, 5=complete)."""
    ONE_LINER = 1
    PARAGRAPH = 2
    SECTION = 3
    DETAILED = 4
    COMPLETE = 5


@dataclass
class TLDRResult:
    """Result at a specific TLDR level."""
    level: TLDRLevel
    content: str
    word_count: int
    token_estimate: int  # Rough estimate: words * 1.3
    key_findings: List[str] = field(default_factory=list)
    confidence: float = 0.0
    generated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "level": self.level.value,
            "level_name": self.level.name,
            "content": self.content,
            "word_count": self.word_count,
            "token_estimate": self.token_estimate,
            "key_findings": self.key_findings,
            "confidence": self.confidence,
            "generated_at": self.generated_at.isoformat(),
        }


@dataclass
class TLDRStack:
    """Complete 5-layer TLDR stack for a document/output."""
    source_id: str
    source_hash: str
    layers: Dict[TLDRLevel, TLDRResult] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

    def get_level(self, level: TLDRLevel) -> Optional[TLDRResult]:
        """Get TLDR at specific level."""
        return self.layers.get(level)

    def get_best_fit(self, max_tokens: int) -> Optional[TLDRResult]:
        """Get highest detail level that fits in token budget."""
        for level in sorted(self.layers.keys(), reverse=True):
            result = self.layers[level]
            if result.token_estimate <= max_tokens:
                return result
        return self.layers.get(TLDRLevel.ONE_LINER)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_id": self.source_id,
            "source_hash": self.source_hash,
            "layers": {k.value: v.to_dict() for k, v in self.layers.items()},
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }


class TLDRAnalyzer:
    """
    Hierarchical summarization engine.

    Generates 5 levels of summary from any text input,
    optimized for different consumption contexts.
    """

    # Target word counts per level
    LEVEL_TARGETS = {
        TLDRLevel.ONE_LINER: (10, 20),
        TLDRLevel.PARAGRAPH: (50, 100),
        TLDRLevel.SECTION: (200, 500),
        TLDRLevel.DETAILED: (1000, 2000),
        TLDRLevel.COMPLETE: (0, float('inf')),
    }

    # Structured marker patterns for extraction
    MARKER_PATTERNS = {
        "finding": re.compile(r'\[FINDING\]\s*(.+?)(?=\[|$)', re.DOTALL),
        "confidence": re.compile(r'\[STAT:CONFIDENCE\]\s*([\d.]+)'),
        "severity": re.compile(r'\[STAT:SEVERITY\]\s*(.+?)(?=\[|$)'),
        "data": re.compile(r'\[DATA\]\s*(.+?)(?=\[|$)', re.DOTALL),
        "limitation": re.compile(r'\[LIMITATION\]\s*(.+?)(?=\[|$)', re.DOTALL),
    }

    def __init__(self, cache_path: Optional[Path] = None):
        """
        Initialize TLDR analyzer.

        Args:
            cache_path: Optional path to cache generated TLDRs
        """
        self.cache_path = cache_path
        self._cache: Dict[str, TLDRStack] = {}

        if cache_path:
            self._load_cache()

    def _compute_hash(self, content: str) -> str:
        """Compute content hash for caching."""
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def _load_cache(self):
        """Load cached TLDRs from disk."""
        if not self.cache_path or not self.cache_path.exists():
            return

        try:
            with open(self.cache_path, "r") as f:
                data = json.load(f)
                for item in data.get("stacks", []):
                    stack = self._deserialize_stack(item)
                    self._cache[stack.source_hash] = stack
        except Exception as e:
            logger.warning(f"Failed to load TLDR cache: {e}")

    def _save_cache(self):
        """Save cache to disk."""
        if not self.cache_path:
            return

        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "version": "1.0",
            "updated_at": datetime.now().isoformat(),
            "stacks": [s.to_dict() for s in self._cache.values()]
        }
        with open(self.cache_path, "w") as f:
            json.dump(data, f, indent=2)

    def _deserialize_stack(self, data: Dict) -> TLDRStack:
        """Deserialize TLDRStack from dict."""
        stack = TLDRStack(
            source_id=data["source_id"],
            source_hash=data["source_hash"],
            metadata=data.get("metadata", {}),
            created_at=datetime.fromisoformat(data["created_at"]),
        )
        for level_val, result_data in data.get("layers", {}).items():
            level = TLDRLevel(int(level_val))
            stack.layers[level] = TLDRResult(
                level=level,
                content=result_data["content"],
                word_count=result_data["word_count"],
                token_estimate=result_data["token_estimate"],
                key_findings=result_data.get("key_findings", []),
                confidence=result_data.get("confidence", 0.0),
                generated_at=datetime.fromisoformat(result_data["generated_at"]),
            )
        return stack

    def extract_structured_data(self, content: str) -> Dict[str, Any]:
        """
        Extract structured data from content with markers.

        Returns dict with findings, confidence scores, etc.
        """
        extracted = {
            "findings": [],
            "confidence_scores": [],
            "severities": [],
            "data_points": [],
            "limitations": [],
        }

        for match in self.MARKER_PATTERNS["finding"].finditer(content):
            extracted["findings"].append(match.group(1).strip())

        for match in self.MARKER_PATTERNS["confidence"].finditer(content):
            try:
                extracted["confidence_scores"].append(float(match.group(1)))
            except ValueError:
                pass

        for match in self.MARKER_PATTERNS["severity"].finditer(content):
            extracted["severities"].append(match.group(1).strip())

        for match in self.MARKER_PATTERNS["data"].finditer(content):
            extracted["data_points"].append(match.group(1).strip())

        for match in self.MARKER_PATTERNS["limitation"].finditer(content):
            extracted["limitations"].append(match.group(1).strip())

        return extracted

    def _extract_key_sentences(self, content: str, max_sentences: int = 10) -> List[str]:
        """Extract key sentences from content."""
        # Split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', content)

        # Score sentences by importance signals
        scored = []
        for sent in sentences:
            score = 0
            sent_lower = sent.lower()

            # Boost for key phrases
            if any(kw in sent_lower for kw in ["critical", "important", "key", "major"]):
                score += 3
            if any(kw in sent_lower for kw in ["found", "discovered", "identified"]):
                score += 2
            if any(kw in sent_lower for kw in ["vulnerability", "issue", "problem", "risk"]):
                score += 2
            if any(kw in sent_lower for kw in ["recommend", "should", "must"]):
                score += 1

            # Boost for structured markers
            if "[FINDING]" in sent or "[STAT:" in sent:
                score += 5

            # Penalize very short or very long sentences
            word_count = len(sent.split())
            if word_count < 5 or word_count > 50:
                score -= 1

            scored.append((score, sent))

        # Sort by score and return top sentences
        scored.sort(key=lambda x: x[0], reverse=True)
        return [s[1] for s in scored[:max_sentences]]

    def _generate_one_liner(self, content: str, extracted: Dict) -> str:
        """Generate L1: One-liner summary (10-20 words)."""
        # If we have findings, use the first one
        if extracted["findings"]:
            finding = extracted["findings"][0]
            # Truncate to ~15 words
            words = finding.split()[:15]
            return " ".join(words) + ("..." if len(finding.split()) > 15 else "")

        # Otherwise, extract first meaningful sentence
        key_sentences = self._extract_key_sentences(content, 1)
        if key_sentences:
            words = key_sentences[0].split()[:15]
            return " ".join(words) + ("..." if len(key_sentences[0].split()) > 15 else "")

        # Fallback: first 15 words
        words = content.split()[:15]
        return " ".join(words) + "..."

    def _generate_paragraph(self, content: str, extracted: Dict) -> str:
        """Generate L2: Paragraph summary (50-100 words)."""
        parts = []

        # Add confidence if available
        if extracted["confidence_scores"]:
            avg_conf = sum(extracted["confidence_scores"]) / len(extracted["confidence_scores"])
            parts.append(f"Overall confidence: {avg_conf:.0%}.")

        # Add key findings
        if extracted["findings"]:
            parts.append(f"Key findings ({len(extracted['findings'])}):")
            for finding in extracted["findings"][:3]:
                # Truncate each finding
                words = finding.split()[:20]
                parts.append("- " + " ".join(words))

        # Add limitations if present
        if extracted["limitations"]:
            parts.append(f"Limitations: {extracted['limitations'][0][:100]}")

        result = " ".join(parts)

        # If too short, add key sentences
        if len(result.split()) < 50:
            key_sentences = self._extract_key_sentences(content, 3)
            result += " " + " ".join(key_sentences)

        # Truncate to ~100 words
        words = result.split()[:100]
        return " ".join(words)

    def _generate_section(self, content: str, extracted: Dict) -> str:
        """Generate L3: Section summary (200-500 words)."""
        sections = []

        # Overview
        sections.append("## Summary")
        if extracted["confidence_scores"]:
            avg_conf = sum(extracted["confidence_scores"]) / len(extracted["confidence_scores"])
            sections.append(f"Analysis completed with {avg_conf:.0%} average confidence.")

        # Findings
        if extracted["findings"]:
            sections.append(f"\n## Key Findings ({len(extracted['findings'])})")
            for i, finding in enumerate(extracted["findings"][:5], 1):
                sections.append(f"{i}. {finding[:200]}")

        # Severity breakdown
        if extracted["severities"]:
            sections.append("\n## Severity Breakdown")
            severity_counts = {}
            for sev in extracted["severities"]:
                sev_lower = sev.lower()
                if "critical" in sev_lower:
                    severity_counts["Critical"] = severity_counts.get("Critical", 0) + 1
                elif "high" in sev_lower:
                    severity_counts["High"] = severity_counts.get("High", 0) + 1
                elif "medium" in sev_lower:
                    severity_counts["Medium"] = severity_counts.get("Medium", 0) + 1
                else:
                    severity_counts["Low/Info"] = severity_counts.get("Low/Info", 0) + 1

            for sev, count in sorted(severity_counts.items()):
                sections.append(f"- {sev}: {count}")

        # Supporting data
        if extracted["data_points"]:
            sections.append("\n## Supporting Evidence")
            for data in extracted["data_points"][:3]:
                sections.append(f"- {data[:150]}")

        # Limitations
        if extracted["limitations"]:
            sections.append("\n## Limitations")
            for lim in extracted["limitations"][:2]:
                sections.append(f"- {lim[:150]}")

        result = "\n".join(sections)

        # If too short, add key sentences
        if len(result.split()) < 200:
            key_sentences = self._extract_key_sentences(content, 10)
            result += "\n\n## Additional Context\n" + " ".join(key_sentences)

        # Truncate to ~500 words
        words = result.split()[:500]
        return " ".join(words)

    def _generate_detailed(self, content: str, extracted: Dict) -> str:
        """Generate L4: Detailed summary (1000-2000 words)."""
        sections = []

        # Executive summary
        sections.append("# Detailed Analysis Report")
        sections.append("\n## Executive Summary")
        paragraph = self._generate_paragraph(content, extracted)
        sections.append(paragraph)

        # Full findings with context
        sections.append("\n## Comprehensive Findings")
        if extracted["findings"]:
            for i, finding in enumerate(extracted["findings"], 1):
                sections.append(f"\n### Finding {i}")
                sections.append(finding)

                # Add related confidence if available
                if i <= len(extracted["confidence_scores"]):
                    sections.append(f"\n*Confidence: {extracted['confidence_scores'][i-1]:.0%}*")

                # Add related severity if available
                if i <= len(extracted["severities"]):
                    sections.append(f"\n*Severity: {extracted['severities'][i-1]}*")

        # All supporting data
        if extracted["data_points"]:
            sections.append("\n## Supporting Evidence")
            for i, data in enumerate(extracted["data_points"], 1):
                sections.append(f"\n### Evidence {i}")
                sections.append(data)

        # Methodology notes (extracted from content)
        sections.append("\n## Analysis Context")
        key_sentences = self._extract_key_sentences(content, 15)
        sections.append(" ".join(key_sentences))

        # All limitations
        if extracted["limitations"]:
            sections.append("\n## Scope and Limitations")
            for lim in extracted["limitations"]:
                sections.append(f"- {lim}")

        result = "\n".join(sections)

        # Truncate to ~2000 words
        words = result.split()[:2000]
        return " ".join(words)

    def analyze(
        self,
        content: str,
        source_id: str = "unknown",
        levels: Optional[List[TLDRLevel]] = None,
        use_cache: bool = True
    ) -> TLDRStack:
        """
        Generate TLDR stack for content.

        Args:
            content: Text content to summarize
            source_id: Identifier for the source
            levels: Specific levels to generate (default: all)
            use_cache: Whether to use cached results

        Returns:
            TLDRStack with summaries at each level
        """
        content_hash = self._compute_hash(content)

        # Check cache
        if use_cache and content_hash in self._cache:
            cached = self._cache[content_hash]
            # Return if we have all requested levels
            if levels is None or all(l in cached.layers for l in levels):
                return cached

        # Extract structured data first
        extracted = self.extract_structured_data(content)

        # Calculate overall confidence
        avg_confidence = 0.0
        if extracted["confidence_scores"]:
            avg_confidence = sum(extracted["confidence_scores"]) / len(extracted["confidence_scores"])

        # Create stack
        stack = TLDRStack(
            source_id=source_id,
            source_hash=content_hash,
            metadata={
                "finding_count": len(extracted["findings"]),
                "has_structured_markers": bool(extracted["findings"]),
            }
        )

        # Generate requested levels
        levels_to_generate = levels or list(TLDRLevel)

        for level in levels_to_generate:
            if level == TLDRLevel.ONE_LINER:
                text = self._generate_one_liner(content, extracted)
            elif level == TLDRLevel.PARAGRAPH:
                text = self._generate_paragraph(content, extracted)
            elif level == TLDRLevel.SECTION:
                text = self._generate_section(content, extracted)
            elif level == TLDRLevel.DETAILED:
                text = self._generate_detailed(content, extracted)
            else:  # COMPLETE
                text = content

            word_count = len(text.split())
            stack.layers[level] = TLDRResult(
                level=level,
                content=text,
                word_count=word_count,
                token_estimate=int(word_count * 1.3),
                key_findings=extracted["findings"][:5],
                confidence=avg_confidence,
            )

        # Cache and save
        self._cache[content_hash] = stack
        self._save_cache()

        return stack

    def get_for_budget(
        self,
        content: str,
        token_budget: int,
        source_id: str = "unknown"
    ) -> TLDRResult:
        """
        Get the most detailed summary that fits in token budget.

        Args:
            content: Text content
            token_budget: Maximum tokens allowed
            source_id: Source identifier

        Returns:
            TLDRResult at appropriate level
        """
        stack = self.analyze(content, source_id)
        return stack.get_best_fit(token_budget)

    def batch_analyze(
        self,
        items: List[Tuple[str, str]],  # (content, source_id) pairs
        levels: Optional[List[TLDRLevel]] = None
    ) -> List[TLDRStack]:
        """
        Analyze multiple items.

        Args:
            items: List of (content, source_id) tuples
            levels: Levels to generate

        Returns:
            List of TLDRStacks
        """
        return [
            self.analyze(content, source_id, levels)
            for content, source_id in items
        ]

    def get_stats(self) -> Dict[str, Any]:
        """Get analyzer statistics."""
        return {
            "cached_stacks": len(self._cache),
            "cache_path": str(self.cache_path) if self.cache_path else None,
        }


# Global analyzer instance
_analyzer: Optional[TLDRAnalyzer] = None


def get_tldr_analyzer(cache_path: Optional[Path] = None) -> TLDRAnalyzer:
    """Get or create the global TLDR analyzer."""
    global _analyzer
    if _analyzer is None:
        _analyzer = TLDRAnalyzer(cache_path=cache_path)
    return _analyzer


# CLI for testing
if __name__ == "__main__":
    print("5-Layer TLDR Analyzer Test")
    print("=" * 60)

    # Test content with structured markers
    test_content = """
    [FINDING] SQL injection vulnerability in login endpoint
    [STAT:CONFIDENCE] 0.95
    [STAT:SEVERITY] Critical (CVSS 9.8)
    [DATA] Payload tested: admin' OR '1'='1' --

    The authentication system uses string concatenation for SQL queries
    without proper parameterization. This allows attackers to bypass
    authentication entirely and gain unauthorized access.

    [FINDING] Cross-site scripting in user profile page
    [STAT:CONFIDENCE] 0.88
    [STAT:SEVERITY] High (CVSS 7.5)
    [DATA] Payload: <script>alert(document.cookie)</script>

    User-supplied input in the bio field is rendered without escaping,
    allowing stored XSS attacks that could steal session cookies.

    [FINDING] Missing rate limiting on API endpoints
    [STAT:CONFIDENCE] 0.92
    [STAT:SEVERITY] Medium (CVSS 5.3)

    [LIMITATION] Only tested unauthenticated endpoints
    [LIMITATION] Internal network testing not performed
    """

    analyzer = TLDRAnalyzer()
    stack = analyzer.analyze(test_content, source_id="security_audit_001")

    for level in TLDRLevel:
        result = stack.get_level(level)
        if result:
            print(f"\n{'='*60}")
            print(f"LEVEL {level.value}: {level.name}")
            print(f"Words: {result.word_count} | Tokens: ~{result.token_estimate}")
            print(f"Confidence: {result.confidence:.0%}")
            print("-" * 60)
            print(result.content[:500] + ("..." if len(result.content) > 500 else ""))

    # Test budget-based retrieval
    print(f"\n{'='*60}")
    print("Budget-Based Retrieval Test")
    print("-" * 60)
    for budget in [50, 200, 500, 2000]:
        result = analyzer.get_for_budget(test_content, budget)
        print(f"Budget {budget} tokens → Level {result.level.value} ({result.level.name})")
