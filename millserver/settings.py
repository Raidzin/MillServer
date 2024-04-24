from pydantic_settings import BaseSettings, SettingsConfigDict


class _Settings(BaseSettings):
    app_secret: str
    sqlalchemy_url: str
    client_id: str
    client_secret: str
    base_url: str

    model_config = SettingsConfigDict(env_file='.env')


settings = _Settings()
