from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    telegram_bot_token: str
    api_auth_token: str
    imeicheck_api_key: str
    db_path: str = "sqlite+aiosqlite:///./test.db"

    class Config:
        env_file = ".env"

settings = Settings()