import logging

from dotenv import find_dotenv, load_dotenv
from pydantic import Field

from pydantic_settings import BaseSettings

load_dotenv(find_dotenv())


class AppSettings(BaseSettings):
    db: str = Field(..., alias="DATABASE_URL")
    app_name: str | None = Field("", alias="APP_NAME")
    description: str | None = Field("", alias="DESCRIPTION")
    version: str | None = Field("0.0.1", alias="VERSION")

    redis_url: str = Field(..., alias="REDIS_URL")


class LoggingSettings(BaseSettings):
    level: str = Field("INFO", alias="LOGGING_LVL")
    format: str = Field("%(asctime)s - %(name)s - %(levelname)s - %(message)s", alias="LOGGING_FORMAT")

    @property
    def logging_lvl(self):
        return getattr(logging, self.level, logging.ERROR)


settings = AppSettings()
logging_settings = LoggingSettings()
