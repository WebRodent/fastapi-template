import logging
from enum import Enum

from pydantic import Field
from pydantic_settings import BaseSettings


class LogLevels(str, Enum):
    CRITICAL = "CRITICAL"
    FATAL = "FATAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    WARN = "WARN"
    INFO = "INFO"
    DEBUG = "DEBUG"


class AppConfig(BaseSettings):
    # App settings
    DATABASE_URL: str = "sqlite:///:memory:"
    CACHE_ENABLED: bool = False
    ENV_NAME: str = "dev"

    # Logging settings
    LOG_LEVEL: LogLevels = LogLevels.DEBUG
    LOG_FORMAT: str = (
        "[%(asctime)s] [%(process)d] [%(levelname)s] [%(module)s.%(funcName)s] "
        "[%(filename)s:%(lineno)d] [%(name)s] %(message)s"
    )
    LOG_JSON: bool = False
    LOG_SQL: bool = True
    LOG_SQL_LEVEL: LogLevels = LogLevels.INFO

    class Config:
        env_prefix = (
            "APP_"  # Prefix for all environment variables, e.g., APP_DATABASE_URL
        )


def get_config():
    """Returns the app configuration."""
    logging.info("Loading app configuration")
    return AppConfig()
