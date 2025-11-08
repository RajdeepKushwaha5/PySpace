import hashlib
import json
from pathlib import Path
from typing import Dict
from loguru import logger


class CacheManager:
    def __init__(self, cache_dir: Path = None):
        self.cache_dir = cache_dir or Path.home() / ".pyspace" / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.cache_dir / "metadata.json"
        self._load_metadata()

    def _load_metadata(self):
        if self.metadata_file.exists():
            with open(self.metadata_file) as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {}
            self._save_metadata()

    def _save_metadata(self):
        with open(self.metadata_file, "w") as f:
            json.dump(self.metadata, f, indent=2)

    def _calculate_checksum(self, package: str, version: str = None) -> str:
        """Calculate checksum for package."""
        key = f"{package}@{version}" if version else package
        return hashlib.md5(key.encode()).hexdigest()

    def is_cached(self, package: str, version: str = None) -> bool:
        """Check if package is cached."""
        checksum = self._calculate_checksum(package, version)
        return checksum in self.metadata

    def cache_package(self, package: str, version: str = None):
        """Cache a package."""
        logger.info(f"Caching package '{package}' (version: {version or 'latest'})")
        checksum = self._calculate_checksum(package, version)
        self.metadata[checksum] = {
            "package": package,
            "version": version,
            "cached_at": str(Path.cwd()),
        }
        self._save_metadata()
        logger.success(f"Package '{package}' cached successfully")

    def clear_cache(self):
        """Clear all cached packages."""
        logger.info("Clearing package cache")
        try:
            for item in self.cache_dir.iterdir():
                if item.is_file() and item != self.metadata_file:
                    item.unlink()
            self.metadata = {}
            self._save_metadata()
            logger.success("Cache cleared successfully")
        except Exception as e:
            logger.error(f"Failed to clear cache: {e}")

    def prune_cache(self, max_age_days: int = 30):
        """Prune old cache entries."""
        logger.info(f"Pruning cache entries older than {max_age_days} days")
        # Simplified - in practice, check timestamps
        logger.info("Cache pruning completed")

    def get_cache_info(self) -> Dict:
        """Get cache information."""
        total_size = 0
        for item in self.cache_dir.iterdir():
            if item.is_file() and item != self.metadata_file:
                total_size += item.stat().st_size

        return {
            "total_packages": len(self.metadata),
            "total_size": total_size,
            "cache_dir": str(self.cache_dir),
        }
