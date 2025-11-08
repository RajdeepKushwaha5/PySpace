import subprocess
from pathlib import Path
from .utils import logger


class CacheManager:
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def download_wheel(self, package: str):
        """Download package wheel to cache."""
        cmd = ["pip", "download", "--dest", str(self.cache_dir), package]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"Downloaded {package} to cache")
            return True
        else:
            logger.error(f"Failed to download {package}: {result.stderr}")
            return False

    def clean_cache(self):
        """Remove all cached packages."""
        for file in self.cache_dir.iterdir():
            if file.is_file():
                file.unlink()
        logger.info("Cache cleaned")

    def get_cache_path(self):
        return self.cache_dir
