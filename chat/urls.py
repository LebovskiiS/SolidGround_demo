from django.urls import path
from .views import *


appname = 'chat'


urlpatterns = [
    path('<int:user_id>/', send_get_message_gpt, name='send_get_message'),
    path('user/support/<int:user_id>/', support_chat_view, name='support_chat')
]

