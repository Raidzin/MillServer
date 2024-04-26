from litestar import Litestar, get
from litestar.di import Provide
from litestar.openapi import OpenAPIConfig
from litestar.openapi.spec import Server

from millserver.controllers.oauth import GithubOauthController
from millserver.dependencies import provide_http_client
from millserver.settings import settings


@get('/')
async def index() -> str:
    return 'Hello from index page'


async def close_http_client():
    http_client = provide_http_client()
    await http_client.aclose()


app = Litestar(
    route_handlers=[index, GithubOauthController],
    dependencies={
        'http_client': Provide(provide_http_client, sync_to_thread=True),
    },
    on_shutdown=[close_http_client],
    openapi_config=OpenAPIConfig(
        title='Mill Game Server API',
        version='0.1.0',
        servers=[Server(url=settings.base_url)],
    ),

)
