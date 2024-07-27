"""
ASGI config for MessageApp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MessageApp.settings')
django.setup()

import myWhisper.routing

app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        # HTTP handler
        "http": app,
        # WebSocket handler
        # route Websocket connections based on URL patterns on websocket_urlpatterns
        "websocket": AuthMiddlewareStack(
            URLRouter(
                myWhisper.routing.websocket_urlpatterns
            )
        )
    }
)
