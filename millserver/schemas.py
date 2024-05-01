from uuid import UUID

from pydantic import BaseModel, ConfigDict, HttpUrl


class UserData(BaseModel):
    id: UUID
    login: str
    username: str | None = None
    avatar_url: HttpUrl | None = None

    model_config = ConfigDict(extra='ignore')