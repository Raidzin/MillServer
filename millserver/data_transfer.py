from litestar.contrib.pydantic.pydantic_dto_factory import PydanticDTO

from millserver.schemas import UserData

UserDTO = PydanticDTO[UserData]
