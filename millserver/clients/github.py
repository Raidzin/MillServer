from httpx import AsyncClient, HTTPError
from pydantic import BaseModel, ConfigDict, HttpUrl

from millserver.exceptions import GitHubAPIError

GITHUB_USER_API_URL = 'https://api.github.com/user'


def create_bearer_auth_header(bearer_token: str) -> dict[str, str]:
    return {'authorization': f'Bearer {bearer_token}'}


class OauthUserData(BaseModel):
    login: str
    avatar_url: HttpUrl

    model_config = ConfigDict(extra='ignore')


async def get_github_user_data(
        github_access_token: str,
        http_client: AsyncClient,
) -> OauthUserData:
    try:
        response = await http_client.get(
            url=GITHUB_USER_API_URL,
            headers=create_bearer_auth_header(github_access_token),
        )
        response.raise_for_status()
    except HTTPError as error:
        raise GitHubAPIError() from error
    return OauthUserData(**response.json())
