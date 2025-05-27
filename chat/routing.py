from django.urls import path
from . import consumers
from chat.consumers import ChatConsumer




websocket_urlpatterns = [
    path('ws/chat/<str:session_id>/', ChatConsumer.as_asgi()),
    path('ws/chat/<int:user_id>/', ChatConsumer.as_asgi()),
    path("ws/admin/", consumers.AdminConsumer.as_asgi()),
]
