from uuid import UUID

from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.middleware import (
    AbstractAuthenticationMiddleware,
    AuthenticationResult,
)
from jwt.exceptions import DecodeError
from sqlalchemy.ext.asyncio import AsyncSession

from millserver.dependencies import provide_user_repository
from millserver.repository import UserRepository
from millserver.security.jwt import decode_jwt_token

API_TOKEN_COOKIE_NAME = 'mill_token'


class CookieAuthenticationMiddleware(AbstractAuthenticationMiddleware):
    async def authenticate_request(
            self,
            connection: ASGIConnection,
    ) -> AuthenticationResult:
        access_token = connection.cookies.get(API_TOKEN_COOKIE_NAME, None)
        if access_token is None:
            raise NotAuthorizedException()
        try:
            token_payload = decode_jwt_token(token=access_token)
        except DecodeError as error:
            raise NotAuthorizedException()
        async with AsyncSession(connection.app.state.db_engine) as session:
            user_repository: UserRepository = (
                await connection.app.dependencies.get('user_repository')
                .dependency(session)
            )
            user = await user_repository.get(UUID(token_payload.sub))
        return AuthenticationResult(user=user, auth=token_payload)
