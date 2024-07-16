from typing import Literal

from pydantic import BaseModel


class LoggingSettings(BaseModel):
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    logger_name: str = "root"

    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict[str, dict] = {
        "default": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"},
    }
    handlers: dict[str, dict] = {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
            "level": log_level,
        },
    }
    loggers: dict[str, dict] = {
        logger_name: {
            "handlers": ["console"],
            "level": log_level,
            "propagate": False,
        },
    }

    def as_dictconfig(self) -> dict:
        config = self.dict()
        config["handlers"]["console"]["level"] = self.log_level
        config["loggers"][self.logger_name]["level"] = self.log_level
        return config
