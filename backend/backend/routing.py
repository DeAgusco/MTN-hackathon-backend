# your_app/routing.py
from django.urls import re_path
from wallet_api import consumers

websocket_urlpatterns = [
    re_path(r'ws/transactions/$', consumers.TransactionConsumer.as_asgi()),
]
