from granian import Granian
from granian.constants import Interfaces


def cli():
    Granian(
        address='0.0.0.0',
        target='millserver:app',
        interface=Interfaces.ASGI,
    ).serve()


if __name__ == '__main__':
    cli()
