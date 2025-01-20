import os
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    url: str = "postgresql+asyncpg://admin:admin@db/library"


class AuthJWT(BaseSettings):
    private_key_path: Path = Path(os.getenv("PRIVATE_KEY_PATH"))
    public_key_path: Path = Path(os.getenv("PUBLIC_KEY_PATH"))
    algorithm: str = "RS256"
    access_token_expire_seconds: int = 15 * 60  # 15 minutes
    refresh_token_expire_seconds: int = 30 * (24 * 60 * 60)  # 30 days


class LoggingSettings(BaseSettings):
    filename: str = os.path.join("/var/log", "log_file.log")
    max_bytes: int = 50 * 1024  # 50kb
    backup_count: int = 3


class Settings(BaseModel):
    model_config = SettingsConfigDict(case_sensitive=False)
    db: PostgresSettings = PostgresSettings()
    auth_jwt: AuthJWT = AuthJWT()
    logging: LoggingSettings = LoggingSettings()


settings = Settings()
