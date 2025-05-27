from channels.middleware import BaseMiddleware
import logging

logger = logging.getLogger('django')


class AdminAuthBypassMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        # Перенос импорта внутрь метода
        from django.contrib.auth.models import AnonymousUser

        # Check if this is a WebSocket connection to the admin endpoint
        if scope["type"] == "websocket" and scope.get("path") == "/ws/admin/":
            logger.debug("Admin WebSocket connection detected, bypassing authentication checks")
            # Set a flag in the scope to indicate that this is an admin connection
            scope['is_admin_ws'] = True
            # Ensure the user is set (even if it's AnonymousUser)
            if 'user' not in scope:
                scope['user'] = AnonymousUser()

        # Pass the request to the next middleware in the stack
        return await super().__call__(scope, receive, send)