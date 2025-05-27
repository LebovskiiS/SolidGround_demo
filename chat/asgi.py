import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from chat.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoProject.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # WebSocket маршруты напрямую (без AuthMiddlewareStack для отладки)
    "websocket": URLRouter(
        websocket_urlpatterns  # Ваши маршруты WebSocket
    ),
})
