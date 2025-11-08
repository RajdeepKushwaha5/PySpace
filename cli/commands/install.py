import typer
from loguru import logger
from env_manager.environment import EnvironmentManager

env_manager = EnvironmentManager()


def install(packages: list[str], global_: bool = typer.Option(False, "--global")):
    """Install packages in the current or global environment."""
    try:
        logger.info(f"CLI: Installing packages {packages} (global: {global_})")
        if global_:
            typer.echo("Installing globally...")
            # Implement global install
            logger.info("CLI: Global install not yet implemented")
        else:
            typer.echo("Installing in current environment...")
            # Implement local install
            logger.info("CLI: Local install not yet implemented")
        logger.success(f"CLI: Install command completed for packages {packages}")
    except Exception as e:
        typer.echo(f"Error installing packages: {e}")
        logger.error(f"CLI: Error installing packages {packages}: {e}")
        raise typer.Exit(1)
