from granian import Granian
from granian.constants import Interfaces


def cli():
    Granian(
        target='millserver:app',
        interface=Interfaces.ASGI,
    ).serve()


if __name__ == '__main__':
    cli()
