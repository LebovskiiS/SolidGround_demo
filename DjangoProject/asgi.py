"""
ASGI config for DjangoProject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from chat.routing import websocket_urlpatterns
from chat.middleware import DebugWebSocketMiddleware
from chat.token_auth import TokenAuthMiddleware
from chat.admin_auth import AdminAuthBypassMiddleware
from chat.auth_stack import CustomAuthMiddlewareStack
from channels.sessions import CookieMiddleware, SessionMiddleware

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": CookieMiddleware(  # CookieMiddleware must wrap SessionMiddleware
        SessionMiddleware(
            DebugWebSocketMiddleware(
                TokenAuthMiddleware(
                    AdminAuthBypassMiddleware(
                        CustomAuthMiddlewareStack(
                            URLRouter(
                                websocket_urlpatterns
                            )
                        )
                    )
                )
            )
        )
    ),
})
