from django.urls import path, include
from myWhisper.consumer import WhisperConsumer

# the empty string routes to ChatConsumer, which manages the chat functionality.
websocket_urlpatterns = [
    path("", WhisperConsumer.as_asgi()),
]