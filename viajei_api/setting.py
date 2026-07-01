from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='uft-8'
    )

    # DATABASE_URL: str = Field(init=False, default_factory=)
