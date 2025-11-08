import typer
from loguru import logger
from env_manager.environment import EnvironmentManager

env_manager = EnvironmentManager()


def remove(name: str):
    """Remove an environment."""
    try:
        logger.info(f"CLI: Removing environment '{name}'")
        if env_manager.remove_environment(name):
            typer.echo(f"Removed environment '{name}'")
            logger.success(f"CLI: Environment '{name}' removed successfully")
        else:
            typer.echo(f"Environment '{name}' not found")
            logger.warning(f"CLI: Environment '{name}' not found")
    except Exception as e:
        typer.echo(f"Error removing environment: {e}")
        logger.error(f"CLI: Error removing environment '{name}': {e}")
        raise typer.Exit(1)
