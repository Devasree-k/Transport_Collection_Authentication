import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.core.config import LOG_DIR, LOG_LEVEL


def configure_logging() -> None:

    # Create log directory if it doesn't exist
    log_directory = Path(LOG_DIR)
    log_directory.mkdir(parents=True, exist_ok=True)

    # Log format
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # Get root logger
    root_logger = logging.getLogger()

    # Set log level
    root_logger.setLevel(
        getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    )

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
        handler.close()

    # File handler with rotation
    file_handler = RotatingFileHandler(
        filename=log_directory / "application.log",
        maxBytes=5_000_000,
        backupCount=3,
        encoding="utf-8"
    )

    file_handler.setFormatter(formatter)
    file_handler.setLevel(
        getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    )

    # Add only file handler (no console handler)
    root_logger.addHandler(file_handler)

    # Prevent propagation to parent loggers
    root_logger.propagate = False


