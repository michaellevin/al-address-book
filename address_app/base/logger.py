import logging
from address_app import __app_name__

# ANSI escape sequences for colors
COLORS = {
    "WARNING": "\033[93m",  # Yellow
    "ERROR": "\033[91m",  # Red
    "CRITICAL": "\033[91m",  # Red
    "RESET": "\033[0m",  # Reset to default terminal color
}


class ColorizedFormatter(logging.Formatter):
    def format(self, record):
        levelname = record.levelname
        if levelname in COLORS:
            levelname_color = COLORS[levelname] + levelname + COLORS["RESET"]
            record.levelname = levelname_color
        return super().format(record)


# Now, you set up your loggers and handlers using the ColorizedFormatter

logger = logging.getLogger(__app_name__)
logger.setLevel(logging.DEBUG)  # Set the minimum level of logging

# Handler for lower-level logs (e.g., DEBUG, INFO)
info_handler = logging.StreamHandler()
info_handler.setLevel(logging.INFO)
info_format = ColorizedFormatter("%(asctime)s %(levelname)s %(message)s")
info_handler.setFormatter(info_format)
info_handler.addFilter(lambda record: record.levelno <= logging.INFO)

# Handler for higher-level logs (e.g., WARNING, ERROR, CRITICAL)
error_handler = logging.StreamHandler()
error_handler.setLevel(logging.WARNING)
error_format = ColorizedFormatter(
    "%(asctime)s %(levelname)s %(module)s.py:%(lineno)d %(message)s"
)
error_handler.setFormatter(error_format)

# Add handlers to the logger
logger.addHandler(info_handler)
logger.addHandler(error_handler)
