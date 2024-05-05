from litestar.config.cors import CORSConfig

from millserver.settings import settings

cors_config = CORSConfig(allow_origins=settings.cors_origins.split(','))
