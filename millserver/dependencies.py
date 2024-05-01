from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from millserver.oauth.github import GithubOauth
from millserver.repository import UserRepository
from millserver.settings import settings

_github_oauth = GithubOauth(
    client_id=settings.client_id,
    client_secret=settings.client_secret,
    state_secret=settings.state_secret,
)


def provide_github_oauth() -> GithubOauth:
    return _github_oauth


_http_client = AsyncClient()


def provide_http_client() -> AsyncClient:
    return _http_client


def provide_user_repository(db_session: AsyncSession) -> UserRepository:
    return UserRepository(session=db_session)
