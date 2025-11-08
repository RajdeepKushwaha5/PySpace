from fastapi import FastAPI, HTTPException
from .workspace_manager import WorkspaceManager
from .cache_manager import CacheManager
from .env_manager import create_workspace_env
from .config_manager import ConfigManager
from pathlib import Path
import subprocess

app = FastAPI()

config = ConfigManager()
wm = WorkspaceManager(Path.home() / ".pyspace" / "metadata.db")
cm = CacheManager(Path(config.get("default_cache_path")))


@app.get("/")
def read_root():
    return {"message": "PySpace Daemon API"}


@app.get("/workspaces")
def list_workspaces():
    return {"workspaces": wm.list_workspaces()}


@app.post("/workspaces")
def create_workspace(name: str):
    workspace_root = Path(config.get("workspace_root"))
    env_path = create_workspace_env(name, workspace_root)
    if wm.create_workspace(name, str(env_path)):
        return {"message": f"Workspace {name} created"}
    raise HTTPException(status_code=400, detail="Workspace already exists")


@app.get("/workspaces/{name}")
def get_workspace(name: str):
    path = wm.get_workspace(name)
    if path:
        return {"path": path}
    raise HTTPException(status_code=404, detail="Workspace not found")


@app.post("/install/{workspace}")
def install_package(workspace: str, package: str):
    env_path = wm.get_workspace(workspace)
    if not env_path:
        raise HTTPException(status_code=404, detail="Workspace not found")
    cm.download_wheel(package)
    from .env_manager import install_package

    if install_package(Path(env_path), package, cm.get_cache_path()):
        return {"message": f"Installed {package} in {workspace}"}
    raise HTTPException(status_code=500, detail="Install failed")


@app.post("/workspaces/{name}/reset")
def reset_workspace(name: str):
    env_path_str = wm.get_workspace(name)
    if not env_path_str:
        raise HTTPException(status_code=404, detail="Workspace not found")
    env_path = Path(env_path_str)
    if env_path.exists():
        import shutil

        shutil.rmtree(env_path)
    workspace_root = Path(config.get("workspace_root"))
    create_workspace_env(name, workspace_root)
    return {"message": f"Reset workspace {name}"}


@app.post("/workspaces/{name}/snapshot")
def snapshot_workspace(name: str):
    env_path_str = wm.get_workspace(name)
    if not env_path_str:
        raise HTTPException(status_code=404, detail="Workspace not found")
    env_path = Path(env_path_str)
    requirements_file = env_path / "requirements.txt"
    # Generate requirements.txt using pip freeze
    python_exe = (
        env_path / "Scripts" / "python.exe"
        if (env_path / "Scripts").exists()
        else env_path / "bin" / "python"
    )
    result = subprocess.run(
        [str(python_exe), "-m", "pip", "freeze"],
        capture_output=True,
        text=True,
        cwd=env_path,
    )
    if result.returncode == 0:
        requirements_file.write_text(result.stdout)
        return {"message": f"Snapshot saved for {name}"}
    else:
        raise HTTPException(
            status_code=500, detail="Failed to generate requirements.txt"
        )


@app.post("/cache/clean")
def clean_cache():
    cm.clean_cache()
    return {"message": "Cache cleaned"}


@app.get("/config")
def get_config():
    return config.config
