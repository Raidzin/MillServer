from datetime import datetime
from typing import Annotated

from httpx import AsyncClient
from litestar import Controller, get
from litestar.datastructures import Cookie
from litestar.di import Provide
from litestar.params import Parameter
from litestar.response import Redirect, Response

from millserver.core.users import create_user, get_user_or_none_by_login
from millserver.dependencies import provide_github_oauth
from millserver.oauth.github import GithubOauth
from millserver.repository import UserRepository
from millserver.security.authentication_middleware import API_TOKEN_COOKIE_NAME
from millserver.security.jwt import create_jwt_token

ONE_YEAR = 60 * 60 * 24 * 365


class GithubOauthController(Controller):
    path = '/oauth/github'

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
            user_repository: UserRepository,
            github_oauth: GithubOauth,
            http_client: AsyncClient,
    ) -> Response[dict]:
        github_access_token = await github_oauth.get_access_token(
            state=gh_state,
            code=code,
            http_client=http_client,
        )
        user_data = await github_oauth.get_user_data(
            access_token=github_access_token,
            http_client=http_client,
        )
        user = await get_user_or_none_by_login(
            login=user_data.login,
            user_repository=user_repository,
        )
        if user is None:
            user_id = await create_user(
                login=user_data.login,
                user_repository=user_repository,
            )
        else:
            user_id = user.id
        return Response(
            content={'success': True},
            cookies=(
                Cookie(
                    key=API_TOKEN_COOKIE_NAME,
                    value=create_jwt_token(
                        user_id=user_id,
                        oauth_token=github_access_token,
                    ),
                    httponly=True,
                    expires=int(datetime.now().timestamp()) + ONE_YEAR,
                ),
            ),
        )
