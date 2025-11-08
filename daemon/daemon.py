import time
import threading
from pathlib import Path
from typing import Dict
from loguru import logger
from env_manager.environment import EnvironmentManager
from env_manager.cache import CacheManager
from env_manager.config import ConfigManager
from daemon.watcher import FileWatcher


class PySpaceDaemon:
    def __init__(self):
        self.env_manager = EnvironmentManager()
        self.cache_manager = CacheManager()
        self.config_manager = ConfigManager()
        self.running = False
        self.watcher_thread = None
        self.watcher = None
        self.pyspace_json_path = Path.cwd() / "pyspace.json"

    def start(self):
        """Start the daemon."""
        logger.info("Starting PySpace daemon")
        self.running = True

        # Start file watcher in a separate thread
        self.watcher_thread = threading.Thread(
            target=self._start_file_watcher, daemon=True
        )
        self.watcher_thread.start()

        logger.success("PySpace daemon started")
        try:
            while self.running:
                self._check_auto_sync()
                time.sleep(5)  # Check every 5 seconds
        except KeyboardInterrupt:
            logger.info("Daemon interrupted by user")
        except Exception as e:
            logger.error(f"Daemon error: {e}")
        finally:
            self.stop()

    def stop(self):
        """Stop the daemon."""
        logger.info("Stopping PySpace daemon")
        self.running = False
        if self.watcher_thread and self.watcher_thread.is_alive():
            # Stop the file watcher gracefully
            try:
                if self.watcher:
                    self.watcher.stop_watching()
                    # Join the thread to allow a clean shutdown
                    self.watcher_thread.join(timeout=2)
            except Exception as e:
                logger.warning(f"Error stopping watcher thread: {e}")
        logger.success("PySpace daemon stopped")

    def _start_file_watcher(self):
        """Start watching pyspace.json for changes."""
        # Keep a reference so we can stop it later
        self.watcher = FileWatcher(
            self.pyspace_json_path, self._on_pyspace_json_changed
        )
        self.watcher.start_watching()

    def _on_pyspace_json_changed(self):
        """Callback when pyspace.json changes."""
        logger.info("pyspace.json has changed, triggering auto-sync")
        self._check_auto_sync()

    def _check_auto_sync(self):
        """Check for pyspace.json changes and sync."""
        if not self.config_manager.get("auto_sync", True):
            return

        try:
            local_config = self.config_manager.get_local_config()
            env_name = local_config.get("environment")
            if env_name:
                if not self.env_manager.is_active(env_name):
                    logger.info(f"Auto-activating environment '{env_name}'")
                    # In a real implementation, this would activate the environment
                    # For now, just log the intent
                else:
                    logger.debug(f"Environment '{env_name}' is already active")
        except Exception as e:
            logger.error(f"Error during auto-sync check: {e}")

    def get_status(self) -> Dict:
        """Get daemon status."""
        return {
            "running": self.running,
            "environments": len(self.env_manager.list_environments()),
            "cache_info": self.cache_manager.get_cache_info(),
        }
