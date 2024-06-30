"""
ASGI config for MessageApp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack
from django.core.asgi import get_asgi_application
from django.urls import path
from myWhisper.consumers import WhisperConsumer
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MessageApp.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/chat/", WhisperConsumer.as_asgi()),
            # Add more paths for other WebSocket consumers as needed
        ])
    ),
})

