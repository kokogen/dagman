from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Настройки базы данных
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "dagman"
    DB_PASSWORD: str = "dagman"
    DB_NAME: str = "dagman"
    
    # Настройки API сервера
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_RELOAD: bool = True
    
    # Формируем URL для подключения к базе данных
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings() 