from litestar import Litestar, get


@get("/")
async def index() -> str:
    return 'Hello, LiteStar!'


app = Litestar([index])
