# app/infrastructure/config/settings.py

import os
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    ENVIRONMENT: Literal["develop", "development", "staging", "production"] = os.getenv(
        "ENVIRONMENT", "develop"
    )
    API_TITLE: str = os.getenv("API_TITLE", "SNT Trade Tool API")
    API_VERSION: str = os.getenv("API_VERSION", "1.0.0")
    API_DESCRIPTION: str = os.getenv(
        "API_DESCRIPTION", "API para obtener información del universo de EVE Online"
    )
    DOMAIN: str = os.getenv("DOMAIN", "http://localhost:8000")
    ENDPOINT_MAX_AGE: int = os.getenv("ENDPOINT_MAX_AGE", 86400)
    ENDPOINT_MIN_AGE: int = os.getenv("ENDPOINT_MIN_AGE", 60)
    ESI_URL: str = os.getenv("ESI_URL", "https://esi.evetech.net")
    ESI_VERSION: str = os.getenv("ESI_VERSION", "v6")
