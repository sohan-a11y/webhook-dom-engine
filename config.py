from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    HEADLESS: bool = True
    MAX_CONCURRENT_CONTEXTS: int = 5
    DEFAULT_TIMEOUT_MS: int = 15000

    class Config:
        env_file = ".env"

settings = Settings()
