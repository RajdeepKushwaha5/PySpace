import typer
from loguru import logger
from env_manager.cache import CacheManager

cache_manager = CacheManager()


def cache_clear():
    """Clear the cache."""
    try:
        logger.info("CLI: Clearing cache")
        cache_manager.clear_cache()
        typer.echo("Cache cleared")
        logger.success("CLI: Cache cleared successfully")
    except Exception as e:
        typer.echo(f"Error clearing cache: {e}")
        logger.error(f"CLI: Error clearing cache: {e}")
        raise typer.Exit(1)
