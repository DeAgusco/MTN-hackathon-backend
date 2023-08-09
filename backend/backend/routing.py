from wallet_api import consumers
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r'ws/transactions/$', consumers.TransactionConsumer.as_asgi()),
]

