# your_app/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

class TransactionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("WebSocket connected")
        user = self.scope['user']
        
        if user.is_anonymous:
            await self.close()

        # Create a unique group for the user
        await self.channel_layer.group_add(
            f"user_{user.id}_group",
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        user = self.scope['user']
        await self.channel_layer.group_discard(
            f"user_{user.id}_group",
            self.channel_name
        )

    async def transaction_initiation(self, event):
        await self.send(text_data=json.dumps({
            'message': 'Transaction initiated',
            'type': 'initiation'
        }))

    async def transaction_verification(self, event):
        await self.send(text_data=json.dumps({
            'message': 'Transaction verified',
            'type': 'verification'
        }))

    async def transaction_reversal(self, event):
        await self.send(text_data=json.dumps({
            'message': 'Transaction reversed',
            'type': 'reversal'
        }))
