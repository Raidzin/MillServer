from typing import Annotated, Literal

import jwt
from litestar import Litestar, get
from litestar.response import Redirect, Response
from litestar.openapi import OpenAPIConfig
from litestar.openapi.spec import Server
from litestar.params import Parameter
from httpx import AsyncClient

from millserver.settings import settings

STATE_ENCODE_ALGORITHM = 'HS256'
APP_URL = 'https://raidzin.github.io/vue-mill'

GITHUB_OAUTH_AUTHORIZE_URL = 'https://github.com/login/oauth/authorize'
GITHUB_OAUTH_ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'


@get('/')
async def index() -> str:
    return 'Hello from index page'


@get('/oauth/github/login')
async def register_user() -> Redirect:
    state_jwt = jwt.encode(
        payload={'iss': 'MillServer'},
        key=settings.app_secret,
        algorithm=STATE_ENCODE_ALGORITHM,
    )
    path = GITHUB_OAUTH_AUTHORIZE_URL + (
        f'?client_id={settings.client_id}'
        # f'&redirect_uri=https://raidzin.ddns.net:30000/api/dev/schamas/swagger'
        f'&scope=read:user user:email'
        f'&state={state_jwt}'
    )
    return Redirect(
        path=path
    )


@get('/oauth/github')
async def oauth_github(
        code: str, gh_state: Annotated[str, Parameter(query='state')]
) -> Response[dict]:
    payload = jwt.decode(
        jwt=gh_state,
        key=settings.app_secret,
        algorithms=[STATE_ENCODE_ALGORITHM],
    )
    async with AsyncClient() as client:
        url = GITHUB_OAUTH_ACCESS_TOKEN_URL + (
            f'?client_id={settings.client_id}'
            f'&client_secret={settings.client_secret}'
            f'&code={code}'
            # f'&redirect_uri={APP_URL}'
        )
        response = await client.get(
            url, headers={'accept': 'application/json'}
        )
    if response.status_code != 200:
        api_response = Response(
            status_code=400
        )

    api_response = Response(
        content=response.json(),
    )
    return api_response


app = Litestar(
    route_handlers=[index, register_user, oauth_github],
    openapi_config=OpenAPIConfig(
        title='Mill Game Server API',
        version='0.1.0',
        servers=[Server(url=settings.base_url)]
    )
)
