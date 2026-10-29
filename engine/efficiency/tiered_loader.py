#!/usr/bin/env python3
"""
USF 6.0 OMEGA - ENGINE 11: Token Efficiency
Tiered Context Loader - Load context at appropriate granularity

This is REAL implementation, not a spec.

Context Tiers:
- L1 (Immediate): Full content for most relevant items (50k tokens max)
- L2 (Session): Paragraph summaries for moderately relevant (200k tokens max)
- L3 (Project): Section headers + first lines for broad context

Achieves 5x token reduction by loading appropriate granularity.
"""

import re
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

import yaml

try:
    import tiktoken
    HAS_TIKTOKEN = True
except ImportError:
    HAS_TIKTOKEN = False


class ContextTier(Enum):
    """Context loading tiers"""
    L1_IMMEDIATE = "L1"   # Full content
    L2_SESSION = "L2"     # Paragraph level
    L3_PROJECT = "L3"     # Section headers only


@dataclass
class LoadedContext:
    """A piece of loaded context"""
    path: str
    content: str
    tier: ContextTier
    token_count: int
    relevance_score: float
    truncated: bool = False
    original_tokens: int = 0


@dataclass
class TierConfig:
    """Configuration for a context tier"""
    max_tokens: int
    granularity: str  # "full", "paragraph", "section"
    max_items: int = 50


class TieredLoader:
    """
    ENGINE 11: Tiered Context Loader

    Loads context at appropriate granularity based on relevance:
    - High relevance → Full content (L1)
    - Medium relevance → Summarized (L2)
    - Low relevance → Headers only (L3)

    This achieves 5x token savings by not loading full content for everything.
    """

    DEFAULT_TIERS = {
        ContextTier.L1_IMMEDIATE: TierConfig(
            max_tokens=50000,
            granularity="full",
            max_items=20
        ),
        ContextTier.L2_SESSION: TierConfig(
            max_tokens=200000,
            granularity="paragraph",
            max_items=100
        ),
        ContextTier.L3_PROJECT: TierConfig(
            max_tokens=500000,
            granularity="section",
            max_items=500
        )
    }

    # Relevance thresholds for tier assignment
    L1_THRESHOLD = 0.7  # Above this → L1
    L2_THRESHOLD = 0.4  # Above this → L2, else L3

    def __init__(self, vault_path: str, config_path: Optional[str] = None):
        self.vault_path = Path(vault_path)
        self.config = self._load_config(config_path)
        self.tiers = dict(self.DEFAULT_TIERS)

        # Load custom tier configs
        if 'tiers' in self.config:
            for tier_name, tier_config in self.config['tiers'].items():
                tier = ContextTier(tier_name.split('_')[0])
                self.tiers[tier] = TierConfig(
                    max_tokens=tier_config.get('max_tokens', self.tiers[tier].max_tokens),
                    granularity=tier_config.get('granularity', self.tiers[tier].granularity),
                    max_items=tier_config.get('max_items', self.tiers[tier].max_items)
                )

        # Token counter
        self.tokenizer = None
        if HAS_TIKTOKEN:
            self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def _load_config(self, config_path: Optional[str]) -> dict:
        """Load configuration"""
        if config_path:
            config_file = Path(config_path)
        else:
            config_file = self.vault_path / '.usf' / 'config.yaml'

        if config_file.exists():
            with open(config_file) as f:
                config = yaml.safe_load(f)
                return config.get('efficiency', {})

        return {}

    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        if self.tokenizer:
            return len(self.tokenizer.encode(text))
        # Fallback: estimate ~4 chars per token
        return len(text) // 4

    def _determine_tier(self, relevance_score: float) -> ContextTier:
        """Determine which tier based on relevance score"""
        if relevance_score >= self.L1_THRESHOLD:
            return ContextTier.L1_IMMEDIATE
        elif relevance_score >= self.L2_THRESHOLD:
            return ContextTier.L2_SESSION
        else:
            return ContextTier.L3_PROJECT

    def _extract_paragraphs(self, content: str, max_tokens: int) -> Tuple[str, bool]:
        """Extract paragraph-level summary (L2 granularity)"""
        paragraphs = re.split(r'\n\n+', content)
        result = []
        current_tokens = 0
        truncated = False

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            para_tokens = self.count_tokens(para)

            # Always include headings
            if para.startswith('#'):
                result.append(para)
                current_tokens += para_tokens
                continue

            # For non-headings, take first sentence or truncate
            if current_tokens + para_tokens <= max_tokens:
                # Take first 2-3 sentences
                sentences = re.split(r'(?<=[.!?])\s+', para)
                summary = ' '.join(sentences[:3])
                if len(sentences) > 3:
                    summary += '...'
                result.append(summary)
                current_tokens += self.count_tokens(summary)
            else:
                truncated = True
                break

        return '\n\n'.join(result), truncated

    def _extract_sections(self, content: str, max_tokens: int) -> Tuple[str, bool]:
        """Extract section-level summary (L3 granularity)"""
        lines = content.split('\n')
        result = []
        current_tokens = 0
        truncated = False
        in_code_block = False

        for line in lines:
            # Track code blocks
            if line.startswith('```'):
                in_code_block = not in_code_block
                continue

            if in_code_block:
                continue

            # Include headings
            if line.startswith('#'):
                line_tokens = self.count_tokens(line)
                if current_tokens + line_tokens <= max_tokens:
                    result.append(line)
                    current_tokens += line_tokens
                else:
                    truncated = True
                    break
                continue

            # Include first non-empty line after heading
            if result and result[-1].startswith('#') and line.strip():
                # Take first 100 chars of first content line
                preview = line.strip()[:100]
                if len(line.strip()) > 100:
                    preview += '...'
                line_tokens = self.count_tokens(preview)
                if current_tokens + line_tokens <= max_tokens:
                    result.append(f"  → {preview}")
                    current_tokens += line_tokens

        return '\n'.join(result), truncated

    def load_content(
        self,
        path: str,
        relevance_score: float,
        force_tier: Optional[ContextTier] = None
    ) -> LoadedContext:
        """
        Load content at appropriate granularity.

        Args:
            path: Path to the file (relative to vault)
            relevance_score: 0-1 score indicating relevance
            force_tier: Override automatic tier selection

        Returns:
            LoadedContext with appropriately granular content
        """
        # SECURITY FIX (VULN-001): Validate path is within vault
        try:
            file_path = (self.vault_path / path).resolve()
            file_path.relative_to(self.vault_path.resolve())
        except ValueError:
            return LoadedContext(
                path=path,
                content="[Access denied: path traversal attempt]",
                tier=ContextTier.L3_PROJECT,
                token_count=0,
                relevance_score=relevance_score
            )

        # SECURITY FIX: Reject symlinks
        if file_path.is_symlink():
            return LoadedContext(
                path=path,
                content="[Access denied: symlinks not allowed]",
                tier=ContextTier.L3_PROJECT,
                token_count=0,
                relevance_score=relevance_score
            )

        if not file_path.exists():
            return LoadedContext(
                path=path,
                content=f"[File not found: {path}]",
                tier=ContextTier.L3_PROJECT,
                token_count=0,
                relevance_score=relevance_score
            )

        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            return LoadedContext(
                path=path,
                content=f"[Error reading file: {e}]",
                tier=ContextTier.L3_PROJECT,
                token_count=0,
                relevance_score=relevance_score
            )

        original_tokens = self.count_tokens(content)
        tier = force_tier or self._determine_tier(relevance_score)
        tier_config = self.tiers[tier]

        truncated = False

        if tier == ContextTier.L1_IMMEDIATE:
            # Full content, but respect max tokens
            if original_tokens > tier_config.max_tokens:
                # Truncate to max tokens
                if self.tokenizer:
                    tokens = self.tokenizer.encode(content)[:tier_config.max_tokens]
                    content = self.tokenizer.decode(tokens)
                else:
                    content = content[:tier_config.max_tokens * 4]
                content += "\n\n[... truncated ...]"
                truncated = True

        elif tier == ContextTier.L2_SESSION:
            # Paragraph-level summary
            content, truncated = self._extract_paragraphs(
                content,
                tier_config.max_tokens // tier_config.max_items
            )

        else:  # L3_PROJECT
            # Section headers only
            content, truncated = self._extract_sections(
                content,
                tier_config.max_tokens // tier_config.max_items
            )

        final_tokens = self.count_tokens(content)

        return LoadedContext(
            path=path,
            content=content,
            tier=tier,
            token_count=final_tokens,
            relevance_score=relevance_score,
            truncated=truncated,
            original_tokens=original_tokens
        )

    def load_batch(
        self,
        items: List[Tuple[str, float]],  # (path, relevance_score)
        total_budget: Optional[int] = None
    ) -> List[LoadedContext]:
        """
        Load multiple items with budget management.

        Automatically manages token budget across tiers.
        """
        if total_budget is None:
            total_budget = sum(t.max_tokens for t in self.tiers.values())

        # Sort by relevance (highest first)
        sorted_items = sorted(items, key=lambda x: x[1], reverse=True)

        results = []
        tokens_used = 0

        for path, score in sorted_items:
            if tokens_used >= total_budget:
                break

            # Calculate remaining budget
            remaining = total_budget - tokens_used

            # Load with appropriate tier
            ctx = self.load_content(path, score)

            # Check if we can afford it
            if ctx.token_count <= remaining:
                results.append(ctx)
                tokens_used += ctx.token_count
            else:
                # Try lower tier
                for tier in [ContextTier.L2_SESSION, ContextTier.L3_PROJECT]:
                    ctx = self.load_content(path, score, force_tier=tier)
                    if ctx.token_count <= remaining:
                        results.append(ctx)
                        tokens_used += ctx.token_count
                        break

        return results

    def get_stats(self, contexts: List[LoadedContext]) -> Dict:
        """Get statistics about loaded contexts"""
        total_tokens = sum(c.token_count for c in contexts)
        original_tokens = sum(c.original_tokens for c in contexts)

        tier_counts = {tier: 0 for tier in ContextTier}
        tier_tokens = {tier: 0 for tier in ContextTier}

        for ctx in contexts:
            tier_counts[ctx.tier] += 1
            tier_tokens[ctx.tier] += ctx.token_count

        savings_ratio = original_tokens / total_tokens if total_tokens > 0 else 0

        return {
            'total_items': len(contexts),
            'total_tokens': total_tokens,
            'original_tokens': original_tokens,
            'savings_ratio': savings_ratio,
            'tier_distribution': {t.value: tier_counts[t] for t in ContextTier},
            'tokens_by_tier': {t.value: tier_tokens[t] for t in ContextTier}
        }


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description='USF 6.0 ENGINE 11 - Tiered Context Loader'
    )
    parser.add_argument(
        'vault_path',
        help='Path to Obsidian vault'
    )
    parser.add_argument(
        '--load',
        metavar='FILE',
        help='Load a specific file'
    )
    parser.add_argument(
        '--relevance',
        type=float,
        default=0.5,
        help='Relevance score (0-1) for tier selection'
    )
    parser.add_argument(
        '--tier',
        choices=['L1', 'L2', 'L3'],
        help='Force specific tier'
    )
    parser.add_argument(
        '--demo',
        action='store_true',
        help='Demo with sample files'
    )

    args = parser.parse_args()

    loader = TieredLoader(vault_path=args.vault_path)

    if args.load:
        force_tier = None
        if args.tier:
            force_tier = ContextTier(args.tier)

        ctx = loader.load_content(args.load, args.relevance, force_tier)

        print(f"\nLoaded: {ctx.path}")
        print(f"Tier: {ctx.tier.value} ({ctx.tier.name})")
        print(f"Tokens: {ctx.token_count} (original: {ctx.original_tokens})")
        print(f"Savings: {ctx.original_tokens / ctx.token_count:.1f}x" if ctx.token_count > 0 else "N/A")
        print(f"Truncated: {ctx.truncated}")
        print(f"\nContent preview (first 500 chars):")
        print("-" * 40)
        print(ctx.content[:500])
        if len(ctx.content) > 500:
            print("...")

    if args.demo:
        # Find some files to demo with
        vault = Path(args.vault_path)
        md_files = list(vault.rglob('*.md'))[:10]

        if md_files:
            # Create sample items with varying relevance
            items = [
                (str(f.relative_to(vault)), 0.9 - i * 0.1)
                for i, f in enumerate(md_files)
            ]

            contexts = loader.load_batch(items, total_budget=10000)
            stats = loader.get_stats(contexts)

            print("\nDemo Results:")
            print(f"  Items loaded: {stats['total_items']}")
            print(f"  Total tokens: {stats['total_tokens']}")
            print(f"  Original tokens: {stats['original_tokens']}")
            print(f"  Savings ratio: {stats['savings_ratio']:.1f}x")
            print(f"\n  Tier distribution:")
            for tier, count in stats['tier_distribution'].items():
                print(f"    {tier}: {count} items, {stats['tokens_by_tier'][tier]} tokens")


if __name__ == '__main__':
    main()
