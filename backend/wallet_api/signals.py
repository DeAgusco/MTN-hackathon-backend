# in signals.py

# import the necessary modules
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# import your models
from .models import OfflineMessage

# define a signal that is triggered when a user logs in
@receiver(user_logged_in)
def retrieve_offline_messages(sender, request, user, **kwargs):
    # get all the offline messages for the user
    offline_messages = OfflineMessage.objects.filter(recipient=user)
    # get the channel layer to communicate with the user's group
    channel_layer = get_channel_layer()

    # loop through the offline messages
    for message in offline_messages:
        # send the message to the user's group using the channel layer
        async_to_sync(channel_layer.group_send)(
            f"user_{user.id}_group",
            {
                "type": "offline_message",
                "message": message.message,
                "timestamp": str(message.timestamp)
            }
        )
        # delete the message from the database after sending it
        message.delete()
