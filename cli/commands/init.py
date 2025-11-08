import typer
from loguru import logger
from env_manager.config import ConfigManager

config_manager = ConfigManager()


def init():
    """Initialize PySpace in the current directory."""
    try:
        logger.info("CLI: Initializing PySpace in current directory")
        config_manager.initialize_local_config()
        typer.echo("Initialized PySpace in current directory")
        logger.success("CLI: PySpace initialized successfully")
    except Exception as e:
        typer.echo(f"Error initializing PySpace: {e}")
        logger.error(f"CLI: Error initializing PySpace: {e}")
        raise typer.Exit(1)
