from channels.auth import AuthMiddlewareStack
import logging

logger = logging.getLogger('django')

class CustomAuthMiddlewareStack:
    """
    Custom auth middleware stack that bypasses authentication checks for admin WebSocket connections.
    """
    def __init__(self, inner):
        self.inner = AuthMiddlewareStack(inner)

    async def __call__(self, scope, receive, send):
        # Ленивый импорт
        from django.contrib.auth.models import AnonymousUser

        # Check if this is an admin WebSocket connection (flag set by AdminAuthBypassMiddleware)
        if scope.get("is_admin_ws", False):
            logger.debug("Bypassing authentication checks for admin WebSocket connection")
            # Skip authentication checks for admin WebSocket connections
            return await self.inner.inner(scope, receive, send)
        else:
            # Apply normal authentication checks for other connections
            return await self.inner(scope, receive, send)