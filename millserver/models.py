from litestar.contrib.sqlalchemy.base import UUIDBase
from sqlalchemy.orm import Mapped, mapped_column


class User(UUIDBase):
    username: Mapped[str | None] = mapped_column(nullable=True, default=None)
