"""Cache manager for security reminders."""

import json
import os
from pathlib import Path
from typing import Optional

class SecurityReminderCache:
    """Manages caching of security reminders to avoid redundant LLM calls."""
    
    def __init__(self, cache_dir: str = ".corridor_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_file = self.cache_dir / "security_reminders.json"
        self._cache = self._load_cache()
    
    def _load_cache(self) -> dict:
        """Load cache from disk."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_cache(self) -> None:
        """Save cache to disk."""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self._cache, f, indent=2)
        except IOError:
            pass  # Fail silently if can't save cache
    
    def get(self, key: str) -> Optional[str]:
        """Get cached reminder by key."""
        return self._cache.get(key)
    
    def set(self, key: str, value: str) -> None:
        """Set cached reminder."""
        self._cache[key] = value
        self._save_cache()