from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# TODO: доработать файл настроек сделать его болле профессионально
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = Field(alias="DATABASE_URL")
    htx_base_url: str = Field(alias="HTX_BASE_URL")
    htx_access_key: str = Field(alias="HTX_ACCESS_KEY")
    htx_secret_key: str = Field(alias="HTX_SECRET_KEY")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
