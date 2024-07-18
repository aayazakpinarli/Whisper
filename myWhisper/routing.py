from django.urls import path
from myWhisper.consumer import WhisperConsumer

# the empty string routes to ChatConsumer, which manages the chat functionality.
websocket_urlpatterns = [
    # as_asgi is a method in channels/consumer.py
    path("", WhisperConsumer.as_asgi()),
]
