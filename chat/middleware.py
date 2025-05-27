from django.utils.timezone import now

class DebugWebSocketMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "websocket":
            # Логируем содержимое scope
            print(f"[DEBUG] WebSocket scope at initiation: {scope}")
            if "cookies" in scope and scope['cookies']:
                print(f"[DEBUG] Cookies in scope: {scope['cookies']}")
            else:
                print("[WARNING] No cookies in WebSocket scope!")
        try:
            await self.app(scope, receive, send)
        except Exception as e:
            print(f"[ERROR] WebSocket processing failed: {e}")
            raise

class EnforceSessionMiddleware:
    """
    Middleware to ensure session data is added to the WebSocket scope.
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # Ensure that session data is available in scope
        if "session" not in scope:
            from channels.sessions import CookieMiddleware, SessionMiddlewareStack
            scope['session'] = {}  # Fallback if no session is loaded
        await self.app(scope, receive, send)
