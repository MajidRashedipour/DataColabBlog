from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    TOKEN_TYPE: str
    ACCESS_TOKEN_EXPIRE_HOURS: int
    REFRESH_TOKEN_EXPIRE_HOURS: int

    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="ignore"
    )

Config = Settings()