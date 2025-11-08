import typer
from loguru import logger
from env_manager.environment import EnvironmentManager

env_manager = EnvironmentManager()


def create(name: str, python: str = typer.Option(None, "--python")):
    """Create a new environment."""
    try:
        logger.info(
            f"CLI: Creating environment '{name}' with Python {python or 'default'}"
        )
        if env_manager.create_environment(name, python):
            typer.echo(f"Created environment '{name}'")
            logger.success(f"CLI: Environment '{name}' created successfully")
        else:
            typer.echo(
                f"Failed to create environment '{name}' - it may already exist or Python version not found"
            )
            logger.warning(f"CLI: Failed to create environment '{name}'")
    except Exception as e:
        typer.echo(f"Error creating environment: {e}")
        logger.error(f"CLI: Error creating environment '{name}': {e}")
        raise typer.Exit(1)
