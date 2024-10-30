# routing.py
from django.urls import path
from .consumers import MensajeConsumer

websocket_urlpatterns = [
    path('ws/mensajes/', MensajeConsumer.as_asgi()),
]
