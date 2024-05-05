from datetime import datetime
from uuid import UUID

import jwt
from pydantic import BaseModel, ConfigDict

from millserver.settings import settings

ONE_YEAR = 60 * 60 * 24 * 365


class AccessTokenPayload(BaseModel):
    sub: str
    exp: int
    oauth_type: str
    oauth_token: str

    model_config = ConfigDict(extra='ignore')


def create_jwt_token(user_id: UUID, oauth_token: str) -> str:
    return jwt.encode(
        payload={
            'sub': str(user_id),
            'exp': int(datetime.now().timestamp()) + ONE_YEAR,
            'oauth_type': 'github',
            'oauth_token': oauth_token,
        },
        key=settings.state_secret,
        algorithm='HS256',
    )


def decode_jwt_token(token: str) -> AccessTokenPayload:
    return AccessTokenPayload.model_validate(jwt.decode(
        jwt=token,
        key=settings.state_secret,
        algorithms=['HS256'],
    ))
