import pytest
import threading
from unittest.mock import patch, MagicMock, Mock
from pathlib import Path
from daemon.daemon import PySpaceDaemon
from daemon.watcher import FileWatcher


# Add timeout decorator for tests
pytestmark = pytest.mark.timeout(10)


class TestDaemonAutoSync:
    """Test daemon auto-sync functionality."""

    def setup_method(self):
        """Set up test environment."""
        self.daemon = PySpaceDaemon()

    def test_daemon_initialization(self):
        """Test daemon initialization."""
        assert self.daemon.watcher is None
        assert not self.daemon.running

    @patch("daemon.daemon.PySpaceDaemon._start_file_watcher")
    @patch("time.sleep")  # Mock sleep to speed up test
    def test_daemon_start_stop(self, mock_sleep, mock_watcher):
        """Test daemon start and stop functionality."""

        # Start daemon in a thread with timeout
        def run_daemon():
            self.daemon.running = True
            # Simulate one loop iteration
            self.daemon._check_auto_sync()
            self.daemon.running = False

        thread = threading.Thread(target=run_daemon, daemon=True)
        thread.start()
        thread.join(timeout=2)

        # Stop daemon
        self.daemon.stop()
        assert not self.daemon.running

    def test_daemon_status(self):
        """Test daemon status reporting."""
        status = self.daemon.get_status()
        assert isinstance(status, dict)
        assert "running" in status
        assert status["running"] is False

    @patch("env_manager.config.ConfigManager.get_local_config")
    def test_auto_sync_check(self, mock_config):
        """Test auto-sync check functionality."""
        mock_config.return_value = {"environment": "test_env"}

        # Should not raise exception
        self.daemon._check_auto_sync()

    @patch("env_manager.config.ConfigManager.get_local_config")
    @patch("env_manager.environment.EnvironmentManager.is_active")
    def test_sync_with_config(self, mock_is_active, mock_get_config):
        """Test environment synchronization with config."""
        mock_get_config.return_value = {"environment": "test_env"}
        mock_is_active.return_value = False

        self.daemon._check_auto_sync()

        # Verify config was checked
        mock_get_config.assert_called()

    @patch("daemon.watcher.FileWatcher.start_watching")
    def test_file_watcher_integration(self, mock_start):
        """Test file watcher integration with daemon."""
        # Start file watcher in separate thread
        self.daemon._start_file_watcher()

        # Verify watcher was created
        assert self.daemon.watcher is not None


class TestFileWatcher:
    """Test file watcher functionality."""

    def setup_method(self):
        """Set up test environment."""
        self.test_file = Path("test_pyspace.json")
        self.callback = Mock()
        self.watcher = FileWatcher(self.test_file, self.callback)

    def test_watcher_initialization(self):
        """Test watcher initialization."""
        assert self.watcher.file_path == self.test_file
        assert self.watcher.callback == self.callback
        assert not self.watcher.watching

    @patch("time.sleep")  # Mock sleep to speed up test
    def test_watch_nonexistent_file(self, mock_sleep):
        """Test watching a file that doesn't exist."""
        # Should handle gracefully
        self.watcher.watch()
        # No callback should be triggered
        self.callback.assert_not_called()

    def test_stop_watching(self):
        """Test stopping file watcher."""
        self.watcher.watching = True
        self.watcher.stop_watching()
        assert not self.watcher.watching

    def test_watcher_with_custom_callback(self):
        """Test watcher with custom callback function."""
        callback_called = False

        def test_callback(file_path, action):
            nonlocal callback_called
            callback_called = True
            assert file_path == "test.json"
            assert action == "modified"

        self.watcher.set_callback(test_callback)
        self.watcher._on_file_change(None, "test.json", "modified")
        assert callback_called


class TestDaemonIntegration:
    """Integration tests for daemon functionality."""

    def test_daemon_full_lifecycle(self):
        """Test complete daemon lifecycle."""
        daemon = PySpaceDaemon()

        # Start daemon
        with patch("threading.Thread"), patch("daemon.watcher.FileWatcher"):
            daemon.start()
            assert daemon.running

        # Check status
        assert daemon.get_status() == "running"

        # Stop daemon
        daemon.stop()
        assert not daemon.running
        assert daemon.get_status() == "stopped"

    def test_daemon_auto_sync_on_file_change(self):
        """Test that daemon auto-syncs when pyspace.json changes."""
        daemon = PySpaceDaemon()

        with patch(
            "daemon.daemon.PySpaceDaemon._sync_environments"
        ) as mock_sync, patch("daemon.watcher.FileWatcher") as mock_watcher_class:
            mock_watcher = MagicMock()
            mock_watcher_class.return_value = mock_watcher

            # Start daemon
            daemon.start()

            # Simulate file change
            daemon.watcher._on_file_change(daemon, "pyspace.json", "modified")

            # Verify sync was called
            mock_sync.assert_called_once()

            # Stop daemon
            daemon.stop()

    def test_daemon_handles_watcher_errors(self):
        """Test daemon handles file watcher errors gracefully."""
        daemon = PySpaceDaemon()

        with patch("daemon.watcher.FileWatcher") as mock_watcher_class:
            mock_watcher = MagicMock()
            mock_watcher.start_watching.side_effect = Exception("Watcher error")
            mock_watcher_class.return_value = mock_watcher

            # Should not crash on watcher error
            daemon.start()
            assert daemon.running  # Daemon still runs even if watcher fails

            daemon.stop()
