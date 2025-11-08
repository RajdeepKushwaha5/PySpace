import typer
from loguru import logger
from env_manager.utils import run_command


def doctor():
    """Run diagnostics."""
    try:
        logger.info("CLI: Running diagnostics")
        typer.echo("Running diagnostics...")

        # Check Python version
        returncode, stdout, stderr = run_command(["python", "--version"])
        typer.echo(f"Python version: {stdout.strip()}")

        # Check pip
        returncode, stdout, stderr = run_command(["pip", "--version"])
        typer.echo(f"Pip version: {stdout.strip()}")

        # Check pyenv if available
        returncode, stdout, stderr = run_command(["pyenv", "--version"])
        if returncode == 0:
            typer.echo(f"Pyenv version: {stdout.strip()}")
        else:
            typer.echo("Pyenv not found")

        typer.echo("Diagnostics complete")
        logger.success("CLI: Diagnostics completed successfully")
    except Exception as e:
        typer.echo(f"Error running diagnostics: {e}")
        logger.error(f"CLI: Error running diagnostics: {e}")
        raise typer.Exit(1)
