# your_app/routing.py
from django.urls import re_path
from channels.routing import ProtocolTypeRouter, URLRouter, get_default_application
from channels.auth import AuthMiddlewareStack
from .consumers import WhisperConsumer

application = ProtocolTypeRouter({
    "http": get_default_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            re_path(r'ws/chat/$', WhisperConsumer.as_asgi()),
        ])
    ),
})
