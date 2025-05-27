from django.utils.timezone import now

class DebugWebSocketMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "websocket":
            print(f"[DEBUG] WebSocket connection initiated at {now()} | Scope: {scope}")
        try:
            await self.app(scope, receive, send)
        except Exception as e:
            print(f"[ERROR] WebSocket processing failed: {e}")
            raise
