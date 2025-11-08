import typer
from loguru import logger
from env_manager.environment import EnvironmentManager

env_manager = EnvironmentManager()


def list():
    """List all environments."""
    try:
        logger.info("CLI: Listing environments")
        envs = env_manager.list_environments()
        if envs:
            typer.echo("Environments:")
            for env in envs:
                status = " (active)" if env["active"] else ""
                typer.echo(f"  {env['name']} - Python {env['python_version']}{status}")
            logger.success(f"CLI: Listed {len(envs)} environments")
        else:
            typer.echo("No environments found")
            logger.info("CLI: No environments found")
    except Exception as e:
        typer.echo(f"Error listing environments: {e}")
        logger.error(f"CLI: Error listing environments: {e}")
        raise typer.Exit(1)
