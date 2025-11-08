import typer
from loguru import logger
from env_manager.environment import EnvironmentManager
from env_manager.config import ConfigManager

env_manager = EnvironmentManager()
config_manager = ConfigManager()


def use(name: str):
    """Switch to an environment."""
    try:
        logger.info(f"CLI: Switching to environment '{name}'")
        if env_manager.activate_environment(name):
            config_manager.set_local_config({"environment": name})
            typer.echo(f"Switched to environment '{name}'")
            logger.success(f"CLI: Switched to environment '{name}' successfully")
        else:
            typer.echo(f"Environment '{name}' not found")
            logger.warning(f"CLI: Environment '{name}' not found")
    except Exception as e:
        typer.echo(f"Error switching to environment: {e}")
        logger.error(f"CLI: Error switching to environment '{name}': {e}")
        raise typer.Exit(1)
