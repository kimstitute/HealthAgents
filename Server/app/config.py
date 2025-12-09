from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Health Agents Server"
    debug: bool = True

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings() 