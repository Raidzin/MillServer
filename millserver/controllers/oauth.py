from typing import Annotated

from httpx import AsyncClient
from litestar import Controller, get
from litestar.datastructures import Cookie
from litestar.di import Provide
from litestar.params import Parameter
from litestar.response import Redirect, Response

from millserver.dependencies import provide_github_oauth
from millserver.oauth.github import GithubOauth
from millserver.security.authentication_middleware import API_TOKEN_COOKIE_NAME


class GithubOauthController(Controller):
    path = '/oauth/github'
    dependencies = {
        'github_oauth': Provide(provide_github_oauth, sync_to_thread=True),
    }

    @get('/login')
    async def register_user(
            self,
            github_oauth: GithubOauth,
            login: str | None = None,
    ) -> Redirect:
        return Redirect(
            path=github_oauth.get_authorize_url(login),
        )

    @get()
    async def oauth_github(
            self,
            code: str,
            gh_state: Annotated[str, Parameter(query='state')],
            github_oauth: GithubOauth,
            http_client: AsyncClient,
    ) -> Response[dict]:
        access_token = await github_oauth.get_access_token(
            state=gh_state,
            code=code,
            http_client=http_client,
        )
        return Response(
            content={'success': True},
            cookies=(
                Cookie(
                    key=API_TOKEN_COOKIE_NAME,
                    value=access_token,
                    httponly=True,
                ),
            ),
        )
