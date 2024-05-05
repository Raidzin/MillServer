from httpx import AsyncClient
from litestar import Request, get
from litestar.controller import Controller
from litestar.datastructures import State

from millserver.data_transfer import UserDTO

# from millserver.repository import UserRepository
from millserver.models import User
from millserver.oauth.github import GithubOauth
from millserver.schemas import UserData
from millserver.security.jwt import AccessTokenPayload


class UserController(Controller):
    path = '/users'

    @get('/me', return_dto=UserDTO)
    async def get_my_data(
            self,
            request: Request[User, AccessTokenPayload, State],
            github_oauth: GithubOauth,
            http_client: AsyncClient,
    ) -> UserData:
        user_data = await github_oauth.get_user_data(
            access_token=request.auth.oauth_token,
            http_client=http_client,
        )
        return UserData(**(user_data.model_dump() | request.user.to_dict()))
