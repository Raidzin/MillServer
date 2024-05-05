from uuid import UUID

from millserver.models import User
from millserver.repository import UserRepository


async def create_user(
        login: str,
        user_repository: UserRepository,
) -> UUID:
    new_user = User(login=login)
    await user_repository.add(
        data=new_user,
        auto_commit=True,
        auto_refresh=True,
    )
    return new_user.id


async def get_user_or_none_by_login(
        login: str,
        user_repository: UserRepository,
) -> User | None:
    return await user_repository.get_one_or_none(login=login)
