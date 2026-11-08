from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class EnvironmentSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    django_secret_key: str = Field(validation_alias="DJANGO_SECRET_KEY")
    django_debug: bool = Field(
        default=False,
        validation_alias="DJANGO_DEBUG",
    )
    django_allowed_hosts: str = Field(
        default="",
        validation_alias="DJANGO_ALLOWED_HOSTS",
    )

    postgres_db: str = Field(validation_alias="POSTGRES_DB")
    postgres_user: str = Field(validation_alias="POSTGRES_USER")
    postgres_password: str = Field(validation_alias="POSTGRES_PASSWORD")
    postgres_host: str = Field(
        default="127.0.0.1",
        validation_alias="POSTGRES_HOST",
    )
    postgres_port: int = Field(
        default=5432,
        ge=1,
        le=65535,
        validation_alias="POSTGRES_PORT",
    )

    @property
    def allowed_hosts(self) -> list[str]:
        return [host.strip() for host in self.django_allowed_hosts.split(",") if host.strip()]
