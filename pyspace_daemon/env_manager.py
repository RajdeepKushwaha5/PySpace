import venv
import subprocess
from pathlib import Path
from .utils import logger


def create_workspace_env(name: str, workspace_root: Path):
    """Create a workspace with venv and directories."""
    workspace_path = workspace_root / name
    workspace_path.mkdir(parents=True, exist_ok=True)
    env_path = workspace_path / ".env"
    env_path.mkdir(exist_ok=True)
    venv.create(str(env_path), with_pip=True)
    # Create subdirs
    (workspace_path / "notebooks").mkdir(exist_ok=True)
    (workspace_path / "scripts").mkdir(exist_ok=True)
    # Create requirements.txt
    req_file = workspace_path / "requirements.txt"
    req_file.write_text("")
    logger.info(f"Created workspace '{name}' at {workspace_path}")
    return env_path


def get_workspace_env_path(name: str, workspace_root: Path):
    """Get the path to the workspace's virtual environment."""
    return workspace_root / name / ".env"


def install_package(env_path: Path, package: str, cache_path: Path):
    """Install a package in the virtual environment using cache."""
    python_exe = env_path / "bin" / "python"  # Unix
    if not python_exe.exists():
        python_exe = env_path / "Scripts" / "python.exe"  # Windows
    cmd = [
        str(python_exe),
        "-m",
        "pip",
        "install",
        "--find-links",
        str(cache_path),
        package,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        logger.info(f"Installed {package} in {env_path}")
        return True
    else:
        logger.error(f"Failed to install {package}: {result.stderr}")
        return False
