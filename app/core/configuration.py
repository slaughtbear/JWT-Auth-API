from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_username: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    frontend_url: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()