from advanced_alchemy import AsyncSessionConfig
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyAsyncConfig
from pydantic_settings import BaseSettings, SettingsConfigDict


class _Settings(BaseSettings):
    state_secret: str
    sqlalchemy_url: str
    client_id: str
    client_secret: str
    base_url: str

    model_config = SettingsConfigDict(env_file='.env')


settings = _Settings()

session_config = AsyncSessionConfig(expire_on_commit=False)
sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=settings.sqlalchemy_url,
    session_config=session_config,
)
