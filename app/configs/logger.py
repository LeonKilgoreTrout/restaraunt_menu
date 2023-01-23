from pydantic import BaseModel
from logging.config import dictConfig
import logging


class LogConfig(BaseModel):
    """Logging configuration"""

    LOGGER_NAME: str = "restaurant"
    LOG_STDOUT_FORMAT = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_FILE_FORMAT: str = " %(asctime)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"
    LOG_PATH: str = "../logs.log"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    version = 1
    disable_existing_loggers = False
    formatters = {
        "stdout": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_STDOUT_FORMAT,
            "datefmt": DATE_FORMAT,
        },
        "file": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FILE_FORMAT,
            "datefmt": DATE_FORMAT,
        },
    }
    handlers = {
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "file",
            "filename": LOG_PATH,
            "encoding": "utf-8",
            "maxBytes": 500000,
            "backupCount": 4
        },
        "stdout": {
            "formatter": "stdout",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        LOGGER_NAME: {"handlers": ["file", "stdout"], "level": LOG_LEVEL},
    }


dictConfig(LogConfig().dict())
Logger = logging.getLogger('restaurant')
