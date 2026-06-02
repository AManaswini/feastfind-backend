# app/core/config.py
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    allowed_origins: str = "http://localhost:3000"
    host: str = "0.0.0.0"
    port: int = 8000
    database_url: str = "postgresql+asyncpg://localhost/feastfind"
    openai_api_key: str = ""

    @property
    def origins_list(self) -> List[str]:
        return [o.strip() for o in self.allowed_origins.split(",")]

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
