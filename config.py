from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_URL: str
    JWT_ACCESS_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    ALGORITHM: str

    # Магия, которая читает файл .env
    model_config = SettingsConfigDict(env_file=".env")

# Создаем экземпляр, который будем импортировать везде
settings = Settings()