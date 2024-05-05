from datetime import datetime
from uuid import UUID

from litestar.contrib.sqlalchemy.base import UUIDBase
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

type UserID = UUID  # type: ignore[valid-type]


class User(UUIDBase):
    login: Mapped[str]
    username: Mapped[str | None] = mapped_column(nullable=True, default=None)

    # created_games: Mapped[list['Game']] = relationship(
    #     lazy='subquery',
    #     back_populates='creator'
    # )
    # black_games: Mapped[list['Game']] = relationship(
    #     lazy='subquery',
    #     back_populates='black_player'
    # )
    # white_games: Mapped[list['Game']] = relationship(
    #     lazy='subquery',
    #     back_populates='white_player'
    # )


class Game(UUIDBase):
    creator_id: Mapped[UserID] = mapped_column(ForeignKey('user.id'))
    black_player_id: Mapped[UserID] = mapped_column(ForeignKey('user.id'))
    white_player_id: Mapped[UserID] = mapped_column(ForeignKey('user.id'))
    start_time: Mapped[datetime]
    end_time: Mapped[datetime]

    # creator: Mapped[User] = relationship(
    #     lazy='subquery',
    #     back_populates='created_games',
    # )
    # black_player: Mapped[User] = relationship(
    #     lazy='subquery',
    #     back_populates='black_games',
    # )
    # white_player: Mapped[User] = relationship(
    #     lazy='subquery',
    #     back_populates='white_games',
    # )
