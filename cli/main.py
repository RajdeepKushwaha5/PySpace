import typer
from env_manager.environment import EnvironmentManager
from env_manager.cache import CacheManager
from env_manager.config import ConfigManager
from .commands.init import init as init_cmd
from .commands.use import use as use_cmd
from .commands.create import create as create_cmd
from .commands.install import install as install_cmd
from .commands.list import list as list_cmd
from .commands.remove import remove as remove_cmd
from .commands.status import status as status_cmd
from .commands.cache_clear import cache_clear as cache_clear_cmd
from .commands.doctor import doctor as doctor_cmd

app = typer.Typer()
env_manager = EnvironmentManager()
cache_manager = CacheManager()
config_manager = ConfigManager()


@app.command()
def init(name: str = None):
    """Initialize PySpace in current directory."""
    init_cmd(name)


@app.command()
def use(name: str):
    """Switch to a different environment."""
    use_cmd(name)


@app.command()
def create(name: str, python: str = None):
    """Create a new environment."""
    create_cmd(name, python)


@app.command()
def install(
    package: str,
    global_flag: bool = typer.Option(False, "--global"),
    local: bool = typer.Option(False, "--local"),
):
    """Install a package."""
    install_cmd([package], global_flag)


@app.command()
def list():
    """List all environments."""
    list_cmd()


@app.command()
def remove(name: str):
    """Remove an environment."""
    remove_cmd(name)


@app.command()
def status():
    """Show current status."""
    status_cmd()


@app.command()
def cache_clear():
    """Clear the package cache."""
    cache_clear_cmd()


@app.command()
def doctor():
    """Run diagnostics."""
    doctor_cmd()


if __name__ == "__main__":
    app()
