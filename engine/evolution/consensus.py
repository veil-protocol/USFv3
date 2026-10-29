"""
Byzantine Fault Tolerant Consensus for USF Multi-Agent Verification.

USF 7.0 Implementation - Survives f < n/3 failures.

Based on patterns from:
- claude-flow: Multi-agent consensus
- practical Byzantine fault tolerance literature

Key properties:
- Tolerates up to f < n/3 faulty/malicious agents
- Early exit when consensus threshold reached
- Timeout handling for non-responsive agents
- Confidence-weighted voting
"""

import asyncio
import time
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable, Dict, List, Optional, Tuple
from enum import Enum
import hashlib
import json


class ConsensusFailure(Exception):
    """Raised when consensus cannot be reached."""
    pass


class VoteType(Enum):
    """Types of votes in consensus."""
    AGREE = "agree"
    DISAGREE = "disagree"
    ABSTAIN = "abstain"
    TIMEOUT = "timeout"


@dataclass
class AgentResult:
    """Result from a single agent in the consensus round."""
    agent_id: str
    output: Any
    confidence: float
    latency_seconds: float
    vote: VoteType = VoteType.AGREE
    reasoning: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def content_hash(self) -> str:
        """Hash of output for comparison."""
        content = json.dumps(self.output, sort_keys=True, default=str)
        return hashlib.sha256(content.encode()).hexdigest()[:16]


@dataclass
class ConsensusResult:
    """Aggregated consensus result."""
    consensus_reached: bool
    final_output: Any
    confidence: float
    agreement_ratio: float
    total_agents: int
    responding_agents: int
    agreeing_agents: int
    results: List[AgentResult]
    consensus_time_seconds: float
    early_exit: bool = False
    method: str = "byzantine"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "consensus_reached": self.consensus_reached,
            "confidence": self.confidence,
            "agreement_ratio": self.agreement_ratio,
            "total_agents": self.total_agents,
            "responding_agents": self.responding_agents,
            "agreeing_agents": self.agreeing_agents,
            "consensus_time_seconds": self.consensus_time_seconds,
            "early_exit": self.early_exit,
            "method": self.method,
        }


def _extract_confidence(result: Any) -> float:
    """Extract confidence from various result formats."""
    if isinstance(result, dict):
        # Check common confidence fields
        for key in ['confidence', 'score', 'certainty', 'probability']:
            if key in result:
                val = result[key]
                if isinstance(val, (int, float)):
                    return float(val)
        # Check nested stats
        if 'stats' in result and 'confidence' in result['stats']:
            return float(result['stats']['confidence'])
    elif isinstance(result, (int, float)):
        return float(result)
    elif isinstance(result, str):
        # Try to parse confidence markers
        import re
        match = re.search(r'\[STAT:CONFIDENCE\]\s*([\d.]+)', result)
        if match:
            return float(match.group(1))
    return 0.5  # Default confidence


def _results_match(r1: Any, r2: Any, similarity_threshold: float = 0.8) -> bool:
    """
    Check if two results are similar enough to be considered matching.

    For structured outputs, compares key findings.
    For text outputs, uses simple overlap metric.
    """
    if r1 == r2:
        return True

    # Convert to strings for comparison
    s1 = json.dumps(r1, sort_keys=True, default=str) if not isinstance(r1, str) else r1
    s2 = json.dumps(r2, sort_keys=True, default=str) if not isinstance(r2, str) else r2

    # Simple word overlap similarity
    words1 = set(s1.lower().split())
    words2 = set(s2.lower().split())

    if not words1 or not words2:
        return False

    intersection = len(words1 & words2)
    union = len(words1 | words2)
    similarity = intersection / union if union > 0 else 0

    return similarity >= similarity_threshold


def _find_majority_cluster(results: List[AgentResult], threshold: float = 0.67) -> Tuple[List[AgentResult], Any]:
    """
    Find the largest cluster of matching results.

    Returns: (matching_results, representative_output)
    """
    if not results:
        return [], None

    # Group by content hash (exact matches)
    hash_groups: Dict[str, List[AgentResult]] = {}
    for r in results:
        h = r.content_hash
        if h not in hash_groups:
            hash_groups[h] = []
        hash_groups[h].append(r)

    # Find largest exact-match group
    if hash_groups:
        largest_group = max(hash_groups.values(), key=len)
        if len(largest_group) / len(results) >= threshold:
            return largest_group, largest_group[0].output

    # Fall back to similarity matching
    clusters: List[List[AgentResult]] = []
    for r in results:
        matched = False
        for cluster in clusters:
            if _results_match(r.output, cluster[0].output):
                cluster.append(r)
                matched = True
                break
        if not matched:
            clusters.append([r])

    if clusters:
        largest_cluster = max(clusters, key=len)
        if len(largest_cluster) / len(results) >= threshold:
            # Return highest confidence result as representative
            best = max(largest_cluster, key=lambda x: x.confidence)
            return largest_cluster, best.output

    return [], None


def aggregate(results: List[AgentResult]) -> Any:
    """
    Aggregate results using confidence-weighted combination.

    For matching results, combines with confidence weighting.
    For divergent results, returns highest confidence result.
    """
    if not results:
        return None

    if len(results) == 1:
        return results[0].output

    # Find majority cluster
    matching, representative = _find_majority_cluster(results)
    if matching:
        # Calculate weighted confidence
        total_weight = sum(r.confidence for r in matching)
        weighted_confidence = sum(r.confidence ** 2 for r in matching) / total_weight if total_weight > 0 else 0

        if isinstance(representative, dict):
            representative['_consensus'] = {
                'agreeing_agents': len(matching),
                'weighted_confidence': weighted_confidence,
            }
        return representative

    # No consensus - return highest confidence
    best = max(results, key=lambda x: x.confidence)
    return best.output


def has_consensus(results: List[AgentResult], threshold: float = 0.67) -> bool:
    """Check if results have reached consensus threshold."""
    if not results:
        return False

    matching, _ = _find_majority_cluster(results, threshold)
    return len(matching) / len(results) >= threshold


async def byzantine_consensus(
    chains: List[Awaitable[Any]],
    threshold: float = 0.67,
    timeout: int = 30,
    early_exit: bool = True,
    min_responses: Optional[int] = None
) -> ConsensusResult:
    """
    Byzantine fault tolerant consensus across multiple verification chains.

    Survives f < n/3 failures while reaching consensus among honest agents.

    Args:
        chains: List of awaitable verification chain coroutines
        threshold: Fraction of agents that must agree (default 0.67 = 2/3)
        timeout: Maximum seconds to wait for all agents
        early_exit: If True, return early when consensus threshold reached
        min_responses: Minimum responses needed before checking consensus

    Returns:
        ConsensusResult with aggregated output and confidence

    Raises:
        ConsensusFailure if insufficient agents respond or agree
    """
    start_time = time.time()
    n = len(chains)

    if n == 0:
        raise ConsensusFailure("No chains provided")

    # Calculate minimum responses needed
    if min_responses is None:
        min_responses = max(1, int(n * threshold))

    results: List[AgentResult] = []
    completed = 0
    failed = 0

    async def run_chain(idx: int, chain: Awaitable) -> Optional[AgentResult]:
        """Run a single chain with error handling."""
        chain_start = time.time()
        try:
            output = await chain
            latency = time.time() - chain_start
            confidence = _extract_confidence(output)

            return AgentResult(
                agent_id=f"chain_{idx}",
                output=output,
                confidence=confidence,
                latency_seconds=latency,
                vote=VoteType.AGREE,
            )
        except asyncio.TimeoutError:
            return AgentResult(
                agent_id=f"chain_{idx}",
                output=None,
                confidence=0.0,
                latency_seconds=time.time() - chain_start,
                vote=VoteType.TIMEOUT,
            )
        except Exception as e:
            return AgentResult(
                agent_id=f"chain_{idx}",
                output=None,
                confidence=0.0,
                latency_seconds=time.time() - chain_start,
                vote=VoteType.ABSTAIN,
                reasoning=str(e),
            )

    # Run all chains with timeout
    try:
        async with asyncio.timeout(timeout):
            # Use as_completed for early exit capability
            pending = [run_chain(i, chain) for i, chain in enumerate(chains)]

            for coro in asyncio.as_completed(pending):
                result = await coro

                if result and result.vote == VoteType.AGREE:
                    results.append(result)
                    completed += 1

                    # Early exit check
                    if early_exit and completed >= min_responses:
                        if has_consensus(results, threshold):
                            # Consensus reached early
                            agreeing, output = _find_majority_cluster(results, threshold)
                            elapsed = time.time() - start_time

                            return ConsensusResult(
                                consensus_reached=True,
                                final_output=aggregate(results),
                                confidence=sum(r.confidence for r in agreeing) / len(agreeing),
                                agreement_ratio=len(agreeing) / n,
                                total_agents=n,
                                responding_agents=completed,
                                agreeing_agents=len(agreeing),
                                results=results,
                                consensus_time_seconds=elapsed,
                                early_exit=True,
                            )
                else:
                    failed += 1

    except asyncio.TimeoutError:
        # Timeout - work with what we have
        pass

    # Final consensus check
    elapsed = time.time() - start_time

    if completed < min_responses:
        raise ConsensusFailure(
            f"Only {completed}/{n} chains completed (need {min_responses})"
        )

    agreeing, output = _find_majority_cluster(results, threshold)

    if len(agreeing) / n >= threshold:
        return ConsensusResult(
            consensus_reached=True,
            final_output=aggregate(results),
            confidence=sum(r.confidence for r in agreeing) / len(agreeing),
            agreement_ratio=len(agreeing) / n,
            total_agents=n,
            responding_agents=completed,
            agreeing_agents=len(agreeing),
            results=results,
            consensus_time_seconds=elapsed,
            early_exit=False,
        )
    else:
        # No consensus - return best effort
        best = max(results, key=lambda x: x.confidence) if results else None
        return ConsensusResult(
            consensus_reached=False,
            final_output=best.output if best else None,
            confidence=best.confidence if best else 0.0,
            agreement_ratio=len(agreeing) / n if agreeing else 0.0,
            total_agents=n,
            responding_agents=completed,
            agreeing_agents=len(agreeing),
            results=results,
            consensus_time_seconds=elapsed,
            early_exit=False,
        )


async def weighted_consensus(
    chains: List[Awaitable[Any]],
    weights: Optional[List[float]] = None,
    timeout: int = 30
) -> ConsensusResult:
    """
    Confidence-weighted consensus without strict Byzantine requirements.

    Useful when you trust all agents but want weighted combination.
    """
    results: List[AgentResult] = []
    n = len(chains)
    start_time = time.time()

    if weights is None:
        weights = [1.0] * n

    async def run_chain(idx: int, chain: Awaitable, weight: float) -> Optional[AgentResult]:
        chain_start = time.time()
        try:
            output = await chain
            latency = time.time() - chain_start
            confidence = _extract_confidence(output) * weight

            return AgentResult(
                agent_id=f"chain_{idx}",
                output=output,
                confidence=confidence,
                latency_seconds=latency,
                vote=VoteType.AGREE,
                metadata={"weight": weight}
            )
        except Exception as e:
            return AgentResult(
                agent_id=f"chain_{idx}",
                output=None,
                confidence=0.0,
                latency_seconds=time.time() - chain_start,
                vote=VoteType.ABSTAIN,
                reasoning=str(e),
            )

    try:
        async with asyncio.timeout(timeout):
            tasks = [run_chain(i, chain, weights[i]) for i, chain in enumerate(chains)]
            results = [r for r in await asyncio.gather(*tasks) if r and r.vote == VoteType.AGREE]
    except asyncio.TimeoutError:
        pass

    elapsed = time.time() - start_time

    if not results:
        raise ConsensusFailure("No chains completed successfully")

    # Weighted combination
    total_weight = sum(r.confidence for r in results)
    weighted_confidence = sum(r.confidence ** 2 for r in results) / total_weight if total_weight > 0 else 0

    # Use highest weighted result as output
    best = max(results, key=lambda x: x.confidence)

    return ConsensusResult(
        consensus_reached=True,
        final_output=best.output,
        confidence=weighted_confidence,
        agreement_ratio=len(results) / n,
        total_agents=n,
        responding_agents=len(results),
        agreeing_agents=len(results),
        results=results,
        consensus_time_seconds=elapsed,
        method="weighted",
    )


# CLI for testing
if __name__ == "__main__":
    import random

    async def mock_chain(idx: int, should_agree: bool = True, delay: float = 0.1):
        """Mock verification chain for testing."""
        await asyncio.sleep(delay + random.random() * 0.1)

        if should_agree:
            return {
                "finding": f"Security issue found by chain {idx}",
                "confidence": 0.8 + random.random() * 0.15,
                "severity": "high",
            }
        else:
            return {
                "finding": f"Different finding by chain {idx}",
                "confidence": 0.5 + random.random() * 0.2,
                "severity": "medium",
            }

    async def test():
        print("Byzantine Consensus Test")
        print("=" * 60)

        # Test 1: All agents agree
        print("\nTest 1: All agents agree")
        chains = [mock_chain(i, True) for i in range(5)]
        result = await byzantine_consensus(chains, threshold=0.67)
        print(f"  Consensus: {result.consensus_reached}")
        print(f"  Agreement: {result.agreement_ratio:.0%}")
        print(f"  Confidence: {result.confidence:.2f}")
        print(f"  Early exit: {result.early_exit}")
        print(f"  Time: {result.consensus_time_seconds:.3f}s")

        # Test 2: Byzantine fault (1/3 disagree)
        print("\nTest 2: Byzantine fault (1 of 3 disagree)")
        chains = [mock_chain(0, True), mock_chain(1, True), mock_chain(2, False)]
        result = await byzantine_consensus(chains, threshold=0.67)
        print(f"  Consensus: {result.consensus_reached}")
        print(f"  Agreement: {result.agreement_ratio:.0%}")
        print(f"  Responding: {result.responding_agents}/{result.total_agents}")

        # Test 3: No consensus (half disagree)
        print("\nTest 3: No consensus (half disagree)")
        chains = [mock_chain(i, i < 2) for i in range(4)]
        result = await byzantine_consensus(chains, threshold=0.67)
        print(f"  Consensus: {result.consensus_reached}")
        print(f"  Agreement: {result.agreement_ratio:.0%}")

        print("\n" + "=" * 60)
        print("All tests complete")

    asyncio.run(test())
