from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "FastAPI App"
    debug: bool = False
    API_V1_STR: str = "/api/v1"

    class Config:
        env_file = ".env"

settings = Settings()