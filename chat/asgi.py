import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoProject.settings")

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import CookieMiddleware, SessionMiddleware
from chat.routing import websocket_urlpatterns
from chat.middleware import DebugWebSocketMiddleware
from chat.token_auth import TokenAuthMiddleware
from chat.admin_auth import AdminAuthBypassMiddleware
from chat.auth_stack import CustomAuthMiddlewareStack

# Упрощённый стек middleware
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": CookieMiddleware(  # CookieMiddleware выше SessionMiddleware
        SessionMiddleware(          # SessionMiddleware добавляет сессии
            DebugWebSocketMiddleware(  # Для отладки WebSocket
                TokenAuthMiddleware(  # Аутентификация через токены
                    AdminAuthBypassMiddleware(  # Пропуск проверки для администраторов
                        CustomAuthMiddlewareStack(  # Пользовательский стек аутентификации
                            URLRouter(websocket_urlpatterns)  # WebSocket маршруты
                        )
                    )
                )
            )
        )
    ),
})