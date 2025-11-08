import typer
from loguru import logger
from env_manager.environment import EnvironmentManager
from daemon.daemon import PySpaceDaemon

env_manager = EnvironmentManager()
daemon = PySpaceDaemon()


def status():
    """Show current status."""
    try:
        logger.info("CLI: Checking status")
        current = env_manager.get_current_environment()
        if current:
            typer.echo(f"Current environment: {current}")
        else:
            typer.echo("No active environment")

        daemon_status = daemon.get_status()
        typer.echo(f"Daemon status: {daemon_status}")
        logger.success("CLI: Status check completed")
    except Exception as e:
        typer.echo(f"Error checking status: {e}")
        logger.error(f"CLI: Error checking status: {e}")
        raise typer.Exit(1)
