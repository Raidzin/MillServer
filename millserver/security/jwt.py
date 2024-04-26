from datetime import datetime

from pydantic import BaseModel

ONE_YEAR = 60 * 60 * 24 * 365


class AccessTokenPayload(BaseModel):
    iss: str
    exp: int
    oauth_token: str


def create_jwt_token(user_id, oauth_token):
    payload = {
        'sub': user_id,
        'iss': 'https://raidzin.ddns.net:3000/api/v1/mill',
        'exp': int(datetime.now().timestamp()) + ONE_YEAR,
    }
