#!/usr/bin/env python3
"""
USF 6.0 OMEGA - ENGINE 11: Token Efficiency
Token Counter - Accurate token counting and budget management

This is REAL implementation, not a spec.
"""

from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

try:
    import tiktoken
    HAS_TIKTOKEN = True
except ImportError:
    HAS_TIKTOKEN = False


@dataclass
class TokenBudget:
    """Token budget tracking"""
    total: int
    used: int
    remaining: int
    items: int
    average_per_item: float


class TokenCounter:
    """
    ENGINE 11: Token Counter

    Provides accurate token counting using tiktoken (cl100k_base encoding).
    Manages token budgets for context loading.
    """

    # Model context limits
    MODEL_LIMITS = {
        'claude-3-opus': 200000,
        'claude-3-sonnet': 200000,
        'claude-3-haiku': 200000,
        'claude-3.5-sonnet': 200000,
        'gpt-4': 128000,
        'gpt-4-turbo': 128000,
        'gpt-3.5-turbo': 16000,
    }

    def __init__(self, model: str = 'claude-3.5-sonnet'):
        self.model = model
        self.tokenizer = None

        if HAS_TIKTOKEN:
            # Use cl100k_base (GPT-4/Claude compatible)
            self.tokenizer = tiktoken.get_encoding("cl100k_base")

        self.context_limit = self.MODEL_LIMITS.get(model, 200000)

    def count(self, text: str) -> int:
        """Count tokens in text"""
        if self.tokenizer:
            return len(self.tokenizer.encode(text))
        # Fallback estimate
        return len(text) // 4

    def count_file(self, path: str) -> int:
        """Count tokens in a file"""
        try:
            content = Path(path).read_text(encoding='utf-8')
            return self.count(content)
        except Exception:
            return 0

    def count_batch(self, texts: List[str]) -> List[int]:
        """Count tokens for multiple texts"""
        return [self.count(t) for t in texts]

    def estimate_cost(
        self,
        input_tokens: int,
        output_tokens: int = 0,
        model: Optional[str] = None
    ) -> float:
        """
        Estimate cost in USD.

        Prices as of late 2024 (approximate):
        - Claude 3.5 Sonnet: $3/1M input, $15/1M output
        - Claude 3 Opus: $15/1M input, $75/1M output
        - GPT-4 Turbo: $10/1M input, $30/1M output
        """
        model = model or self.model

        prices = {
            'claude-3.5-sonnet': (3.0, 15.0),
            'claude-3-opus': (15.0, 75.0),
            'claude-3-sonnet': (3.0, 15.0),
            'claude-3-haiku': (0.25, 1.25),
            'gpt-4-turbo': (10.0, 30.0),
            'gpt-4': (30.0, 60.0),
            'gpt-3.5-turbo': (0.5, 1.5),
        }

        input_price, output_price = prices.get(model, (3.0, 15.0))

        input_cost = (input_tokens / 1_000_000) * input_price
        output_cost = (output_tokens / 1_000_000) * output_price

        return input_cost + output_cost

    def truncate_to_tokens(self, text: str, max_tokens: int) -> str:
        """Truncate text to fit within token limit"""
        if self.tokenizer:
            tokens = self.tokenizer.encode(text)
            if len(tokens) <= max_tokens:
                return text
            return self.tokenizer.decode(tokens[:max_tokens])
        else:
            # Fallback: estimate 4 chars per token
            max_chars = max_tokens * 4
            if len(text) <= max_chars:
                return text
            return text[:max_chars]

    def split_to_chunks(
        self,
        text: str,
        chunk_tokens: int,
        overlap_tokens: int = 50
    ) -> List[str]:
        """Split text into token-sized chunks with overlap"""
        if self.tokenizer:
            tokens = self.tokenizer.encode(text)
            chunks = []

            start = 0
            while start < len(tokens):
                end = min(start + chunk_tokens, len(tokens))
                chunk_tokens_slice = tokens[start:end]
                chunks.append(self.tokenizer.decode(chunk_tokens_slice))
                start = end - overlap_tokens
                if start >= len(tokens) - overlap_tokens:
                    break

            return chunks
        else:
            # Fallback
            chunk_chars = chunk_tokens * 4
            overlap_chars = overlap_tokens * 4
            chunks = []

            start = 0
            while start < len(text):
                end = min(start + chunk_chars, len(text))
                chunks.append(text[start:end])
                start = end - overlap_chars
                if start >= len(text) - overlap_chars:
                    break

            return chunks

    def create_budget(self, total_tokens: int) -> TokenBudget:
        """Create a token budget tracker"""
        return TokenBudget(
            total=total_tokens,
            used=0,
            remaining=total_tokens,
            items=0,
            average_per_item=0.0
        )

    def use_budget(
        self,
        budget: TokenBudget,
        tokens: int,
        items: int = 1
    ) -> TokenBudget:
        """Update budget after using tokens"""
        new_used = budget.used + tokens
        new_items = budget.items + items
        new_remaining = budget.total - new_used

        return TokenBudget(
            total=budget.total,
            used=new_used,
            remaining=max(0, new_remaining),
            items=new_items,
            average_per_item=new_used / new_items if new_items > 0 else 0
        )

    def fits_budget(self, budget: TokenBudget, tokens: int) -> bool:
        """Check if tokens fit within remaining budget"""
        return tokens <= budget.remaining

    def analyze_directory(self, path: str) -> Dict:
        """Analyze token usage for a directory of files"""
        dir_path = Path(path)
        results = {
            'total_tokens': 0,
            'total_files': 0,
            'files': [],
            'by_extension': {}
        }

        for file_path in dir_path.rglob('*'):
            if file_path.is_file() and file_path.suffix in ['.md', '.txt', '.py', '.js', '.ts']:
                try:
                    tokens = self.count_file(str(file_path))
                    ext = file_path.suffix

                    results['total_tokens'] += tokens
                    results['total_files'] += 1
                    results['files'].append({
                        'path': str(file_path.relative_to(dir_path)),
                        'tokens': tokens
                    })

                    if ext not in results['by_extension']:
                        results['by_extension'][ext] = {'count': 0, 'tokens': 0}
                    results['by_extension'][ext]['count'] += 1
                    results['by_extension'][ext]['tokens'] += tokens

                except Exception:
                    pass

        # Sort files by token count
        results['files'].sort(key=lambda x: x['tokens'], reverse=True)

        return results


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description='USF 6.0 ENGINE 11 - Token Counter'
    )
    parser.add_argument(
        'input',
        nargs='?',
        help='Text or file path to count'
    )
    parser.add_argument(
        '--file',
        action='store_true',
        help='Treat input as file path'
    )
    parser.add_argument(
        '--dir',
        metavar='PATH',
        help='Analyze directory'
    )
    parser.add_argument(
        '--cost',
        type=int,
        metavar='TOKENS',
        help='Estimate cost for token count'
    )
    parser.add_argument(
        '--model',
        default='claude-3.5-sonnet',
        help='Model for cost estimation'
    )

    args = parser.parse_args()

    counter = TokenCounter(model=args.model)

    if args.input:
        if args.file:
            tokens = counter.count_file(args.input)
            print(f"File: {args.input}")
        else:
            tokens = counter.count(args.input)
            print(f"Text length: {len(args.input)} chars")

        print(f"Tokens: {tokens:,}")
        cost = counter.estimate_cost(tokens)
        print(f"Est. input cost: ${cost:.4f}")

    if args.dir:
        analysis = counter.analyze_directory(args.dir)
        print(f"\nDirectory Analysis: {args.dir}")
        print(f"  Total files: {analysis['total_files']}")
        print(f"  Total tokens: {analysis['total_tokens']:,}")
        print(f"  Est. cost: ${counter.estimate_cost(analysis['total_tokens']):.2f}")

        print("\n  By extension:")
        for ext, stats in sorted(analysis['by_extension'].items()):
            print(f"    {ext}: {stats['count']} files, {stats['tokens']:,} tokens")

        print("\n  Top 10 files by tokens:")
        for f in analysis['files'][:10]:
            print(f"    {f['tokens']:>8,} - {f['path']}")

    if args.cost:
        input_cost = counter.estimate_cost(args.cost, 0, args.model)
        output_cost = counter.estimate_cost(0, args.cost, args.model)
        print(f"\nCost estimate for {args.cost:,} tokens ({args.model}):")
        print(f"  As input: ${input_cost:.4f}")
        print(f"  As output: ${output_cost:.4f}")


if __name__ == '__main__':
    main()
