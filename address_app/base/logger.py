import logging
from address_app import __app_name__

#: ANSI escape sequences for colors
_COLORS = {
    "WARNING": "\033[93m",  # Yellow
    "ERROR": "\033[91m",  # Red
    "CRITICAL": "\033[91m",  # Red
    "RESET": "\033[0m",  # Reset to default terminal color
}


class _ColorizedFormatter(logging.Formatter):
    """A private formatter to add color to logging levels."""

    def format(self, record):
        levelname = record.levelname
        if levelname in _COLORS:
            levelname_color = _COLORS[levelname] + levelname + _COLORS["RESET"]
            record.levelname = levelname_color
        return super().format(record)


_logger_initialized = False


def get_logger():
    """
    Retrieves the application's configured logger. If the logger has not been
    configured yet, it does so. This ensures that the logger is configured only once.

    Returns:
        logging.Logger: The configured logger.
    """
    global _logger_initialized
    logger = logging.getLogger(__app_name__)

    if not _logger_initialized:
        logger.setLevel(logging.DEBUG)  # Set the minimum level of logging

        # Handler for lower-level logs (e.g., DEBUG, INFO)
        info_handler = logging.StreamHandler()
        info_handler.setLevel(logging.INFO)
        info_format = _ColorizedFormatter("%(asctime)s %(levelname)s %(message)s")
        info_handler.setFormatter(info_format)
        info_handler.addFilter(lambda record: record.levelno <= logging.INFO)

        # Handler for higher-level logs (e.g., WARNING, ERROR, CRITICAL)
        error_handler = logging.StreamHandler()
        error_handler.setLevel(logging.WARNING)
        error_format = _ColorizedFormatter(
            "%(asctime)s %(levelname)s %(module)s.py:%(lineno)d %(message)s"
        )
        error_handler.setFormatter(error_format)

        # Add handlers to the logger
        logger.addHandler(info_handler)
        logger.addHandler(error_handler)

        _logger_initialized = True

    return logger


def set_logger_level(level=logging.DEBUG):
    """
    Sets the log level for the application's logger. Setting the level to
    logging.CRITICAL effectively mutes the logger. This function allows for
    dynamic adjustment of the logging verbosity.

    Args:
        level (int): The logging level to set. Use logging module's constants
                     like logging.DEBUG, logging.INFO, etc.
    """
    logger = get_logger()  # Ensure the logger is initialized
    logger.setLevel(level)
    for handler in logger.handlers:
        handler.setLevel(level)
