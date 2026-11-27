import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from typing import Literal



class Settings(BaseSettings):

    app_env: Literal[
        "development",
        "testing",
        "production",
    ] = "development"

    DATABASE_URL: str

    secret_key: SecretStr
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
    )

def get_settings() -> Settings:

    environment = os.getenv("APP_ENV", "development")
    env_file = (
        ".env.test" if environment == "testing" else ".env"
    )
    return Settings(_env_file=env_file)

settings = get_settings()