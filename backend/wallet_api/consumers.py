# your_app/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from account.models import UserProfile
from django.utils import timezone
from channels.db import database_sync_to_async
class TransactionConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def get_or_create_user_profile(self, user_id):
        user_profile, created = UserProfile.objects.get_or_create(user_id=user_id)
        user_profile.is_online = True
        user_profile.last_active = timezone.now()
        user_profile.save()
        return user_profile
    @database_sync_to_async
    def get_or_create_user_profile_offline(self, user_id):
        user_profile, created = UserProfile.objects.get_or_create(user_id=user_id)
        user_profile.is_online = False
        user_profile.last_active = timezone.now()
        user_profile.save()
        return user_profile
    async def connect(self):
        print("WebSocket connected")
        user = self.scope['user']
        user_id = self.scope['user'].id
        
        user_profile = await self.get_or_create_user_profile(user_id)
        
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
        # Update user's online status
        user_id = self.scope['user'].id
        user_profile = await self.get_or_create_user_profile_offline(user_id)
        
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
        
    async def offline_message(self, event):
        await self.send(text_data=json.dumps(event['message']))

