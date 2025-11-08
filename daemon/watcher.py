import time
from pathlib import Path
from typing import Callable
from loguru import logger


class FileWatcher:
    def __init__(self, file_path: Path, callback: Callable):
        self.file_path = file_path
        self.callback = callback
        self.last_modified = None
        self.watching = False

    def start_watching(self):
        """Start watching for file changes."""
        logger.info(f"Starting to watch file: {self.file_path}")
        self.watching = True
        try:
            while self.watching:
                self.watch()
                time.sleep(1)  # Check every second
        except Exception as e:
            logger.error(f"Error while watching file: {e}")

    def stop_watching(self):
        """Stop watching for file changes."""
        logger.info("Stopping file watcher")
        self.watching = False

    def set_callback(self, callback: Callable):
        """Update the callback invoked when the watched file changes."""
        logger.debug("Updating file watcher callback")
        self.callback = callback

    def watch(self):
        """Watch for file changes."""
        try:
            if not self.file_path.exists():
                return

            current_modified = self.file_path.stat().st_mtime
            if self.last_modified is None:
                self.last_modified = current_modified
                logger.debug(f"Initial file modification time: {current_modified}")
            elif current_modified > self.last_modified:
                logger.info(f"File {self.file_path} has been modified")
                self.last_modified = current_modified
                # Callbacks may accept different signatures in tests (file_path, action)
                try:
                    self.callback(self.file_path, "modified")
                except TypeError:
                    # Fallback to no-arg callback for backwards compatibility
                    self.callback()
        except Exception as e:
            logger.error(f"Error checking file modification: {e}")

    def set_callback(self, callback):
        """Set or replace the callback used when a file changes."""
        self.callback = callback

    def _on_file_change(self, instance, file_path, action):
        """Helper used by tests to simulate an on-change event."""
        try:
            # Ensure callback receives consistent parameters
            try:
                self.callback(file_path, action)
            except TypeError:
                self.callback()
        except Exception as e:
            logger.error(f"Error in _on_file_change callback: {e}")
