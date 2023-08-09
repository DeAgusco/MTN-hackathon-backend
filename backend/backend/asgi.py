# backend/asgi.py
import os
from django.core.asgi import get_asgi_application
from wallet_api.middleware import QueryAuthMiddleware
from channels.routing import ProtocolTypeRouter, URLRouter
from .routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": QueryAuthMiddleware(  # Apply your CustomAuthMiddleware here
        URLRouter(websocket_urlpatterns)
    ),
})
