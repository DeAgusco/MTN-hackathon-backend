# wallet_api/middleware.py

from channels.db import database_sync_to_async
from django.contrib.auth.models import User, AnonymousUser

@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()

class QueryAuthMiddleware:
    """
    Custom middleware that takes user IDs from the query string.
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        # Look up user from query string
        query_string = scope.get('query_string', b'').decode()
        query_params = dict(param.split('=') for param in query_string.split('&'))
        user_id = query_params.get('user_id')

        if user_id:
            scope['user'] = await get_user(int(user_id))
        else:
            scope['user'] = AnonymousUser()

        # Call the next middleware or consumer
        return await self.app(scope, receive, send)
