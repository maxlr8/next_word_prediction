

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter,get_default_application
from channels.auth import AuthMiddlewareStack
from apps.nwp.routing  import websocket_urlspatterns
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = ProtocolTypeRouter(
    {
        'http':  get_asgi_application() ,
        'websocket': AuthMiddlewareStack(
            URLRouter(
              websocket_urlspatterns
            )
        )
    }
)

