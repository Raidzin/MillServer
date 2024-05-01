import traceback

from advanced_alchemy.extensions.litestar import SQLAlchemyInitPlugin
from litestar import Litestar, get
from litestar.di import Provide
from litestar.middleware import DefineMiddleware
from litestar.openapi import OpenAPIConfig
from litestar.openapi.spec import Server
from litestar.response import Redirect
from litestar.types import Scope
from sqlalchemy.ext.asyncio import AsyncEngine

from millserver.controllers.oauth import GithubOauthController
from millserver.controllers.user import UserController
from millserver.dependencies import (
    provide_http_client,
    provide_user_repository, provide_github_oauth,
)
from millserver.models import UUIDBase
from millserver.security.authentication_middleware import \
    CookieAuthenticationMiddleware
from millserver.settings import settings, sqlalchemy_config

auth_mw = DefineMiddleware(
    middleware=CookieAuthenticationMiddleware,
    exclude=['schema', 'oauth'])


@get('/')
async def index() -> Redirect:
    return Redirect(settings.base_url + '/schema/swagger')


async def add_db_engine_to_state(app: Litestar):
    if not getattr(app.state, 'db_engine', None):
        app.state.engine = sqlalchemy_config.get_engine()


async def create_db_tables():
    async with sqlalchemy_config.get_engine().begin() as conn:
        await conn.run_sync(UUIDBase.metadata.create_all)


async def close_http_client():
    http_client = provide_http_client()
    await http_client.aclose()


async def after_exception_handler(exc: Exception, scope: "Scope") -> None:
    print(traceback.format_exc())


app = Litestar(
    route_handlers=[index, GithubOauthController, UserController],
    dependencies={
        'http_client': Provide(
            dependency=provide_http_client,
            sync_to_thread=True,
        ),
        'user_repository': Provide(
            dependency=provide_user_repository,
            sync_to_thread=True,
        ),
        'github_oauth': Provide(
            provide_github_oauth,
            sync_to_thread=True,
        ),

    },
    on_startup=[create_db_tables],
    on_shutdown=[close_http_client],
    after_exception=[after_exception_handler],
    middleware=[auth_mw],
    plugins=[SQLAlchemyInitPlugin(config=sqlalchemy_config)],
    openapi_config=OpenAPIConfig(
        title='Mill Game Server API',
        version='0.1.0',
        servers=[Server(url=settings.base_url)],
    ),

)
