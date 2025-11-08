import pytest
import subprocess
from unittest.mock import patch, MagicMock
from env_manager.environment import EnvironmentManager
from env_manager.utils import run_command


class TestPyenvIntegration:
    """Test Pyenv integration functionality."""

    def setup_method(self):
        """Set up test environment."""
        self.env_manager = EnvironmentManager()

    def test_pyenv_available(self):
        """Test if pyenv is available on the system."""
        returncode, stdout, stderr = run_command(["pyenv", "--version"])
        if returncode == 0:
            assert "pyenv" in stdout.lower()
        else:
            pytest.skip("pyenv not available on this system")

    def test_pyenv_versions_list(self):
        """Test listing available Python versions via pyenv."""
        returncode, stdout, stderr = run_command(["pyenv", "versions"])
        if returncode == 0:
            # Should have at least system Python
            assert len(stdout.strip()) > 0
        else:
            pytest.skip("pyenv not available or no versions installed")

    def test_pyenv_install_version(self):
        """Test installing a Python version via pyenv."""
        # This test is potentially destructive, so we'll mock it
        with patch("env_manager.utils.run_command") as mock_run:
            mock_run.return_value = (0, "3.9.0", "")
            result = self.env_manager._install_python_version("3.9.0")
            assert result is True
            mock_run.assert_called_with(["pyenv", "install", "3.9.0"])

    def test_pyenv_install_version_failure(self):
        """Test handling of pyenv install failure."""
        with patch("env_manager.utils.run_command") as mock_run:
            mock_run.return_value = (1, "", "Version not found")
            result = self.env_manager._install_python_version("nonexistent")
            assert result is False

    def test_create_environment_with_pyenv_version(self):
        """Test creating environment with specific pyenv version."""
        with patch("env_manager.utils.run_command") as mock_run, patch(
            "pathlib.Path.exists", return_value=False
        ), patch("pathlib.Path.mkdir"), patch(
            "env_manager.environment.EnvironmentManager._get_pyenv_python_path"
        ) as mock_get_path:
            mock_get_path.return_value = "/path/to/python3.9"
            mock_run.return_value = (0, "", "")

            result = self.env_manager.create_environment("test_env", "3.9.0")
            assert result is True

    def test_get_pyenv_python_path(self):
        """Test getting Python path from pyenv."""
        with patch("env_manager.utils.run_command") as mock_run:
            mock_run.return_value = (
                0,
                "/home/user/.pyenv/versions/3.9.0/bin/python",
                "",
            )
            path = self.env_manager._get_pyenv_python_path("3.9.0")
            assert path == "/home/user/.pyenv/versions/3.9.0/bin/python"

    def test_get_pyenv_python_path_not_found(self):
        """Test handling when pyenv version is not found."""
        with patch("env_manager.utils.run_command") as mock_run:
            mock_run.return_value = (1, "", "version `3.9.0` not installed")
            path = self.env_manager._get_pyenv_python_path("3.9.0")
            assert path is None

    def test_list_available_python_versions(self):
        """Test listing available Python versions."""
        with patch("env_manager.utils.run_command") as mock_run:
            mock_run.return_value = (
                0,
                "  system\n  3.8.0\n* 3.9.0 (set by PYENV_VERSION)\n  3.10.0",
                "",
            )
            versions = self.env_manager._list_pyenv_versions()
            expected = ["system", "3.8.0", "3.9.0", "3.10.0"]
            assert versions == expected

    def test_environment_creation_with_pyenv_integration(self):
        """Integration test for environment creation with pyenv."""
        with patch("env_manager.utils.run_command") as mock_run, patch(
            "pathlib.Path.exists", return_value=False
        ), patch("pathlib.Path.mkdir"), patch(
            "env_manager.environment.EnvironmentManager._get_pyenv_python_path"
        ) as mock_get_path, patch(
            "env_manager.environment.EnvironmentManager._ensure_pyenv_version"
        ) as mock_ensure:
            mock_get_path.return_value = "/path/to/python3.9"
            mock_ensure.return_value = True
            mock_run.return_value = (0, "", "")

            # Test successful creation
            result = self.env_manager.create_environment("integration_test", "3.9.0")
            assert result is True

            # Verify pyenv version was ensured
            mock_ensure.assert_called_with("3.9.0")

    def test_pyenv_fallback_to_system_python(self):
        """Test fallback to system Python when pyenv version not available."""
        with patch("env_manager.utils.run_command") as mock_run, patch(
            "pathlib.Path.exists", return_value=False
        ), patch("pathlib.Path.mkdir"), patch(
            "env_manager.environment.EnvironmentManager._get_pyenv_python_path",
            return_value=None,
        ):
            # Mock successful venv creation with system python
            mock_run.return_value = (0, "", "")

            result = self.env_manager.create_environment("fallback_test", "3.9.0")
            # Should still work with system python fallback
            assert result is True

    def test_pyenv_version_validation(self):
        """Test validation of Python version strings."""
        valid_versions = ["3.8.0", "3.9.1", "3.10.0", "3.11.0"]
        invalid_versions = ["3", "3.8", "python3.8", "3.8.0-dev"]

        for version in valid_versions:
            assert self.env_manager._is_valid_python_version(version)

        for version in invalid_versions:
            assert not self.env_manager._is_valid_python_version(version)
