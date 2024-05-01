from typing import TYPE_CHECKING

import jwt
from httpx import HTTPError
from jwt import InvalidTokenError
from pydantic import BaseModel, ConfigDict, HttpUrl, ValidationError

from millserver.exceptions import (
    GetAccessTokenError,
    InvalidStateError,
    OauthError,
)

if TYPE_CHECKING:
    from httpx import AsyncClient

ACCEPT_APPLICATION_JSON_HEADERS = {'accept': 'application/json'}
USER_API_URL = 'https://api.github.com/user'


def create_bearer_auth_header(token):
    return {'authorization': f'Bearer {token}'}


class OauthAccessTokenResponse(BaseModel):
    access_token: str
    scope: str
    token_type: str

    model_config = ConfigDict(extra='ignore')


class GitHubUserData(BaseModel):
    login: str
    avatar_url: HttpUrl
    model_config = ConfigDict(extra='ignore')


class GithubOauth:
    """
    - **get_authorize_url**: returns redirect url for user authorization.
    - **get_access_token**: get access token for oauth provider
    - **validate_state**:  check that state is valid

    """
    _encode_algorithm = 'HS256'
    _authorize_url = 'https://github.com/login/oauth/authorize'
    _access_token_url = 'https://github.com/login/oauth/access_token'

    def __init__(
            self,
            client_id: str,
            client_secret: str,
            state_secret: str,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.state_secret = state_secret

    def get_authorize_url(self, login: str | None = None) -> str:
        redirect_url = self._authorize_url + (
            f'?client_id={self.client_id}'
            f'&scope=read:user user:email'
            f'&state={self.state}'
        )
        if login is not None:
            redirect_url += f'&login={login}'
        return redirect_url

    async def get_access_token(
            self,
            state: str,
            code: str,
            http_client: 'AsyncClient',
    ) -> str:
        self.validate_state(state)
        token_url = self._access_token_url + (
            f'?client_id={self.client_id}'
            f'&client_secret={self.client_secret}'
            f'&code={code}'
        )
        try:
            response = await http_client.get(
                url=token_url,
                headers=ACCEPT_APPLICATION_JSON_HEADERS,
            )
            response.raise_for_status()
        except HTTPError as error:
            raise GetAccessTokenError('HTTP or status error') from error
        try:
            return OauthAccessTokenResponse(**response.json()).access_token
        except ValidationError as error:
            raise GetAccessTokenError('Incorrect server response') from error

    async def get_user_data(
            self,
            access_token: str,
            http_client: 'AsyncClient',
    ) -> GitHubUserData:
        try:
            response = await http_client.get(
                url=USER_API_URL,
                headers=create_bearer_auth_header(access_token),
            )
            return GitHubUserData.model_validate(response.json())
        except (HTTPError, ValidationError) as error:
            raise OauthError('Cant fetch user data') from error

    def validate_state(self, state: str):
        try:
            jwt.decode(
                jwt=state,
                key=self.state_secret,
                algorithms=[self._encode_algorithm],
            )
        except InvalidTokenError as error:
            raise InvalidStateError() from error

    @property
    def state(self) -> str:
        return jwt.encode(
            payload={'iss': 'MillServer'},
            key=self.state_secret,
            algorithm=self._encode_algorithm,
        )
