import os
import subprocess
from pathlib import Path
from typing import Optional


def run_command(cmd: list, cwd: Optional[Path] = None) -> tuple[int, str, str]:
    """Run a command and return (returncode, stdout, stderr)."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
        return result.returncode, result.stdout, result.stderr
    except FileNotFoundError:
        return 1, "", "Command not found"


def is_windows() -> bool:
    return os.name == "nt"


def get_python_executable(env_path: Path) -> Path:
    """Get Python executable path for environment."""
    if is_windows():
        return env_path / "Scripts" / "python.exe"
    else:
        return env_path / "bin" / "python"


def get_activate_script(env_path: Path) -> Path:
    """Get activation script path for environment."""
    if is_windows():
        return env_path / "Scripts" / "activate.bat"
    else:
        return env_path / "bin" / "activate"


def ensure_directory(path: Path):
    """Ensure directory exists."""
    path.mkdir(parents=True, exist_ok=True)
