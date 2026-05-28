from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")

    database_url: str
    rabbitmq_url: str
    api_key: SecretStr
    outbox_poll_interval: int = 5
    webhook_max_retries: int = 3
    log_level: str = "info"


@lru_cache
def get_settings() -> Settings:
    return Settings()
