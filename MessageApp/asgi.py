"""
ASGI config for MessageApp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from myWhisper import routing
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MessageApp.settings')

# ProtocolTypeRouter: direct the incoming connections to different handlers
# based on the type of the protocol (HTTP or WebSocket)
application = ProtocolTypeRouter(
    {
        # HTTP handler
        "http": get_asgi_application(),
        # WebSocket handler
        # route Websocket connections based on URL patterns on websocket_urlpatterns
        "websocket": AuthMiddlewareStack(
            URLRouter(
                routing.websocket_urlpatterns
            )
        )
    }
)
