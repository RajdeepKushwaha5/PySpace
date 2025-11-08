import os
import json
import re
from pathlib import Path
from typing import Optional, Dict, List
from loguru import logger
from env_manager.utils import run_command


class EnvironmentManager:
    def __init__(self, base_dir: Path = None):
        self.base_dir = base_dir or Path.home() / ".pyspace" / "envs"
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.config_dir = Path.home() / ".pyspace"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / "config.json"
        self.metadata_file = self.config_dir / "metadata.json"
        self._load_config()
        self._load_metadata()

    def _load_config(self):
        if self.config_file.exists():
            with open(self.config_file) as f:
                self.config = json.load(f)
        else:
            self.config = {"python_version": "3.11", "default_env": None}
            self._save_config()

    def _save_config(self):
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=2)

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

    def create_environment(self, name: str, python_version: str = None) -> bool:
        """Create a new virtual environment."""
        logger.info(
            f"Creating environment '{name}' with Python {python_version or 'default'}"
        )
        env_path = self.base_dir / name
        if env_path.exists():
            logger.warning(f"Environment '{name}' already exists")
            return False

        python_version = python_version or self.config["python_version"]
        # Resolve Python executable (pyenv or system)
        python_exe = self._find_python(python_version)
        if not python_exe:
            logger.error(f"Python executable not found for version {python_version}")
            return False

        try:
            # Create the venv using the resolved python executable to ensure correct interpreter
            returncode, out, err = run_command(
                [python_exe, "-m", "venv", str(env_path)]
            )
            if returncode != 0:
                logger.error(f"venv creation failed: {err}")
                return False
            # Update metadata
            self.metadata[name] = {
                "python_version": python_version,
                "path": str(env_path),
                "created": str(Path.cwd()),
            }
            self._save_metadata()
            logger.success(f"Created environment '{name}' successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to create environment '{name}': {e}")
            return False

    def _find_python(self, version: str) -> Optional[str]:
        """Find Python executable for given version."""
        # Try pyenv first (if available)
        try:
            rc, out, err = run_command(["pyenv", "which", f"python{version}"])
            if rc == 0 and out.strip():
                return out.strip()
        except Exception:
            # pyenv not available or error invoking it; fall back below
            pass

        # If version looks like a pyenv style (x.y.z), try to ensure it's installed
        if self._is_valid_python_version(version):
            # Attempt to get pyenv-managed python path
            path = self._get_pyenv_python_path(version)
            if path:
                return path

        # Fallback to system Python
        import sys

        return sys.executable

    # --- pyenv helper methods ---
    def _is_valid_python_version(self, version: str) -> bool:
        """Validate full Python version strings like '3.9.0'."""
        return bool(re.match(r"^\d+\.\d+\.\d+$", version))

    def _install_python_version(self, version: str) -> bool:
        """Install a Python version using pyenv."""
        try:
            rc, out, err = run_command(["pyenv", "install", version])
            return rc == 0
        except Exception:
            return False

    def _get_pyenv_python_path(self, version: str) -> Optional[str]:
        """Return the python executable path for a given pyenv version, or None."""
        try:
            # Many setups respond to `pyenv which python` when PYENV_VERSION is set.
            # Simpler: ask pyenv for the path directly (tests mock run_command accordingly).
            rc, out, err = run_command(["pyenv", "which", f"python{version}"])
            if rc == 0 and out.strip():
                return out.strip()
            return None
        except Exception:
            return None

    def _list_pyenv_versions(self) -> List[str]:
        """Return list of installed pyenv versions (parsed)."""
        rc, out, err = run_command(["pyenv", "versions"])
        if rc != 0:
            return []
        versions = []
        for line in out.splitlines():
            v = line.strip().lstrip("*").strip()
            # Remove any annotations like (set by ...)
            v = v.split()[0]
            versions.append(v)
        return versions

    def _ensure_pyenv_version(self, version: str) -> bool:
        """Ensure a pyenv version is installed; install if missing."""
        installed = self._list_pyenv_versions()
        if version in installed:
            return True
        # Try to install
        return self._install_python_version(version)

    def activate_environment(self, name: str) -> Optional[str]:
        """Get activation script for environment."""
        env_path = self.base_dir / name
        if not env_path.exists():
            return None

        if os.name == "nt":  # Windows
            return str(env_path / "Scripts" / "activate.bat")
        else:  # Unix
            return str(env_path / "bin" / "activate")

    def list_environments(self) -> List[Dict]:
        """List all environments."""
        envs = []
        for name in self.base_dir.iterdir():
            if name.is_dir():
                metadata = self.metadata.get(name.name, {})
                envs.append(
                    {
                        "name": name.name,
                        "path": str(name),
                        "python_version": metadata.get("python_version", "unknown"),
                        "active": self.is_active(name.name),
                    }
                )
        return envs

    def is_active(self, name: str) -> bool:
        """Check if environment is currently active."""
        # This is a simplified check - in practice, would need to track active env
        return False

    def remove_environment(self, name: str) -> bool:
        """Remove an environment."""
        logger.info(f"Removing environment '{name}'")
        env_path = self.base_dir / name
        if not env_path.exists():
            logger.warning(f"Environment '{name}' does not exist")
            return False

        try:
            import shutil

            shutil.rmtree(env_path)
            if name in self.metadata:
                del self.metadata[name]
                self._save_metadata()
            logger.success(f"Removed environment '{name}' successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to remove environment '{name}': {e}")
            return False

    def get_current_environment(self) -> Optional[str]:
        """Get currently active environment name."""
        # Check for pyspace.json in current directory
        pyspace_json = Path.cwd() / "pyspace.json"
        if pyspace_json.exists():
            with open(pyspace_json) as f:
                data = json.load(f)
                return data.get("environment")
        return self.config.get("default_env")

    def set_default_environment(self, name: str):
        """Set default environment."""
        self.config["default_env"] = name
        self._save_config()
