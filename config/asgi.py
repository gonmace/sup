import os
from django.core.asgi import get_asgi_application
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.prod')

django_application = get_asgi_application()


async def websocket_application(scope, receive, send):
    while True:
        event = await receive()
        if event['type'] == 'websocket.connect':
            await send({'type': 'websocket.accept'})
        if event['type'] == 'websocket.disconnect':
            break
        if event['type'] == 'websocket.receive':
            if event['text'] == 'ping':
                await send({'type': 'websocket.send', 'text': 'pong'})

websocket_patterns = [
    path('ws/somepath/', websocket_application),
]

application = ProtocolTypeRouter({
    # Define Django ASGI application to handle HTTP protocols
    "http": django_application,
    # Define WebSocket application to handle WebSocket protocols
    "websocket": URLRouter(websocket_patterns)
})
