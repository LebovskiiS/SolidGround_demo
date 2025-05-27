from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from urllib.parse import parse_qs
import logging

logger = logging.getLogger('django')


class TokenAuthMiddleware(BaseMiddleware):
    """
    Custom middleware that takes a token from the query string or headers
    and authenticates the user.
    """

    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        from rest_framework.authtoken.models import Token  # <- Перенесен импорт
        from django.contrib.auth.models import AnonymousUser  # <- Перенесен импорт

        token = None

        # Log the headers for debugging
        headers = scope.get('headers', [])
        logger.debug(f"WebSocket connection headers: {headers}")

        # Try to get token from headers first
        for name, value in headers:
            if name.lower() == b'authorization':
                auth_header = value.decode('utf-8')
                logger.debug(f"Found authorization header: {auth_header}")
                if auth_header.startswith('Token '):
                    token = auth_header.split(' ')[1]
                    logger.debug(f"Extracted token: {token}")
                    break

        if not token and scope.get('query_string'):
            query_string = scope['query_string'].decode()
            logger.debug(f"No token in headers, checking query string: {query_string}")
            query_params = parse_qs(query_string)
            token = query_params.get('token', [None])[0]

        if token:
            logger.debug(f"Authenticating with token: {token}")
            user = await self.get_user_from_token(token)
            if user.is_authenticated:
                logger.debug(f"Successfully authenticated user: {user.username}")
            else:
                logger.debug(f"Failed to authenticate with token: {token}")
            scope['user'] = user
        else:
            logger.debug("No token found, setting user as AnonymousUser")
            scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user_from_token(self, token_key):
        from rest_framework.authtoken.models import Token  # <- Перенесен импорт
        from django.contrib.auth.models import AnonymousUser  # <- Перенесен импорт
        try:
            token = Token.objects.get(key=token_key)
            return token.user
        except Token.DoesNotExist:
            return AnonymousUser()