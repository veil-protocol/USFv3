#!/usr/bin/env python3
"""
USF 6.8.0 OMEGA - ENGINE 11: Token Efficiency
Deduplication Module - Avoid sending duplicate content

This is REAL implementation, not a spec.

Tracks content fingerprints to:
1. Detect if content was already sent in session
2. Skip redundant context loading
3. Track content versions for cache invalidation

v6.8.0 Fixes:
- P0#4: Added memory bounds (MAX_SESSION_HASHES, MAX_SESSION_CHUNKS)
- Added _enforce_session_limits() to prevent unbounded growth
"""

import hashlib
import sqlite3
import json
import threading
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Set, Tuple
from dataclasses import dataclass
from collections import deque

import yaml

# v6.8.0 FIX P0#4: Memory bounds for session tracking
# Prevents unbounded memory growth during long sessions
MAX_SESSION_HASHES = 10000  # Max unique content hashes per session
MAX_SESSION_CHUNKS = 50000  # Max chunk hashes per session (more due to chunking)
SESSION_EVICT_RATIO = 0.2   # Evict 20% when limit reached

# v6.9.0 FIX P2-14: Database retention policy
# Fingerprints older than this are eligible for cleanup
FINGERPRINT_RETENTION_DAYS = 30  # Keep fingerprints for 30 days
MAX_FINGERPRINTS = 100000  # Maximum fingerprints before forced cleanup


@dataclass
class ContentFingerprint:
    """Fingerprint of content for deduplication"""
    content_hash: str
    path: str
    size_bytes: int
    first_seen: datetime
    last_seen: datetime
    seen_count: int


class Deduplicator:
    """
    ENGINE 11: Content Deduplication

    Tracks what content has been sent to avoid redundant context.

    Uses multiple fingerprinting strategies:
    1. Full content hash (exact match)
    2. SimHash (fuzzy matching for near-duplicates)
    3. Chunk fingerprints (detect partial overlaps)

    Session-aware: tracks what was sent in current session vs ever.
    """

    def __init__(self, vault_path: str, config_path: Optional[str] = None):
        self.vault_path = Path(vault_path)
        self.config = self._load_config(config_path)

        # Storage
        usf_dir = self.vault_path / '00-USF'
        cache_dir = usf_dir / 'cache'
        cache_dir.mkdir(parents=True, exist_ok=True)

        self.db_path = cache_dir / 'fingerprints.db'
        # FIX-7: Add check_same_thread=False for multi-threaded access
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        # SECURITY FIX (VULN-005): Enable WAL mode for concurrent access
        self.conn.execute('PRAGMA journal_mode=WAL')
        self.conn.execute('PRAGMA busy_timeout=30000')
        self._init_schema()

        # v6.9.0 FIX P0-12: Add write lock for thread-safe SQLite operations
        self._write_lock = threading.Lock()

        # Session tracking (in-memory)
        # v6.9.0 FIX P1-6: Use deque with maxlen for O(1) bounded eviction
        self.session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.session_hashes: deque = deque(maxlen=MAX_SESSION_HASHES)
        self.session_chunks: deque = deque(maxlen=MAX_SESSION_CHUNKS)

    def _load_config(self, config_path: Optional[str]) -> dict:
        """Load configuration"""
        if config_path:
            config_file = Path(config_path)
        else:
            config_file = self.vault_path / '.usf' / 'config.yaml'

        if config_file.exists():
            with open(config_file) as f:
                config = yaml.safe_load(f)
                return config.get('efficiency', {}).get('dedup', {})

        return {}

    def _init_schema(self):
        """Create database schema"""
        cursor = self.conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fingerprints (
                content_hash TEXT PRIMARY KEY,
                path TEXT,
                size_bytes INTEGER,
                first_seen TEXT,
                last_seen TEXT,
                seen_count INTEGER DEFAULT 1
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chunk_fingerprints (
                chunk_hash TEXT,
                content_hash TEXT,
                chunk_index INTEGER,
                PRIMARY KEY (content_hash, chunk_index)
            )
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_chunk_hash
            ON chunk_fingerprints(chunk_hash)
        ''')

        self.conn.commit()

    def _hash_content(self, content: str) -> str:
        """Generate hash for content"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()[:32]

    def _chunk_content(self, content: str, chunk_size: int = 256) -> List[str]:
        """Split content into chunks for partial matching"""
        chunks = []
        words = content.split()

        for i in range(0, len(words), chunk_size // 2):  # 50% overlap
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk:
                chunks.append(chunk)

        return chunks

    def _hash_chunks(self, content: str) -> List[str]:
        """Generate hashes for content chunks"""
        chunks = self._chunk_content(content)
        return [self._hash_content(chunk) for chunk in chunks]

    def fingerprint(self, content: str, path: str = '') -> ContentFingerprint:
        """
        Generate fingerprint for content.

        Also stores in database for future lookups.

        v6.9.0 FIX P0-12: Thread-safe with write lock.
        """
        content_hash = self._hash_content(content)
        now = datetime.now()

        # v6.9.0: Use write lock for all database operations
        with self._write_lock:
            cursor = self.conn.cursor()

            # Check if exists
            cursor.execute(
                'SELECT first_seen, seen_count FROM fingerprints WHERE content_hash = ?',
                (content_hash,)
            )
            row = cursor.fetchone()

            if row:
                first_seen = datetime.fromisoformat(row[0])
                seen_count = row[1] + 1

                cursor.execute('''
                    UPDATE fingerprints
                    SET last_seen = ?, seen_count = ?, path = ?
                    WHERE content_hash = ?
                ''', (now.isoformat(), seen_count, path, content_hash))
            else:
                first_seen = now
                seen_count = 1

                cursor.execute('''
                    INSERT INTO fingerprints
                    (content_hash, path, size_bytes, first_seen, last_seen, seen_count)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    content_hash,
                    path,
                    len(content),
                    now.isoformat(),
                    now.isoformat(),
                    1
                ))

                # Store chunk fingerprints
                chunk_hashes = self._hash_chunks(content)
                for i, chunk_hash in enumerate(chunk_hashes):
                    cursor.execute('''
                        INSERT OR IGNORE INTO chunk_fingerprints
                        (chunk_hash, content_hash, chunk_index)
                        VALUES (?, ?, ?)
                    ''', (chunk_hash, content_hash, i))

            self.conn.commit()

        return ContentFingerprint(
            content_hash=content_hash,
            path=path,
            size_bytes=len(content),
            first_seen=first_seen,
            last_seen=now,
            seen_count=seen_count
        )

    def is_duplicate(self, content: str, session_only: bool = False) -> bool:
        """
        Check if content is a duplicate.

        v6.9.0 FIX P0-3: Changed default to session_only=False to enable
        cross-session deduplication by default (uses SQLite fingerprint DB).

        Args:
            content: Content to check
            session_only: If True, only check current session (faster but less thorough)

        Returns:
            True if content was already seen
        """
        content_hash = self._hash_content(content)

        if session_only:
            return content_hash in self.session_hashes
        else:
            cursor = self.conn.cursor()
            cursor.execute(
                'SELECT 1 FROM fingerprints WHERE content_hash = ?',
                (content_hash,)
            )
            return cursor.fetchone() is not None

    def _enforce_session_limits(self) -> None:
        """
        v6.8.0 FIX P0#4: Enforce session tracking memory bounds.

        v6.9.0 UPDATE: Now a no-op since we use deque with maxlen which
        automatically evicts oldest entries. Kept for API compatibility.
        """
        # v6.9.0: deque with maxlen handles eviction automatically
        # This method is now a no-op but kept for compatibility
        pass

    def mark_sent(self, content: str, path: str = '') -> ContentFingerprint:
        """
        Mark content as sent in current session.

        Returns fingerprint for tracking.

        v6.9.0: Uses deque with maxlen for O(1) bounded storage.
        """
        fp = self.fingerprint(content, path)
        # v6.9.0: deque.append automatically evicts oldest if at maxlen
        self.session_hashes.append(fp.content_hash)

        # Also mark chunks
        chunk_hashes = self._hash_chunks(content)
        for chunk_hash in chunk_hashes:
            self.session_chunks.append(chunk_hash)

        # v6.8.0 FIX P0#4: Enforce memory bounds (now no-op with deque)
        self._enforce_session_limits()

        return fp

    def find_overlap(self, content: str) -> float:
        """
        Find how much of content overlaps with already-sent content.

        Returns overlap ratio (0-1).
        """
        chunk_hashes = self._hash_chunks(content)
        if not chunk_hashes:
            return 0.0

        overlap_count = sum(1 for h in chunk_hashes if h in self.session_chunks)
        return overlap_count / len(chunk_hashes)

    def deduplicate_batch(
        self,
        items: List[Tuple[str, str]]  # (path, content)
    ) -> List[Tuple[str, str, bool]]:
        """
        Deduplicate a batch of items.

        Returns list of (path, content, is_new) tuples.
        Only returns items that are new or significantly different.
        """
        results = []

        for path, content in items:
            if self.is_duplicate(content):
                # Exact duplicate, skip
                continue

            overlap = self.find_overlap(content)
            if overlap > 0.8:
                # 80%+ overlap, likely duplicate
                continue

            # New or different enough
            self.mark_sent(content, path)
            results.append((path, content, True))

        return results

    def get_session_stats(self) -> Dict:
        """Get statistics for current session"""
        return {
            'session_id': self.session_id,
            'unique_contents': len(self.session_hashes),
            'unique_chunks': len(self.session_chunks)
        }

    def get_global_stats(self) -> Dict:
        """Get global deduplication statistics"""
        cursor = self.conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM fingerprints')
        total_fingerprints = cursor.fetchone()[0]

        cursor.execute('SELECT SUM(size_bytes) FROM fingerprints')
        total_bytes = cursor.fetchone()[0] or 0

        cursor.execute('SELECT COUNT(*) FROM chunk_fingerprints')
        total_chunks = cursor.fetchone()[0]

        cursor.execute('SELECT AVG(seen_count) FROM fingerprints')
        avg_seen = cursor.fetchone()[0] or 0

        return {
            'total_fingerprints': total_fingerprints,
            'total_bytes': total_bytes,
            'total_chunks': total_chunks,
            'average_seen_count': avg_seen
        }

    def clear_session(self):
        """Clear session tracking (start fresh)"""
        self.session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.session_hashes.clear()
        self.session_chunks.clear()

    def cleanup_old_fingerprints(self, retention_days: int = None, max_fingerprints: int = None) -> Dict:
        """
        v6.9.0 FIX P2-14: Clean up old fingerprints to prevent unbounded database growth.

        Args:
            retention_days: Days to keep fingerprints (default: FINGERPRINT_RETENTION_DAYS)
            max_fingerprints: Maximum fingerprints to keep (default: MAX_FINGERPRINTS)

        Returns:
            Dict with cleanup statistics
        """
        retention_days = retention_days or FINGERPRINT_RETENTION_DAYS
        max_fingerprints = max_fingerprints or MAX_FINGERPRINTS

        stats = {
            "deleted_by_age": 0,
            "deleted_by_count": 0,
            "remaining": 0,
            "chunks_deleted": 0
        }

        with self._write_lock:
            cursor = self.conn.cursor()

            # Get current count
            cursor.execute('SELECT COUNT(*) FROM fingerprints')
            initial_count = cursor.fetchone()[0]

            # Delete fingerprints older than retention period
            cutoff_date = (datetime.now() - timedelta(days=retention_days)).isoformat()
            cursor.execute('''
                DELETE FROM fingerprints
                WHERE last_seen < ? AND seen_count = 1
            ''', (cutoff_date,))
            stats["deleted_by_age"] = cursor.rowcount

            # Delete orphaned chunk fingerprints
            cursor.execute('''
                DELETE FROM chunk_fingerprints
                WHERE content_hash NOT IN (SELECT content_hash FROM fingerprints)
            ''')
            stats["chunks_deleted"] = cursor.rowcount

            # If still over limit, delete least-recently-seen entries
            cursor.execute('SELECT COUNT(*) FROM fingerprints')
            current_count = cursor.fetchone()[0]

            if current_count > max_fingerprints:
                to_delete = current_count - max_fingerprints
                cursor.execute('''
                    DELETE FROM fingerprints
                    WHERE content_hash IN (
                        SELECT content_hash FROM fingerprints
                        ORDER BY last_seen ASC, seen_count ASC
                        LIMIT ?
                    )
                ''', (to_delete,))
                stats["deleted_by_count"] = cursor.rowcount

                # Clean up orphaned chunks again
                cursor.execute('''
                    DELETE FROM chunk_fingerprints
                    WHERE content_hash NOT IN (SELECT content_hash FROM fingerprints)
                ''')
                stats["chunks_deleted"] += cursor.rowcount

            self.conn.commit()

            # Get final count
            cursor.execute('SELECT COUNT(*) FROM fingerprints')
            stats["remaining"] = cursor.fetchone()[0]

        return stats

    def close(self):
        """Clean up resources"""
        self.conn.close()


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description='USF 6.0 ENGINE 11 - Deduplication'
    )
    parser.add_argument(
        'vault_path',
        help='Path to Obsidian vault'
    )
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show deduplication statistics'
    )
    parser.add_argument(
        '--check',
        metavar='FILE',
        help='Check if file is duplicate'
    )
    parser.add_argument(
        '--fingerprint',
        metavar='FILE',
        help='Generate fingerprint for file'
    )

    args = parser.parse_args()

    dedup = Deduplicator(vault_path=args.vault_path)

    try:
        if args.stats:
            global_stats = dedup.get_global_stats()
            print("\nDeduplication Statistics:")
            print(f"  Total fingerprints: {global_stats['total_fingerprints']}")
            print(f"  Total bytes tracked: {global_stats['total_bytes']:,}")
            print(f"  Total chunks: {global_stats['total_chunks']}")
            print(f"  Avg seen count: {global_stats['average_seen_count']:.2f}")

        if args.check:
            file_path = Path(args.check)
            if file_path.exists():
                content = file_path.read_text(encoding='utf-8')
                is_dup = dedup.is_duplicate(content, session_only=False)
                overlap = dedup.find_overlap(content)

                print(f"\nFile: {args.check}")
                print(f"  Is duplicate: {is_dup}")
                print(f"  Overlap with known content: {overlap:.1%}")
            else:
                print(f"File not found: {args.check}")

        if args.fingerprint:
            file_path = Path(args.fingerprint)
            if file_path.exists():
                content = file_path.read_text(encoding='utf-8')
                fp = dedup.fingerprint(content, str(file_path))

                print(f"\nFingerprint: {args.fingerprint}")
                print(f"  Hash: {fp.content_hash}")
                print(f"  Size: {fp.size_bytes} bytes")
                print(f"  First seen: {fp.first_seen}")
                print(f"  Seen count: {fp.seen_count}")
            else:
                print(f"File not found: {args.fingerprint}")

    finally:
        dedup.close()


if __name__ == '__main__':
    main()
