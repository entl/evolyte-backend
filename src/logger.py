import logging
from logging.config import dictConfig
import ecs_logging

DEFAULT_LEVEL = logging.DEBUG

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,  # Preserve other library loggers
    "formatters": {"ecs": {"()": ecs_logging.StdlibFormatter}},
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "ecs",
            "level": DEFAULT_LEVEL,
            "stream": "ext://sys.stdout",
        }
    },
    "root": {"level": DEFAULT_LEVEL, "handlers": ["console"]},
}


def setup_logging(level: int | None = None) -> None:
    """
    Configure the root logger with an ECS formatter on stdout.
    Call once at application startup.
    """
    if level is not None:
        # override the default level on both handler and root
        LOGGING_CONFIG["handlers"]["console"]["level"] = level
        LOGGING_CONFIG["root"]["level"] = level

    dictConfig(LOGGING_CONFIG)


def get_logger(name: str | None = None) -> logging.Logger:
    """
    Return a logger with the given name (default: caller`s module name).
    Modules should do:
        logger = get_logger(__name__)
    """
    return logging.getLogger(name or __name__)
