"""Common logging setup for the WhatsVector project."""

import logging


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Sets up and returns a logger with the specified name and level.
    Args:
        name (str): The name of the logger.
        level (int): The logging level (default is logging.INFO).
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


app_logger = setup_logger("whatsvector")
