"""Модуль настройки окружения"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Класс конфигурации из переменных среды"""

    SERVER_ADDRESS: str
    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DATABASE: str

    @property
    def DATABASE_URL(self) -> str: # pylint: disable=invalid-name
        """URL для синхронного подключения к БД"""
        return f"postgresql+asyncpg://{self.POSTGRES_USERNAME}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DATABASE}" # pylint: disable=line-too-long

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
