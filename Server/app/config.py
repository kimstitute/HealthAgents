from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Health Agents Server"
    debug: bool = True

    # LLM API 설정
    openai_api_key: str | None = None
    llm_model: str = "gpt-5-nano"
    llm_temperature: float = 0.3
    llm_max_tokens: int = 1500

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings() 