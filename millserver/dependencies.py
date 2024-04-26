from httpx import AsyncClient

from millserver.oauth.github import GithubOauth
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
