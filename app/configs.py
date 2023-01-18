from pydantic import BaseModel


class LogConfig(BaseModel):
    """Logging configuration"""

    LOGGER_NAME: str = "restaurant"
    LOG_STDOUT_FORMAT = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_FILE_FORMAT: str = " %(asctime)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"
    LOG_PATH: str = "../logs.log"

    version = 1
    disable_existing_loggers = False
    formatters = {
        "stdout": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_STDOUT_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "file": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FILE_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
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
