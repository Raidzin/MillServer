from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.middleware import (
    AbstractAuthenticationMiddleware,
    AuthenticationResult,
)

API_TOKEN_COOKIE_NAME = 'gh_token'


class CookieAuthenticationMiddleware(AbstractAuthenticationMiddleware):
    async def authenticate_request(
            self,
            connection: ASGIConnection,
    ) -> AuthenticationResult:
        access_token = connection.cookies.get(API_TOKEN_COOKIE_NAME, None)
        if access_token is None:
            raise NotAuthorizedException()
        


