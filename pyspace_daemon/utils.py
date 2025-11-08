from loguru import logger
import sys

# Configure logging
logger.remove()
logger.add(
    sys.stdout, level="INFO", format="<green>{time}</green> <level>{message}</level>"
)
logger.add(
    "pyspace.log", rotation="10 MB", level="DEBUG", format="{time} {level} {message}"
)

# Export logger for use in other modules
__all__ = ["logger"]
