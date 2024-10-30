# asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from main.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.prod')

django_application = get_asgi_application()


application = ProtocolTypeRouter({
    # Define Django ASGI application to handle HTTP protocols
    "http": django_application,
    # Define WebSocket application to handle WebSocket protocols
    "websocket": URLRouter(websocket_urlpatterns)
})
